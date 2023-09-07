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

from random import random, uniform
import requests
from requests.models import Response
from shared_model.sql_model import cnx, db_dict  # the postgres server must running

from core_stock_update.guru_model import bar_cap
from time import sleep
from timeit import default_timer
from typing import Any, List, Optional, Tuple, Union


# bar_cap()     import
# op_yahoo()
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

            print(f"""
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            OPTION upserted: {d}
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            """)

            return symbol
        else:
            print(f"""
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            NO OPTION upserted: {d}
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            """)

            return symbol
    except Exception as e:
        print(symbol, ' optionupsert1s error: ', e)
        return symbol + ' optionupsert1s Exception e: ' + str(e)
    finally:  # To make sure processes are closed in the end, even if errors happen
        p1.close()
        p2.close()


# yahoo_calc()
def op_yahoo(s: str, d: DictProxy = {}) -> Tuple[Optional[float], Optional[float]]:
    lower_code = s.lower()
    #pool = Pool(os.cpu_count())
    pool = Pool(4)
    option_url: str = f"https://finance.yahoo.com/quote/{s}/options"
    print(option_url)
    try:
        headers: CaseInsensitiveDict = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        

        option_r: Response = requests.get(option_url, headers=headers)

        list1 = option_r.text.split('"')
        list2 = list(dropwhile(lambda s: s != 'expirationDates', list1))
        dates_str: str = list2[1][2:-2] if len(list2) > 1 else ''
        unix_dates: List[str] = dates_str.split(',')
        
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

        print("Call Money:", callmoney)
        print("Put Money:", putmoney)
        return callmoney, putmoney

    except requests.exceptions.RequestException as e1:
        print('op_yahoo() e1: ', e1)
        return None, None
    except Exception as e2:
        print('op_yahoo() e2: ', e2)
        return None, None
    finally:  # To make sure processes are closed in the end, even if errors happen
        pool.close()


def yahoo_calc(page: str) -> Tuple[float, float, float, float]:
    try:
        headers: CaseInsensitiveDict = requests.utils.default_headers()
        headers['User-Agent']: str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        calc_r: Response = requests.get(page, headers=headers)
        calc_text: str = calc_r.text
        sleep(random())  # sleep from 0 to 1 second
        bad_status: bool = calc_r.status_code != 200
        page_dfs: List[DataFrame] = [] if bad_status else pd.read_html(calc_text, header=0)
        good_status: bool = len(page_dfs) > 1
        #print("bad_status: ", bad_status)
        #print("good_status: ", good_status)
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
            print('else', page)
        return cm, pm, coi, poi

    except requests.exceptions.RequestException as e:
         print('yahoo_calc RequestException: ', e, page)
         return 0.0, 0.0, 0.0, 0.0
    except Exception as e2:
         print('yahoo_calc Exception e2: ', e2, page)
         return 0.0, 0.0, 0.0, 0.0



if __name__ == '__main__':
    op_yahoo('NVDA')
    print("Time lapsed: ", default_timer())
