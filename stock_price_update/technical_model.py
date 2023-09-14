

# STANDARD LIBS
import sys; sys.path.append('..')
from datetime import date, datetime, timezone
from functools import partial
from itertools import dropwhile, repeat
import io
from multiprocessing import Pool
from multiprocessing.managers import DictProxy
import os
from timeit import default_timer
from typing import Any, Dict, List, Tuple, Optional

import shutil
import urllib


# THIRD PARTY LIBS
import pandas
from pandas import DataFrame
import requests


# CUSTOM LIBS
from batterypy.functional.list import first, grab
from batterypy.time.cal import add_trading_days, date_range, tdate_range, tdate_length, date_length,  get_trading_day_utc, is_weekly_close
from dimsumpy.finance.technical import ema, quantile, deltas, changes, rsi_calc, steep
from dimsumpy.web.crawler import get_urllib_text, get_csv_dataframe

# PROGRAM MODULES

from database_update.postgres_connection_model import execute_pandas_read
















def get_td_adjclose(FROM: date, TO: date, symbol: str) -> List[Any]:
    """

    IMPORTS: execute_pandas_read()
    USED BY: tech_upsert_1s()
    
    Get price data from my own database table.
    """
    sql = f"SELECT td, adj_close FROM stock_price WHERE symbol = '{symbol}' AND td >= '{FROM.isoformat()}' AND td <= '{TO.isoformat()}' ORDER BY td DESC"
    df: DataFrame = execute_pandas_read(sql) # no error for empty result
    pairs: List[Any] = [tuple(x) for x in df.values] # List of 2-tuples
    return pairs




def st_chg_calc(symbol:str, pairs: List[Tuple[date, float]], td: date) -> None:
    # I must place td at last because it is the iterable argument
    # if i create a connection here, it will be expensive
    d = {}
    d['t']: datetime = datetime.now().replace(second=0, microsecond=0)
    d['symbol'] = symbol
    d['td'] = td
    tuples = list(dropwhile(lambda x: x[0] > td, pairs))
    prices: List[float] = [px for (_, px) in tuples]
    weekly_prices = prices[:1] + [x[1] for x in tuples[1:] if is_weekly_close(x[0])]
    fut_past_prices = [x[1] for x in pairs if add_trading_days(td, -21) < x[0] < add_trading_days(td, 21) and x[0] != td]

    #print('fut_past_prices, ', fut_past_prices)
    #print('Fut_past length: ', len(fut_past_prices))

    d['px'] = (px := first(prices))
    d['p20'] = (p20 := grab(prices, 20))
    d['p50'] = (p50 := grab(prices, 50))
    d['p125'] = grab(prices, 125)
    d['p200'] = grab(prices, 200)
    list20 = changes(20, prices[:421])
    list50 = changes(50, prices[:451])
    ch2002 = quantile(0.02, list20)
    ch2098 = quantile(0.98, list20)
    ch5002 = quantile(0.02, list50)
    ch5098 = quantile(0.98, list50)
    tg2002 = p20 * (1.0 + ch2002)
    tg2098 = p20 * (1.0 + ch2098)
    tg5002 = p50 * (1.0 + ch5002)
    tg5098 = p50 * (1.0 + ch5098)


    rsi = rsi_calc(14, prices)
    wrsi = rsi_calc(14, weekly_prices)
    ema20 = ema(20, prices)
    ema50 = ema(50, prices)
    steep20 = steep(20, prices)
    steep50 = steep(50, prices)

    istop: Optional[bool] = None if len(fut_past_prices) != 40 else all(x < px for x in fut_past_prices)
    isbot: Optional[bool] = None if len(fut_past_prices) != 40 else all(x > px for x in fut_past_prices)
    # print(tg2002)
    # print(tg2098)
    # print(tg5002)
    # print(tg5098)
    # print(rsi)
    # print(wrsi)
    # print(ema20)
    # print(ema50)
    # print(steep20)
    # print(steep50)
    if istop: print(symbol, 'istop', istop, px, td, steep20)
    if isbot: print(symbol, 'isbot', isbot, px, td, tg2002, tg5002, rsi,wrsi, steep20)

    #print(d)
    #upsert_dict(table='usstock_tech', dict=d, primarykeys=db_dict['usstock_tech'].get('pk'), con=cnx)




def tech_upsert_1s(FROM: date, TO: date, SYMBOL: str) -> str:
    """
    DEPENDS ON: get_td_adjclose(), st_chg_calc()
    """
    past_day = add_trading_days(FROM, -1000)
    later_day = add_trading_days(TO, 20)

    extended_pairs: List[Any] = get_td_adjclose(past_day, later_day, SYMBOL)
    extended_length = len(extended_pairs)
    from_to_dates: List[date] = [x[0] for x in extended_pairs if FROM <= x[0] <= TO]

    ltd = get_trading_day_utc()
    theory_len = tdate_length(past_day, min(ltd, later_day))
    #print('ext_len', ext_len)
    #print('theory len:', theory_len)


    valid = (theory_len - extended_length) < 3
    if valid:
        with Pool(os.cpu_count()) as pool:
            pool.map(partial(st_chg_calc, SYMBOL, extended_pairs), from_to_dates) # do not use kwargs


    else:
        print('theory_len:', theory_len)
        print('ext_len:', extended_length)
        print('valid: ', valid)
        return (f' - no tech_upsert')
    return 'done'





def calc_up(lst) -> bool:
    em20 = ema(lst, 20)
    em125 = ema(lst, 125)
    return em20 > em125


def test():
    d1 = date(2018, 1, 1)
    d2 = date(2020, 4, 30)
    print(default_timer())



if __name__ == '__main__':
    test()