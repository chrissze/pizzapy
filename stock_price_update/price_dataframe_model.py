
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
import requests


# CUSTOM LIBS
from batterypy.functional.list import first, grab
from batterypy.time.cal import add_trading_days, date_range, tdate_range, tdate_length, date_length,  get_trading_day_utc, is_weekly_close
from dimsumpy.finance.technical import ema, quantile, deltas, changes, rsi_calc, steep
from dimsumpy.web.crawler import get_urllib_text, get_csv_dataframe

# PROGRAM MODULES


# must use https
def make_price_url(date1: date, date2: date, symbol: str) -> str:
    """
    * INDEPENDENT *
    USED BY: get_price_dataframe()
    """
    datetime1 = datetime(date1.year, date1.month, date1.day)
    datetime2 = datetime(date2.year, date2.month, date2.day)
    unix_from = str(int(datetime1.replace(tzinfo=timezone.utc).timestamp()))
    unix_to = str(int(datetime2.replace(tzinfo=timezone.utc).timestamp()))
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={unix_from}&period2={unix_to}&interval=1d&events=history&crumb=OVcrHyGzap6'
    return url



# easier to debug for having 3 functions
# might have error during HK weekday night
def get_price_dataframe(date1, date2, symbol):
    """
    DEPENDS ON: make_price_url()
    IMPORTS: get_csv_dataframe()
    """
    url = make_price_url(date1, date2, symbol)
    df = get_csv_dataframe(url, header=0)
    df.columns = ['td', 'op', 'hi', 'lo', 'cl', 'adjcl', 'vol']
    df['symbol'] = symbol
    now = datetime.now().replace(second=0, microsecond=0)
    df['t'] = now  # program crashes if i put the now() statement here
    return df




def test():
    d1 = date(2019, 1, 1)
    d2 = date(2023, 2, 1)
    symbol = 'AMD'
    df = get_price_dataframe(d1, d2, symbol)
    print(df)

if __name__ == '__main__':
    test()