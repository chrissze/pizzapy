import sys;

from psycopg2._psycopg import cursor

sys.path.append('..')



from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from datetime import date, datetime

from dimsumpy.database.postgres import upsertquery, upsert_dict
from batterypy.time.cal import get_trading_day, get_trading_day_utc
from batterypy.string.read import formatlarge, is_floatable, readf, readi, readlarge, float0
from itertools import chain, dropwhile

from multiprocessing.managers import DictProxy, ListProxy, SyncManager
from multiprocessing import Manager,  Pool, Process

import os

import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series

import requests
from requests.models import Response
from shared_model.sql_model import cnx, db_dict  # the postgres server must running

from stock_core_update.guru_model import bar_cap

from timeit import default_timer
from typing import Any, List, Optional, Tuple, Union


def option_upsert_1s(symbol: str) -> str:
    code: str = symbol.upper()
    manager: SyncManager = Manager()
    d: DictProxy = manager.dict()
    d['symbol']: str = code
    d['td']: date = get_trading_day_utc()
    d['t']: datetime = datetime.now().replace(microsecond=0)
    try:
        #bar_cap(code, d)
        #op_nasdaq(code, d)
        p1: Process = Process(target=bar_cap, args=(code, d))
        p2: Process = Process(target=op_yahoo, args=(code, d))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        if 'callmoney' in d and 'putmoney' in d and 'cap' in d:
            totalmoney: float = d['callmoney'] + d['putmoney']
            d['callratio']: float = round((d['callmoney'] / totalmoney * 100.0), 1)
            d['putratio']: float = round((d['putmoney'] / totalmoney * 100.0), 1)
            d['callpc']: float = round((d['callmoney'] / d['cap'] * 100.0), 4)
            d['putpc']: float = round((d['putmoney'] / d['cap'] * 100.0), 4)

        #q: str = upsertquery('usstock_option', d.keys(), ['symbol', 'td'])
        #values = tuple(d.values())

        if 'callpc' in d:
            upsert_dict(table='usstock_option', dict=d, primarykeys=db_dict['usstock_option'].get('pk'), con=cnx)
            # c: cursor = cnx.cursor()
            # c.execute(q, values)
            # c.close()
            # cnx.commit()
            print(symbol, 'Upserted: ', d)
            return symbol
        else:
            print('no upsert: ', d)
            return symbol
    except Exception as e:
        print(symbol, ' optionupsert1s error: ', e)
        return symbol + ' optionupsert1s Exception e: ' + str(e)
    finally:  # To make sure processes are closed in the end, even if errors happen
        p1.close()
        p2.close()

def op_nasdaq(s: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]]:
    lower_code = s.lower()
    pool = Pool(os.cpu_count())
    option_url: str = f"https://www.nasdaq.com/symbol/{lower_code}/option-chain?dateindex=-1"
    print(option_url)
    try:
        option_r: Response = requests.get(option_url)
        bad_status: bool = option_r.status_code != 200

        option_soup: BeautifulSoup = BeautifulSoup(option_r.text, 'html.parser')
        option_soup_items: ResultSet = [] if bad_status else option_soup.find('div', id='OptionsChain-dates')
        option_soup_tags = [] if not option_soup_items else option_soup_items.find_all('a')

        main_urls = [] if not option_soup_tags else [x['href'] for x in option_soup_tags[0:-1]]


        result1 = pool.map(op_calc, main_urls)
        callm1 = sum(cm for cm, _, _ in result1)
        putm1 = sum(pm for _, pm, _ in result1)
        page_urls = list(chain.from_iterable(urls for _, _, urls in result1))

        result2 = pool.map(op_calc, page_urls)
        callm2 = sum(cm for cm, _, _ in result2)
        putm2 = sum(pm for _, pm, _ in result2)

        #print(callm1, putm1, page_urls)
        #print(callm2, putm2)

        callmoney = (callm1 + callm2) * 100.0
        putmoney = (putm1 + putm2) * 100.0

        if all([callmoney, putmoney]):
            d['callmoney'] = round(callmoney, 0)
            d['putmoney'] = round(putmoney, 0)

        return callmoney, putmoney

    except requests.exceptions.RequestException as e:
        print('opt RequestException: ', e)
        return None, None
    except Exception as e2:
        print('opt Exception e2: ', e2)
        return None, None
    finally:  # To make sure processes are closed in the end, even if errors happen
        pool.close()
        


def op_calc(page: str) -> Tuple[float, float, List[str]]:
    try:
        page_r: Response = requests.get(page)
        bad_status: bool = page_r.status_code != 200
        page_dfs: List[DataFrame] = [] if bad_status else pd.read_html(page_r.text, header=0)

        df = pd.DataFrame() if len(page_dfs) < 3 else page_dfs[2]
        cm, pm, page_urls = 0.0, 0.0, []
        if len(df.columns) == 16:
            df.columns = ['Calls', 'CallLast', 'CallChg', 'CallBid', 'CallAsk', 'CallVol', 'CallOI', 'Root', 'Strike',
                          'Puts', 'PutLast', 'PutChg', 'PutBid', 'PutAsk', 'PutVol', 'PutOI']
            df.CallLast = [float0(x) for x in df.CallLast]
            df.CallOI = [float0(x) for x in df.CallOI]
            df.CallVol = df.CallLast * df.CallOI

            df.PutLast = [float0(x) for x in df.PutLast]
            df.PutOI = [float0(x) for x in df.PutOI]
            df.PutVol = df.PutLast * df.PutOI

            cm: float = df.CallVol.sum()
            pm: float = df.PutVol.sum()


        if 'page=' not in page:
            page_soup: BeautifulSoup = BeautifulSoup(page_r.text, 'html.parser')
            page_soup_items: ResultSet = [] if bad_status else page_soup.find('div', id='pagerContainer')
            page_soup_tags = [] if not page_soup_items else page_soup_items.find_all('a')
            page_urls = [] if not page_soup_tags else list(set([x['href'] for x in page_soup_tags]))

        return cm, pm, page_urls

    except requests.exceptions.RequestException as e:
        print('opt calc RequestException: ', e)
        return 0.0, 0.0, []
    except Exception as e2:
        print('opt calc Exception e2: ', e2)
        return 0.0, 0.0, []


def op_yahoo(s: str, d: DictProxy = {}) -> Tuple[Optional[float], Optional[float]]:
    lower_code = s.lower()
    pool = Pool(os.cpu_count())
    url: str = f"https://finance.yahoo.com/quote/{s}/options"
    print(url)
    try:
        r: Response = requests.get(url)
        list1 = r.text.split('"')
        #print(raw_list)
        list2 = list(dropwhile(lambda s: s != 'expirationDates', list1))
        dates_str: str = list2[1][2:-2] if len(list2) > 1 else ''
        unix_dates: List[str] = dates_str.split(',')
        print(unix_dates)

        urls = [f'https://finance.yahoo.com/quote/{s}/options?date={d}' for d in unix_dates]

        print(urls)

        result = pool.map(yahoo_calc, urls)
        callmoney = sum(cm for cm, _, _, _ in result) * 100.0
        putmoney = sum(pm for _, pm, _, _ in result) * 100.0
        call_oi = sum(coi for _, _, coi, _ in result)
        put_oi = sum(poi for _, _, _, poi in result)

        print(f'{s} Call OI: {call_oi} ; Put OI: {put_oi}')

        if all([callmoney, putmoney]):
            d['callmoney'] = round(callmoney, 0)
            d['putmoney'] = round(putmoney, 0)

        print( callmoney, putmoney)
        return callmoney, putmoney

    except requests.exceptions.RequestException as e:
        print('opt RequestException: ', e)
        return None, None
    except Exception as e2:
        print('opt Exception e2: ', e2)
        return None, None
    finally:  # To make sure processes are closed in the end, even if errors happen
        pool.close()


def mytest():
    url2 = 'https://finance.yahoo.com/quote/AAPL/options?date=1642723200'
    url1: str =  'https://www.microsoft.com'
    r: Response = requests.get(url1)
    dfs = pd.read_html(r.text, header=0)
    print(dfs)


# temporarity give an Apple stock option url to page, need to delete it later @todo
def yahoo_calc(page: str) -> Tuple[float, float, float, float]:
    try:
        r: Response = requests.get(page)
        bad_status: bool = r.status_code != 200
        page_dfs: List[DataFrame] = [] if bad_status else pd.read_html(r.text, header=0)
        good_status: bool = len(page_dfs) > 1
        #print(good_status)
        call_df: DataFrame = page_dfs[0] if good_status else pd.DataFrame()
        put_df: DataFrame = page_dfs[1] if good_status else pd.DataFrame()

        if len(call_df.columns) == 11 and len(put_df.columns) == 11:
            call_df.columns = ['Contract', 'LTD', 'Strike', 'Last', 'Bid',
                               'Ask', 'Chg', 'PercentChg', 'Volume', 'OI', 'Vol']
            put_df.columns = ['Contract', 'LTD', 'Strike', 'Last', 'Bid',
                               'Ask', 'Chg', 'PercentChg', 'Volume', 'OI', 'Vol']

            call_df.Last = [float0(x) for x in call_df.Last]
            call_df.OI = [float0(x) for x in call_df.OI]
            call_df.Vol = call_df.Last * call_df.OI

            put_df.Last = [float0(x) for x in put_df.Last]
            put_df.OI = [float0(x) for x in put_df.OI]
            put_df.Vol = put_df.Last * put_df.OI

            cm: float = call_df.Vol.sum()
            pm: float = put_df.Vol.sum()
            coi: float = call_df.OI.sum()
            poi: float = put_df.OI.sum()
        else:
            cm, pm, coi, poi = 0.0, 0.0, 0.0, 0.0  # default return values
            print('elseee', page)
        return cm, pm, coi, poi

    except requests.exceptions.RequestException as e:
         print('yahoo_calc RequestException: ', e, page)
         return 0.0, 0.0, 0.0, 0.0
    except Exception as e2:
         print('yahoo_calc Exception e2: ', e2, page)
         return 0.0, 0.0, 0.0, 0.0






if __name__ == '__main__':
    url = 'https://www.nasdaq.com/symbol/amzn/option-chain?page=3'
    uso = "https://www.nasdaq.com/symbol/uso/option-chain?dateindex=6"
    aapl_op = 'https://finance.yahoo.com/quote/AAPL/options?date=1642723200'

    #op_yahoo('AMZN')
    option_upsert_1s('ZYXI')
    print(default_timer())
