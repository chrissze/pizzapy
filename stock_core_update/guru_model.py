# STANDARD LIBS
import sys; sys.path.append('..')
import json

from itertools import dropwhile, takewhile
from typing import Any, List, Optional, Tuple, Union
from timeit import default_timer
from multiprocessing.managers import DictProxy
from multiprocessing import Manager, Process
from datetime import datetime
from urllib.request import Request, urlopen


# THIRD PARTY LIBS
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from numpy import float64
import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import re
import requests
from requests.models import Response

from PySide2.QtWidgets import (QApplication, QTableView, QVBoxLayout ,QWidget)

# CUSTOM LIBS
from dimsumpy.database.postgres import upsertquery, upsert_dict
from dimsumpy.qt5.dataframemodel import DataFrameModel
from batterypy.string.json import extract_nested_values
from batterypy.time.cal import get_trading_day, get_trading_day_utc
from batterypy.string.read import formatlarge, is_floatable, readf, readi, readlarge

# PROGRAM MODULES
from shared_model.sql_model import cnx, db_dict  # the postgres server must running
from shared_model.st_data_model import stock_list_dict



# PROGRAM MODULES
from price_cap_model import proxy_price_cap
from guru_debt_model import proxy_guru_debt
from guru_earn_model import proxy_guru_earn
from guru_interest_model import proxy_guru_interest
from guru_lynch_model import proxy_guru_lynch
from guru_strength_model import proxy_guru_strength


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


def guru_rev(s: str, d: DictProxy = {}) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    try:
        url: str = "https://www.gurufocus.com/term/per+share+rev/" + s + "/Revenue-per-Share/"
        print(url)
        r: Response = requests.get(url)
        html_text: str = r.text
        soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
        soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not soup_items else soup_items[0].get('content')
        strlist: List[str] = content.split()

        rev: Optional[float] = None if len(strlist) < 12 else readf(strlist[11][:-1])
        print('rev IS', rev)

        rev_soup_tables: ResultSet = soup.find_all('table')
        no_table: bool = len(rev_soup_tables) == 0
        if rev is not None:
            d['rev_per_share'] = rev

        rev_dfs: List[DataFrame] = [] if no_table else pandas.read_html(html_text, header=None)

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

        strlist1: List[str] = re.split('[<>%]+', html_text)
        strlist2: List[str] = list(dropwhile(lambda x: x != 'past 12 months', strlist1))
        strlist3: List[str] = strlist2[:40]
        growth_list: list[str] = list(filter(lambda x: readf(x), strlist3)) # growth strings of 1,3,5,10 years
        growth1y: Optional[float] = None if len(growth_list) < 1 else readf(growth_list[0])
        growth5y: Optional[float] = None if len(growth_list) < 3 else readf(growth_list[2])


        if growth1y is not None:
            d['growth1y'] = growth1y
        if growth5y is not None:
            d['growth5y'] = growth5y

        print(rev, revqr, rev4q, revpc, growth1y, growth5y)
        return rev, revqr, rev4q, revpc, growth1y, growth5y

    except requests.exceptions.RequestException as e:
        print('guru_rev RequestException: ', e)
        return None, None, None, None, None, None
    except Exception as e2:
        print('guru_rev Exception e2: ', e2)
        return None, None, None, None, None, None



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
        #print(strlist)
        rnd_mil: Optional[float] = None if len(strlist) < 12 else readf(strlist[11])
        print(rnd_mil)

        if rnd_mil is not None:
            d['rnd_mil'] = rnd_mil
        rndpc: Optional[float] = None if ('cap' not in d or rnd_mil is None) \
            else round((1000000.0 * rnd_mil / d['cap'] * 100.0), 2)
        if rndpc is not None:
            d['rndpc'] = rndpc

        print(rndpc)
        return rnd_mil
    except requests.exceptions.RequestException as e:
        print('guru_rd RequestException: ', e)
        return None
    except Exception as e2:
        print('guru_rd Exception e2: ', e2)
        return None



def guru_upsert_1s(symbol: str) -> str:
    SYMBOL: str = symbol.upper()
    manager = Manager()
    d = manager.dict()
    d['symbol'] = SYMBOL
    d['td'] = get_trading_day_utc()
    d['t'] = datetime.now().replace(microsecond=0)
    try:
        proxy_price_cap(SYMBOL, d)
        p1 = Process(target=proxy_guru_debt, args=(SYMBOL, d))
        p2 = Process(target=proxy_guru_earn, args=(SYMBOL, d))
        p3 = Process(target=proxy_guru_strength, args=(SYMBOL, d))
        p4 = Process(target=proxy_guru_interest, args=(SYMBOL, d))
        p5 = Process(target=proxy_guru_lynch, args=(SYMBOL, d))
        p6 = Process(target=guru_nn, args=(SYMBOL, d))
        p7 = Process(target=guru_rev, args=(SYMBOL, d))
        p8 = Process(target=guru_tb, args=(SYMBOL, d))
        p9 = Process(target=guru_zscore, args=(SYMBOL, d))
        p10 = Process(target=guru_rnd, args=(SYMBOL, d))

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

        coco: Optional[float] = None if not all(key in d for key in ['earnpc', 'net_capital_pc', 'tbookpc']) \
            else round((d['earnpc'] * 5.0 + d['net_capital_pc'] + d['tbookpc']), 2)
        if coco is not None:
            d['coco'] = coco

        print('length of GU dict (max 10): ', len(d))

        if len(d) > 3:
            upsert_dict(table='usstock_g', dict=d, primarykeys=db_dict['usstock_g'].get('pk'), con=cnx)
            print(f"""
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            GU upserted: {d}
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            """)
        else:
            print(f"""
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            NO GU upserted: {d}
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            """)

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









if __name__ == '__main__':

    stock = input('which stock do you want to check? ')
    get_barchart_marketcap(stock)
    #guru_rev(stock)
    #guru_upsert_1s(stock)
    print(default_timer())

