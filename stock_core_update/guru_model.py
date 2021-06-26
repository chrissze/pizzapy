
import sys; sys.path.append('..')
import json

from itertools import dropwhile
from typing import Any, List, Optional, Tuple, Union
from timeit import default_timer
from multiprocessing.managers import DictProxy
from multiprocessing import Manager, Process
from datetime import datetime
from urllib.request import Request, urlopen


from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from numpy import float64


import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series

import requests
from requests.models import Response

from PySide2.QtWidgets import (QApplication, QTableView, QVBoxLayout ,QWidget)

from dimsumpy.database.postgres import upsertquery, upsert_dict
from dimsumpy.qt5.dataframemodel import DataFrameModel
from batterypy.string.json import extract_nested_values
from batterypy.time.cal import get_trading_day, get_trading_day_utc
from batterypy.string.read import formatlarge, is_floatable, readf, readi, readlarge


from shared_model.sql_model import cnx, db_dict  # the postgres server must running
from shared_model.st_data_model import stock_list_dict


def bar_cap(s: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]] :
    headers = {'User-Agent': 'Safari/13.1.1'}
    try:
        url: str = "https://www.barchart.com/stocks/quotes/" + s
        print(url)
        r: Response = requests.get(url, headers=headers)
        #req = Request(url=url, headers=headers)
        #with urlopen(req) as r:
        #    rtext = r.read()

        soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        soup_items: ResultSet = soup.find('div', attrs={'data-ng-controller': 'symbolHeaderCtrl'})
        item = soup_items.get('data-ng-init')
        jason_px = json.loads(item[5:-1])

        #bar_dfs: List[DataFrame] = [] if bad_status else pandas.read_html(bar_r.text, header=None)
        #length_dfs = len(bar_dfs)

        px: Optional[float] = readf(jason_px.get('lastPrice'))
        if px is not None:
            d['px'] = px

        cap_soup_items: ResultSet = soup.find('script', id='bc-dynamic-config')
        jason_cap = json.loads(cap_soup_items.string)
        jason_cap_pretty = json.dumps(jason_cap, indent=2)
        marketcaps: List[Any] = extract_nested_values(jason_cap, 'marketCap')
        cap: Optional[float] = None if len(marketcaps) < 3 else marketcaps[2]
        #print(jason_cap_pretty)
        print(cap)

        #cap_strlist: List[str] = [] if bad_status else bar_soup_items.__str__().split('  ')
        #cap_str: str = '' if bad_status else cap_strlist[1].replace(',', '')
        #cap_multiplier: float = 1000.0 if len(bar_soup_items) > 10 else 1.0 # ETF length is 9; stock 14
        # multipler can also be determined by len(cap_strlist[0]
        #cap: Optional[float] = float(cap_str) * cap_multiplier if is_floatable(cap_str) else None
        if cap is not None:
            d['cap'] = cap
            d['capstr']: str = formatlarge(cap)
            print(px, cap, d['capstr'])
        return px, cap

    except requests.exceptions.RequestException as e:
        print('bar_cap RequestException: ', e)
        return None, None
    except Exception as e2:
        print('bar_cap Exception e2: ', e2)
        return None, None


def guru_debt(s: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]]:
    """ TTWO debt is 0.00 with tables, take two's debt is really 0.00
        USO is also 0.00 without table
    """
    try:
        debt_url: str = "https://www.gurufocus.com/term/Total_Debt_Per_Share/" + s + "/Total-Debt-per-Share/"
        print(debt_url) ##
        debt_r: Response = requests.get(debt_url)
        debt_soup: BeautifulSoup = BeautifulSoup(debt_r.text, 'html.parser')
        debt_soup_tables: ResultSet = debt_soup.find_all('table')
        no_table: bool = len(debt_soup_tables) == 0

        debt_dfs: List[DataFrame] = [] if no_table else pandas.read_html(debt_r.text, header=0)
        debt_str: Any = '' if no_table or len(debt_dfs) < 3 or debt_dfs[2].empty else debt_dfs[2].iloc[-1, -1] # can be str or float64 type
        # valid_type: bool = isinstance(debt_str, float64) or (isinstance(debt_str, str) and '.' in debt_str and len(debt_str) < 9)
        debt: Optional[float] = readf(debt_str)
        if debt is not None:
            d['debt_per_share'] = debt

        debtpc: Optional[float] = None if ('px' not in d or debt is None) else round((debt / d['px'] * 100.0), 2)
        if debtpc is not None:
            d['debtpc'] = debtpc

        print(debt, debtpc)
        return debt, debtpc

    except requests.exceptions.RequestException as e:
        print('guru_debt RequestException: ', e)
        return None, None
    except Exception as e2:
        print('guru_debt Exception e2: ', e2)
        return None, None


def guru_earn(s: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]]:
    try:
        earn_url: str = "https://www.gurufocus.com/term/eps_nri/" + s + "/EPS-without-NRI/"
        print(earn_url)
        earn_r: Response = requests.get(earn_url)
        earn_soup: BeautifulSoup = BeautifulSoup(earn_r.text, 'html.parser')

        earn_soup_items: ResultSet = earn_soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not earn_soup_items else earn_soup_items[0].get('content')

        earn_strlist: List[str] = content.split()
        earn_strlist2: List[str] = list(filter(lambda x: '$' in x, earn_strlist))
        earn: Optional[float] = readf(earn_strlist2[0][:-1]) if earn_strlist2 else None

        # ^ string will be 0.00 even if the symbol is invalid, string have a suffix dot.
        if earn is not None:
            d['earn_per_share'] = earn
        print('earn:', earn, d)
        earnpc: Optional[float] = None if ('px' not in d or earn is None) else round((earn / d['px'] * 100.0), 2)
        if earnpc is not None:
            d['earnpc'] = earnpc

        print('earnpc:', earnpc)
        return earn, earnpc
    except requests.exceptions.RequestException as e:
        print('guru_earn RequestException: ', e)
        return None, None
    except Exception as e2:
        print('guru_earn Exception e2: ', e2)
        return None, None


def guru_fs(s: str, d: DictProxy={}) -> Optional[int]:
    try:
        fs_url: str = "https://www.gurufocus.com/term/rank_balancesheet/" + s + "/Financial-Strength/"
        print(fs_url)
        fs_r: Response = requests.get(fs_url)
        fs_soup: BeautifulSoup = BeautifulSoup(fs_r.text, 'html.parser')

        fs_soup_items: ResultSet = fs_soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not fs_soup_items else fs_soup_items[0].get('content')
        fs_strlist: List[str] = content.split()

        fs: Optional[float] = None if fs_strlist.__len__() < 11 else readi(fs_strlist[10][:1])

        if fs is not None:
            d['strength'] = fs

        print(fs)
        return fs
    except requests.exceptions.RequestException as e:
        print('guru_fs RequestException: ', e)
        return None
    except Exception as e2:
        print('guru_fs Exception e2: ', e2)
        return None


def guru_interest(s: str, d: DictProxy={}) -> Tuple[Optional[float],Optional[float]]:
    try:
        interest_url: str = "https://www.gurufocus.com/term/InterestExpense/" + s + "/Interest-Expense/"
        print(interest_url)
        interest_r: Response = requests.get(interest_url)
        interest_soup: BeautifulSoup = BeautifulSoup(interest_r.text, 'html.parser')

        interest_soup_items: ResultSet = interest_soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not interest_soup_items else interest_soup_items[0].get('content')
        interest_strlist: List[str] = content.split()

        interest_mil: Optional[float] = None if len(interest_strlist) < 11 else readf(interest_strlist[10])
        print(interest_mil)
        if interest_mil is not None:
            d['interest_mil'] = interest_mil

        interestpc: Optional[float] = None if ('cap' not in d or interest_mil is None) \
            else round((1000000.0 * abs(interest_mil) / d['cap'] * 100.0), 4)
        if interestpc is not None:
            d['interestpc'] = interestpc

        print(s, interest_mil, interestpc)

        return interest_mil, interestpc

    except requests.exceptions.RequestException as e:
        print('guru_interest RequestException: ', e)
        return None, None
    except Exception as e2:
        print('guru_interest Exception e2: ', e2)
        return None, None


# ADI and CSX got error, no problem for status code
def guru_lynch(s: str, d: DictProxy={}) -> Tuple[Optional[float],Optional[float]]:
    try:
        url: str = "https://www.gurufocus.com/term/lynchvalue/" + s + "/Peter-Lynch-Fair-Value/"
        print(url)
        r: Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')

        soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not soup_items else soup_items[0].get('content')
        strlist: List[str] = content.split()

        lynch: Optional[float] = None if len(strlist) < 13 else readf(strlist[12][:-1])

        print(lynch)

        if lynch is not None:
            d['lynchvalue'] = lynch

        lynchmove: Optional[float] = None if ('px' not in d or lynch is None) \
            else round((lynch - d['px']) / d['px'] * 100.0, 2)
        if lynchmove is not None:
            d['lynchmove'] = lynchmove

        print(s, 'Fair Value:', lynch)
        print('Expected move: ', lynchmove, '%')

        return lynch, lynchmove


    except requests.exceptions.RequestException as e:
        print('guru_lynch RequestException: ', e)
        return None, None
    except Exception as e2:
        print('guru_lynch Exception e2: ', e2)
        return None, None



def guru_nn(s: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]]:
    try:
        nn_url: str = "https://www.gurufocus.com/term/NCAV/" + s + "/Net-Net-Working-Capital/"
        nn_r: Response = requests.get(nn_url)

        nn_soup: BeautifulSoup = BeautifulSoup(nn_r.text, 'html.parser')
        nn_soup_tables: ResultSet = nn_soup.find_all('table')
        no_table: bool = len(nn_soup_tables) == 0

        nn_dfs: List[DataFrame] = [] if no_table else pandas.read_html(nn_r.text, header=None)
        nn_str: Any = '' if no_table or len(nn_dfs) < 3 or nn_dfs[2].empty else nn_dfs[2].iloc[-1, -1]
        nn: Optional[float] = readf(nn_str)
        if nn is not None:
            d['net_capital'] = nn

        nnpc: Optional[float] = None if ('px' not in d or nn is None) else round((nn / d['px'] * 100.0), 2)
        if nnpc is not None:
            d['net_capital_pc'] = nnpc
        print(nn_url)
        print(nn, nnpc)
        return nn, nnpc
    except requests.exceptions.RequestException as e:
        print('guru_nn RequestException: ', e)
        return None, None
    except Exception as e2:
        print('guru_nn Exception e2: ', e2)
        return None, None


def guru_rev(s: str, d: DictProxy = {}) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    try:
        url: str = "https://www.gurufocus.com/term/per+share+rev/" + s + "/Revenue-per-Share/"
        print(url)
        r: Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not soup_items else soup_items[0].get('content')
        strlist: List[str] = content.split()

        rev: Optional[float] = None if len(strlist) < 12 else readf(strlist[11][:-1])
        print('rev IS', rev)

        rev_soup_tables: ResultSet = soup.find_all('table')
        no_table: bool = len(rev_soup_tables) == 0
        if rev is not None:
            d['rev_per_share'] = rev

        rev_dfs: List[DataFrame] = [] if no_table else pandas.read_html(r.text, header=None)

        revqr_str: Any = '' if no_table or len(rev_dfs) < 3 or rev_dfs[2].empty else rev_dfs[2].iloc[-1, -1]
        print('revqr_str IS', revqr_str)
        revqr: Optional[float] = readf(revqr_str)
        if revqr is not None:
            d['qtlyrev'] = revqr

        rev4q: Optional[float] = None if not all([revqr, rev]) else round((revqr * 4.0 / rev), 4)
        if rev4q is not None:
            d['qtlyrev_x4'] = rev4q

        revpc: Optional[float] = None if ('px' not in d or rev is None) else round((rev / d['px'] * 100.0), 2)
        if revpc is not None:
            d['revpc'] = revpc

        print(rev, revqr, rev4q, revpc)
        return rev, revqr, rev4q, revpc

    except requests.exceptions.RequestException as e:
        print('guru_rev RequestException: ', e)
        return None, None, None, None
    except Exception as e2:
        print('guru_rev Exception e2: ', e2)
        return None, None, None, None



def guru_tb(s: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]]:
    try:
        tb_url: str = "https://www.gurufocus.com/term/Tangibles_book_per_share/" + s + "/Tangible-Book-per-Share/"
        tb_r: Response = requests.get(tb_url)

        tb_soup: BeautifulSoup = BeautifulSoup(tb_r.text, 'html.parser')
        tb_soup_tables: ResultSet = tb_soup.find_all('table')
        no_table: bool = len(tb_soup_tables) == 0

        tb_dfs: List[DataFrame] = [] if no_table else pandas.read_html(tb_r.text, header=None)
        tb_str: Any = '' if no_table or len(tb_dfs) < 3 or tb_dfs[2].empty else tb_dfs[2].iloc[-1, -1]
        tb: Optional[float] = readf(tb_str)
        if tb is not None:
            d['tangible_book'] = tb
        tbpc: Optional[float] = None if ('px' not in d or tb is None) else round((tb / d['px'] * 100.0), 2)
        if tbpc is not None:
            d['tbookpc'] = tbpc

        print(tb_url)
        print(tb, tbpc) ##

        return tb, tbpc
    except requests.exceptions.RequestException as e:
        print('guru_tb RequestException: ', e)
        return None, None
    except Exception as e2:
        print('guru_tb Exception e2: ', e2)
        return None, None


def guru_zscore(s: str, d: DictProxy={}) -> Optional[float]:
    try:
        url: str = "https://www.gurufocus.com/term/zscore/" + s + "/Altman-Z-Score/"
        print(url)
        r: Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not soup_items else soup_items[0].get('content')
        strlist: List[str] = content.split()
        zscore: Optional[float] = None if len(strlist) < 11 else readf(strlist[10])
        print(zscore)

        if zscore is not None:
            d['zscore'] = zscore

        print(zscore)
        return zscore
    except requests.exceptions.RequestException as e:
        print('guru_zs RequestException: ', e)
        return None
    except Exception as e2:
        print('guru_zs Exception e2: ', e2)
        return None


def guru_rnd(s: str, d: DictProxy={}) -> Optional[float]:
    try:
        url: str = f"https://www.gurufocus.com/term/RD/{s}/Research-&-Development/"

        r: Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not soup_items else soup_items[0].get('content')
        strlist: List[str] = content.split()
        print(strlist)
        rnd: Optional[float] = None if len(strlist) < 8 else readf(strlist[7])
        print(rnd)

        if rnd is not None:
            d['rnd'] = rnd
        rndpc: Optional[float] = None if ('cap' not in d or rnd is None) \
            else round((1000000.0 * rnd / d['cap'] * 100.0), 2)
        if rndpc is not None:
            d['rndpc'] = rndpc

        print(rndpc)
        return rnd
    except requests.exceptions.RequestException as e:
        print('guru_rd RequestException: ', e)
        return None
    except Exception as e2:
        print('guru_rd Exception e2: ', e2)
        return None






def guru_revgrowth(s: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]]:
    try:
        url: str = f"https://www.gurufocus.com/financials/{s}"

        r: Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        soup_tables: ResultSet = soup.find_all('table')
        no_table: bool = len(soup_tables) == 0

        dfs: List[DataFrame] = [] if no_table else pandas.read_html(r.text, header=None)
        print(dfs[1])
        print('no. of dfs: ', len(dfs))
        growth5y_str: Any = '' if no_table or len(dfs) < 3 or dfs[1].empty else dfs[1].iloc[0, 2]
        growth1y_str: Any = '' if no_table or len(dfs) < 3 or dfs[1].empty else dfs[1].iloc[0, 3]
        growth5y: Optional[float] = readf(growth5y_str)
        growth1y: Optional[float] = readf(growth1y_str)
        print(growth5y)
        print(growth1y)

        if growth5y is not None:
            d['growth5y'] = growth5y

        if growth1y is not None:
            d['growth1y'] = growth1y

        return growth5y, growth1y
    except requests.exceptions.RequestException as e:
        print('revgrowth RequestException: ', e)
        return None, None
    except Exception as e2:
        print('revgrowth Exception e2: ', e2)
        return None, None


def guru_upsert_1s(symbol: str) -> str:
    code = symbol.upper()
    manager = Manager()
    d = manager.dict()
    d['symbol'] = code
    d['td'] = get_trading_day_utc()
    d['t'] = datetime.now().replace(microsecond=0)
    try:
        bar_cap(code, d)
        p1 = Process(target=guru_debt, args=(code, d))
        p2 = Process(target=guru_earn, args=(code, d))
        p3 = Process(target=guru_fs, args=(code, d))
        p4 = Process(target=guru_interest, args=(code, d))
        p5 = Process(target=guru_lynch, args=(code, d))
        p6 = Process(target=guru_nn, args=(code, d))
        p7 = Process(target=guru_rev, args=(code, d))
        p8 = Process(target=guru_tb, args=(code, d))
        p9 = Process(target=guru_zscore, args=(code, d))
        p10 = Process(target=guru_rnd, args=(code, d))
        p11 = Process(target=guru_revgrowth, args=(code, d))

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()
        p8.start()
        p9.start()
        p10.start()
        p11.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()
        p8.join()
        p9.join()
        p10.join()
        p11.join()

        coco: Optional[float] = None if not all(key in d for key in ['earnpc', 'net_capital_pc', 'tbookpc']) \
            else round((d['earnpc'] * 5.0 + d['net_capital_pc'] + d['tbookpc']), 2)
        if coco is not None:
            d['coco'] = coco

        print(d)

        if 'px' in d and 'earn_per_share' in d:
            upsert_dict(table='usstock_g', dict=d, primarykeys=db_dict['usstock_g'].get('pk'), con=cnx)
            print(f"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
GU upserted: {d}
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
""")
        else:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! no gu upsert: ', d)
        return symbol
    except Exception as e:
        print(symbol, 'guruupsert1s error: ', e)
        return symbol + ' guruupsert1s Exception e: ' + str(e)
    finally:  # To make sure processes are closed in the end, even if errors happen
        p1.close()
        p2.close()
        p3.close()
        p4.close()
        p5.close()
        p6.close()
        p7.close()
        p8.close()
        p9.close()
        p10.close()
        p11.close()









### Testing Lab ###



if __name__ == '__main__':

    stock = input('which stock do you want to check? ')

    guru_zscore(stock)
    #guru_upsert_1s(stock)
    print(default_timer())

