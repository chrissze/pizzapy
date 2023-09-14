

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
















def get_td_adjclose(FROM: date, TO: date, symbol: str) -> List[Tuple[date, float]]:
    """

    IMPORTS: execute_pandas_read()
    USED BY: tech_upsert_1s()
    
    Get price data from my own database table.

    The resuling list will have latest dates placed at the front as it is DESC.
    """
    sql = f"SELECT td, adj_close FROM stock_price WHERE symbol = '{symbol}' AND td >= '{FROM.isoformat()}' AND td <= '{TO.isoformat()}' ORDER BY td DESC"
    df: DataFrame = execute_pandas_read(sql) # no error for empty result
    td_adjclose_pairs: List[Any] = [tuple(x) for x in df.values] # List of 2-tuples
    return td_adjclose_pairs





def calculate_changes(symbol:str, pairs: List[Tuple[date, float]], td: date) -> None:
    """

    pairs argument is generated by get_td_adjclose()

    walrus operator := allows you to assign a value to a variable as part of an expression.
    
    # I must place td at last because it is the iterable argument
    """
    
    # latest dates tuples are placed in the front in pairs
    tuples = list(dropwhile(lambda x: x[0] > td, pairs))    # drop all dates exceeding target date   
    
    # td's closing price will the the first element, prices are placed from td to the past
    prices: List[float] = [adjclose for (_, adjclose) in tuples] 
    
    weekly_prices = prices[:1] + [x[1] for x in tuples[1:] if is_weekly_close(x[0])]
    
    plus_minus_20_prices = [x[1] for x in pairs if add_trading_days(td, -21) < x[0] < add_trading_days(td, 21) and x[0] != td]

    #print('fut_past_prices, ', fut_past_prices)
    #print('Fut_past length: ', len(fut_past_prices))

    td_price = first(prices)
    p20 = grab(prices, 20)
    p50 = grab(prices, 50)
    p125 = grab(prices, 125)
    p200 = grab(prices, 200)
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

    istop: Optional[bool] = all(td_price > price for price in plus_minus_20_prices) if len(plus_minus_20_prices) == 40 else None
    
    isbot: Optional[bool] = all(td_price < price for price in plus_minus_20_prices) if len(plus_minus_20_prices) == 40 else None
    if istop: 
        print(symbol, 'istop', istop, td_price, td, steep20)
    if isbot: 
        print(symbol, 'isbot', isbot, td_price, td, tg2002, tg5002, rsi,wrsi, steep20)

    print(td_price)
    print(p20)
    print(p50)
    print(ch2002)
    print(tg2002)
    print(rsi)
    print(wrsi)
    print(steep20)
    print(steep50)


def tech_upsert_1s(FROM: date, TO: date, SYMBOL: str) -> str:
    """
    DEPENDS ON: get_td_adjclose(), st_chg_calc()
    """
    pairs_from_date = add_trading_days(FROM, -1000)
    pairs_to_date = add_trading_days(TO, 20)

    td_adjclose_pairs: List[Any] = get_td_adjclose(pairs_from_date, pairs_to_date, SYMBOL)
    pairs_length = len(td_adjclose_pairs)
    from_to_trading_dates: List[date] = [x[0] for x in td_adjclose_pairs if FROM <= x[0] <= TO]

    last_trading_day = get_trading_day_utc()
    theory_len = tdate_length(pairs_from_date, min(last_trading_day, pairs_to_date))
    #print('ext_len', ext_len)
    #print('theory len:', theory_len)


    valid = (theory_len - pairs_length) < 3
    if valid:
        with Pool(os.cpu_count()) as pool:
            pool.map(partial(calculate_changes, SYMBOL, td_adjclose_pairs), from_to_trading_dates) # do not use kwargs

    else:
        print('theory_len:', theory_len)
        print('ext_len:', pairs_length)
        print('valid: ', valid)
        return (f' - no tech_upsert')
    return 'done'





def calc_up(lst) -> bool:
    em20 = ema(lst, 20)
    em125 = ema(lst, 125)
    return em20 > em125





def test():
    FROM = date(2017, 1, 1)
    TO = date(2023, 9, 14)
    pairs = get_td_adjclose(FROM, TO, 'AMD')
    
    td = date(2023, 8, 1)

    calculate_changes('AMD', pairs, td)




if __name__ == '__main__':
    test()