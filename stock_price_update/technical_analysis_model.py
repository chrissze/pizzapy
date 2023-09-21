
# STANDARD LIBS
import sys; sys.path.append('..')
from collections import OrderedDict
from datetime import date, datetime, timezone
from functools import partial
from itertools import dropwhile, repeat
import io
from multiprocessing import Pool
from multiprocessing.managers import DictProxy, SyncManager
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
from batterypy.number.format import round0, round1, round2, round4

from dimsumpy.finance.technical import ema, quantile, deltas, convert_to_changes, calculate_rsi, steep
from dimsumpy.web.crawler import get_urllib_text, get_csv_dataframe

# PROGRAM MODULES

from database_update.postgres_connection_model import execute_pandas_read
from general_update.general_model import initialize_proxy
from stock_price_update.raw_price_model import get_price_dataframe, get_price_odict

















def get_td_odict(odict: OrderedDict[date, float], td: date) -> OrderedDict[date, float]:
    """
    * INDEPENDENT *
    IMPORTS: add_trading_days()
    USED BY: get_technical_values()
    """
    d500 = add_trading_days(td, -500)
    td_odict = OrderedDict((key, value) for key, value in odict.items() if d500 <= key <= td)
    return td_odict



def get_historical_prices(odict: OrderedDict[date, float], td: date) -> Any:
    """
    * INDEPENDENT *
    IMPORTS: add_trading_days()
    USED BY: calculate_target_prices()
    """
    td_price = odict.get(td)
    p20 = odict.get(add_trading_days(td, -20))
    p50 = odict.get(add_trading_days(td, -50))
    p100 = odict.get(add_trading_days(td, -100))
    p200 = odict.get(add_trading_days(td, -200))
    p500 = odict.get(add_trading_days(td, -500))
    return td_price, p20, p50, p100, p200, p500



def calculate_changes(prices: List[float], p20: Optional[float], p50: Optional[float]) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    * INDEPENDENT *
    IMPORTS: conver_to_changes(), quantile()
    USED BY: calculate_target_prices()
    """

    list_of_20_day_changes = convert_to_changes(20, prices) if prices else []
    list_of_50_day_changes = convert_to_changes(50, prices) if prices else []

    increase_20 = quantile(0.98, list_of_20_day_changes) if list_of_20_day_changes else None
    decrease_20 = quantile(0.02, list_of_20_day_changes) if list_of_20_day_changes else None
    increase_50 = quantile(0.98, list_of_50_day_changes) if list_of_50_day_changes else None
    decrease_50 = quantile(0.02, list_of_50_day_changes) if list_of_50_day_changes else None
    
    best_20 = p20 * (1.0 + increase_20) if p20 and increase_20 else None
    worst_20 = p20 * (1.0 + decrease_20) if p20 and decrease_20 else None
    best_50 = p50 * (1.0 + increase_50) if p50 and increase_50 else None
    worst_50 = p50 * (1.0 + decrease_50) if p50 and decrease_50 else None
    return increase_20, decrease_20, increase_50, decrease_50, best_20, worst_20, best_50, worst_50



def calculate_target_prices(td_odict: OrderedDict[date, float], td: date) -> Any:

    """
    DEPENDS ON:  get_historical_prices(), calculate_changes()

    USED BY: get_technical_values()

    td_odict's length is 501 if all data available, that is 2 years data before td

    td_odict argument needs to be descending in dates, that is latest dates are placed at the front.
    """
    td_price, p20, p50, p100, p200, p500 = get_historical_prices(td_odict, td)

    prices = list(td_odict.values()) if 498 <= len(td_odict) <= 501 else []
    
    increase_20, decrease_20, increase_50, decrease_50, best_20, worst_20, best_50, worst_50 = calculate_changes(prices, p20, p50)
    
    gain_20 = (best_20 - td_price) / td_price if td_price and best_20 else None
    fall_20 = (td_price - worst_20) / td_price if td_price and worst_20 else None
    gain_50 = (best_50 - td_price) / td_price if td_price and best_50 else None
    fall_50 = (td_price - worst_50) / td_price if td_price and worst_50 else None

    return td_price, p20, p50, p100, p200, p500, increase_20, decrease_20, increase_50, decrease_50, best_20, worst_20, best_50, worst_50, gain_20, fall_20, gain_50, fall_50





def get_rsi(odict: OrderedDict[date, float], td: date) -> Tuple[float, float]:
    """
    * INDEPENDENT *
    IMPORTS: is_weekly_close(), calculate_rsi()
    USED BY: get_technical_values()

    typical RSI input list needs to be at least 14 * 14 + 1 days, that is 197 trading days.
    Weekly RSI requires 197 * 5, approximately 1000 trading days
    """
    d199 = add_trading_days(td, -199)
    rsi_odict = OrderedDict((key, value) for key, value in odict.items() if d199 <= key <= td)
    prices = list(rsi_odict.values())
    rsi = calculate_rsi(14, prices)
    
    d999 = add_trading_days(td, -999)
    four_year_odict = OrderedDict((key, value) for key, value in odict.items() if d999 <= key <= td)
    
    weekly_prices: List[float] = [value for key, value in four_year_odict.items() if is_weekly_close(key)]
    weekly_rsi = calculate_rsi(14, weekly_prices)
    return rsi, weekly_rsi    




def get_technical_values(odict: OrderedDict[date, float], td: date) -> Any:
    """
    DEPENDS ON: get_td_odict(), calculate_target_prices()
    IMPORTS: round1(), round2(), round4()
    USED BY: make_technical_proxy()
    
    I must place td at last because it is the iterable argument in pool.map()
    """
    rsi, weekly_rsi = get_rsi(odict, td)

    td_odict = get_td_odict(odict, td)

    td_price, p20, p50, p100, p200, p500, increase_20, decrease_20, increase_50, decrease_50, best_20, worst_20, best_50, worst_50, gain_20, fall_20, gain_50, fall_50 = calculate_target_prices(td_odict, td)

    
    #technical_values = round2(td_price), round2(p20), round2(p50), round2(p125), round2(p200), round4(rsi), round4(weekly_rsi), round2(increase_20), round2(decrease_20), round2(increase_50), round2(decrease_50), round1(best_20), round1(worst_20), round1(best_50), round1(worst_50), round2(steep_20), round2(steep_50), is_top, is_bottom
    
    return td_price, p20, p50, p100, p200, p500, increase_20, decrease_20, increase_50, decrease_50, best_20, worst_20, best_50, worst_50, gain_20, fall_20, gain_50, fall_50



def test():
    FROM = date(2019, 4, 3)
    TO = date(2023, 3, 14)

    od = get_price_odict(FROM, TO, 'AMD', ascending=False)
    td = date(2023, 4, 3)
    
    tuple = get_technical_values(od, td)
    print(tuple)

if __name__ == '__main__':
    test()





