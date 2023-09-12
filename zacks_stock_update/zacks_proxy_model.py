"""

"""
# STANDARD LIBS
import sys; sys.path.append('..')
from datetime import date, datetime

from multiprocessing import Manager
from multiprocessing.managers import DictProxy, SyncManager
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS

import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series

import requests
from requests.models import Response
from requests.structures import CaseInsensitiveDict



# CUSTOM LIBS
from batterypy.string.read import readf, readi
from batterypy.time.cal import get_trading_day, get_trading_day_utc
from dimsumpy.web.crawler import get_html_dataframes, get_html_text

# PROGRAM MODULES
from general_update.general_model import initialize_proxy
from zacks_stock_update.zacks_earnings_model import proxy_zacks_earnings
from zacks_stock_update.zacks_scores_model import proxy_zacks_scores





def make_zacks_proxy(symbol: str) -> DictProxy:
    """
    IMPORTS: initialize_proxy(), proxy_zacks_earnings(), proxy_zacks_scores()
    USED BY: zacks_update_database_model.py (upsert_zacks)
    
    the symbol will be changed to upper case at upsert_zacks()
    """
    proxy = initialize_proxy(symbol)
    proxy_zacks_earnings(symbol, proxy)
    proxy_zacks_scores(symbol, proxy)
    return proxy




def test() -> None:
    symbol: str = input('What SYMBOL do you want to check? ')
    proxy = make_zacks_proxy(symbol)
    print(proxy)

if __name__ == '__main__':
    test()
