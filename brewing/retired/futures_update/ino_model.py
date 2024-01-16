

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from cloudscraper import create_scraper, CloudScraper
from datetime import date, datetime

from dimsumpy.database.postgres import upsertquery
from batterypy.time.cal import get_trading_day_utc
from batterypy.time.date import is_iso_date_format
from batterypy.string.read import formatlarge, readf, readlarge, float0


from functools import partial
from multiprocessing.managers import DictProxy, ListProxy, SyncManager

from multiprocessing import Manager,  Pool, Process
import os

import pandas
from pandas.core.frame import DataFrame
from pandas.core.indexes.base import Index
from pandas.core.series import Series

import requests
from requests.models import Response
import requests.packages.urllib3



from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from shared_model.fut_data_model import all_fut, Contract, fut_dict

# from shared_model.sqlmodel import cnx, cur  # the postgres server must running
import ssl
import time
from timeit import default_timer
from typing import Any, Dict, List, Optional, Tuple, Union

from urllib3 import PoolManager
import urllib

def ino_upsert_all() -> None:
    for f in all_fut:
        ino_upsert_1s(f)


def ino_upsert_1s(s: str) -> str:
    # prevent error on importing cnx on shell:
    from shared_model.sql_model import cnx  # the postgres server must running

    manager: SyncManager = Manager()
    d: DictProxy = manager.dict()

    ino_ratio(s,d)

    try:

        # p1 = Process(target=ycharts_oi, args=(s, d))     # manager code will have error on running
        # p2 = Process(target=ino_op, args=(s, d, parallel))
        # p1.start()
        # p2.start()
        # p1.join()
        # p2.join()

        q: str = upsertquery('fut_option', d.keys(), ['symbol', 'td'])
        values: Tuple[Any, ...] = tuple(d.values())

        print(d)
        if 'callpc' in d:
            c = cnx.cursor()
            c.execute(q, values)
            c.close()
            cnx.commit()
            print(s, 'Upserted: ', d)
        else:
            print('no upsert: ', d)
        return s
    except Exception as e:
        print(s, ' inoupsert1s error: ', e)
        return s + ' inoupsert1s Exception e: ' + str(e)


def cme_oi(s: str, d: DictProxy={}) -> Optional[float]:
    try:
        contract: Optional[Contract] = fut_dict.get(s)  # contract is the value
        url0: Optional[str] = contract.get('url')
        url: str = url0 + '_quotes_volume_voi.html'
        print(url)
        browser1: WebDriver = webdriver.Chrome()
        browser1.get(url)
        time.sleep(2)
        tbl: WebElement = browser1.find_element_by_id("volumeDetailProductTable")
        htmltext: str = '<table>' + tbl.get_attribute('innerHTML') + '</table>'
        cme_dfs: List[DataFrame] = pandas.read_html(htmltext, header=0)
        df: DataFrame = pandas.DataFrame() if not cme_dfs else cme_dfs[0]
        oi: Optional[float] = None if df.empty else readf(df.iloc[-2, -2])
        if oi is not None:
            d['oi'] = oi
        time.sleep(1)
        browser1.close()
        print(s, type(oi), oi)
        return oi
    except Exception as e2:
        print('cme_oi Exception e2, switch to tradingcharts_oi() ', e2)
        tradingcharts_oi(s, d)


def tradingcharts_oi(s: str, d: DictProxy={}) -> Optional[float] :
    try:
        url: str = f'https://futures.tradingcharts.com/marketquotes/{s}.html' 
        print(url)
        browser: WebDriver = webdriver.Chrome()
        browser.get(url)  # navigate to the page
        time.sleep(2)
        tbl: WebElement = browser.find_element_by_id("tblQuote") # error if no such element
        htmltext: str = '<table>' + tbl.get_attribute('innerHTML') + '</table>'

        print(htmltext)

        cap_dfs: List[DataFrame] = pandas.read_html(htmltext, header=1)
        df: DataFrame = cap_dfs[0]
        oi_column: Series = [] if df.empty else df.iloc[0:, -2]
        columns: List[float] = [float0(x) for x in oi_column]
        oi: Optional[float] = None if not columns else sum(columns)
        if oi is not None:
            d['oi'] = oi

        time.sleep(1)
        browser.close()
        print(s, type(oi), oi)
        return oi

    except Exception as e2:
        print('tradingcharts_oi Exception e2, could use another function ycharts_oi() ', e2)
        ycharts_oi(s, d)






def ycharts_oi(s: str,  d: DictProxy={}) -> Optional[float] :
    """return the open interest in no. of contract """

    headers: CaseInsensitiveDict = requests.utils.default_headers()
    headers['User-Agent']: str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    try:
        contract: Optional[Contract] = fut_dict.get(s)
        url: str = contract.get('ycharts')
        print(url)
        r: Response = requests.get(url, headers=headers)
        bad_status: bool = r.status_code != 200
        print('bad_status: ', bad_status, r.status_code)
        html_text: str = r.text

        soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
        soup_items: ResultSet = soup.find_all('div', class_='key-stat-title')

        print(soup_items)
        
        str_list = str(soup_items).split()
        print(str_list)
        oi: Optional[float] = 1000000.0 if len(str_list) < 3 else readlarge(str_list[2])

        print(oi)
        if oi is not None:
             d['oi'] = oi

        return oi

    except requests.exceptions.RequestException as e:
        print('ycharts_oi RequestException: ', e)
        return None
    except Exception as e2:
        print('ycharts_oi Exception e2: ', e2)
        return None









def ino_ratio(s: str, d: DictProxy={}) -> Dict[str, Any]:
    """shell: inomodel.ino_ratio('GC')"""

    manager: SyncManager = Manager()
    #d: DictProxy = manager.dict()
    d['symbol']: str = s
    d['td']: date = get_trading_day_utc()
    d['t']: datetime = datetime.now().replace(microsecond=0)
    contract: Optional[Contract] = fut_dict.get(s)
    lot: Optional[float] = contract.get('lot')
    try:
        ycharts_oi(s, d)  # cme_oi and tradingcharts_oi will have errors on running
        ino_op(s, d)

        if {'callmoney', 'putmoney', 'oi', 'px'}.issubset(d):
            d['cap']: float = round((d['px'] * d['oi'] * lot), 0)
            d['cap_str']: str = formatlarge(d['cap'])
            totalmoney: float = d['callmoney'] + d['putmoney']
            d['callratio']: float = round((d['callmoney'] / totalmoney * 100.0), 1)
            d['putratio']: float = round((d['putmoney'] / totalmoney * 100.0), 1)
            d['callpc']: float = round((d['callmoney'] / d['cap'] * 100.0), 4)
            d['putpc']: float = round((d['putmoney'] / d['cap'] * 100.0), 4)


    except Exception as e:
        print(s, ' inoupsert1s error: ', e)
    print(d)
    return d

def ino_op_test() -> None:
    try:
        month_url: str = 'https://quotes.ino.com/exchanges/contracts.html?r=NYMEX_GC'
        #month_url: str = 'https://google.com'
        print(month_url)
        headers = {
            'Referer': 'https://quotes.ino.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '$0',
            'sec-ch-us-platform': 'macOS'
        }
        scraper = CloudScraper()
        month_r: Response = scraper.get(url=month_url, headers=headers)
        bad_status: bool = month_r.status_code != 200 #and month_r.status_code != 403
        #bad_status: bool = month_r.status != 200
        print(month_r.text)
        print('bad_status: ', bad_status, month_r.status_code)
        
    except Exception as e:
        print(e)


def ino_op(s: str,  d: DictProxy={}) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """
    example: ino_op('CL')
    return callmoney, putmoney, price
    6J got some invalid data with expiration dates missing
    """

    headers = {
        'Host': 'quote.ino.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest'
    }
    #headers: CaseInsensitiveDict = requests.utils.default_headers()
    
    #http = PoolManager()
    context = ssl._create_unverified_context()


    pool: Pool = Pool() # do not put into try block, as it need to be closed
    contract: Optional[Contract] = fut_dict.get(s)
    lot: Optional[float] = contract.get('lot')
    exchange: Optional[str] = contract.get('exchange')
    
    #requests.packages.urllib3.disable_warnings()

    if exchange == 'ICE':
        month_url: str = "https://quotes.ino.com/exchanges/contracts.html?r=" + exchange + "_@" + s
    else:
        #month_url: str = "https://quotes.ino.com/exchanges/contracts.html?r=" + exchange + "_" + s
        month_url: str = f"https://www.ino.com"

    print(month_url)
    try:
        http = PoolManager(ssl_minimum_version=ssl.TLSVersion.TLSv1)
        #month_r: Response = urllib.request.urlopen(month_url, context=context)
        #month_r: Response = http.request('GET', month_url, context=context)
        #month_r: Response = requests.post(url=month_url, headers=headers, verify='certs.pem')
        month_r: Response = requests.get(url=month_url, headers=headers, verify=True)
        bad_status: bool = month_r.status_code != 200 #and month_r.status_code != 403
        #bad_status: bool = month_r.status != 200
        print('bad_status: ', bad_status, month_r.status_code)
        #print('bad_status: ', bad_status, month_r.status)

        html_text: str = month_r.text
        
        #print(html_text)

        #month_dfs: List[DataFrame] = [] if bad_status else pandas.read_html(html_text, header=0)
        month_dfs: List[DataFrame] = pandas.read_html(html_text, header=0)
        
        print(month_dfs)
        df: DataFrame = pandas.DataFrame() if not month_dfs else month_dfs[0]
        px: Optional[float] = None if df.empty else readf(df.iloc[2, 5])
        if px is not None:
            d['px'] = px

        month_column: List[str] = [] if df.empty else list(df.iloc[2:, 0])
        months: List[str] = [ x for x in month_column if len(x) < 8] # ICE product has @
        #op_urls: List[str] = ["https://quotes.ino.com/options/?s=" + exchange + "_" + x for x in months]
        op_urls: List[str] = [f'https://quotes.ino.com/options/?s={exchange}_{x}' for x in months]
        result: List[Tuple[float, float]] = pool.map(ino_calc, op_urls)

        callmoney: float = sum(cm for cm, _ in result) * lot
        putmoney: float = sum(pm for _, pm in result) * lot

        if all([callmoney, putmoney]):
            d['callmoney']: float = round(callmoney, 0)
            d['putmoney']: float = round(putmoney, 0)

        return callmoney, putmoney, px

    except requests.exceptions.RequestException as e:
        print('opt RequestException: ', e)
        return None, None, None
    except Exception as e2:
        print('opt Exception e2: ', e2)
        return None, None, None
    finally:  # To make sure processes are closed in the end, even if errors happen
        pool.close()

"""
	dfObj.drop( dfObj[ dfObj['Age'] == 30 ].index , inplace=True)
# delete all rows with column 'Age' has value 30 to 40 
indexNames = df[ df['Expiration'] < date.today() ].index
df.drop(indexNames , inplace=True)
"""



def ino_calc(page: str) -> Tuple[float, float]:
    try:
        print(page)
        page_r: Response = requests.get(page)
        bad_status: bool = page_r.status_code != 200
        page_dfs: List[DataFrame] = [] if bad_status else pandas.read_html(page_r.text, header=0)

        df: DataFrame = pandas.DataFrame() if len(page_dfs) < 2 else page_dfs[1]
        cm: float = 0.0
        pm: float = 0.0
        if len(df.columns) == 10:
            df.columns: Index = ['Expiration', 'Strike', 'CallSymbol', 'CallLast', 'CallChg', 'CallOI'
                                  , 'PutSymbol', 'PutLast', 'PutChg', 'PutOI']
            df.dropna(subset=['Expiration'], inplace=True)

            df.Expiration: Series = [date.fromisoformat(x) if is_iso_date_format(x) else date.today() for x in df.Expiration]
            indexNames = df[df['Expiration'] <= date.today()].index # drop all dates earlier than today
            df.drop(indexNames, inplace=True)

            print(df)
            df.CallLast: Series = [float0(x) for x in df.CallLast]
            df.CallOI: Series = [float0(x) for x in df.CallOI]
            df.CallChg: Series = df.CallLast * df.CallOI

            df.PutLast: Series = [float0(x) for x in df.PutLast]
            df.PutOI: Series = [float0(x) for x in df.PutOI]
            df.PutChg: Series = df.PutLast * df.PutOI
            cm: float = df.CallChg.sum()
            pm: float = df.PutChg.sum()

        return cm, pm

    except requests.exceptions.RequestException as e:
        print('ino calc RequestException: ', e)
        return 0.0, 0.0
    except Exception as e2:
        print('ino calc Exception e2: ', e2)
        return 0.0, 0.0




if __name__ == '__main__':
    
    #symbol = input('which symbol do you want to check? ')

    #ycharts_oi(symbol)
    ino_op_test()
