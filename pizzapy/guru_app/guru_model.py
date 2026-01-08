


"""


initialize_guru > gather_guru > finalize_guru

"""
# STANDARD LIBRARIES

from datetime import date, datetime
import json

from multiprocessing import Manager
from multiprocessing.managers import DictProxy, SyncManager

from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
import requests


# CUSTOM LIBRARIES
from batterypy.string.json import extract_nested_values
from batterypy.string.read import formatlarge, readf
from batterypy.time.cal import get_trading_day_utc
from dimsumpy.web.crawler import get_html_soup


# STANDARD LIBS


from typing import Any, List, Optional, Tuple, Union
from timeit import default_timer
from multiprocessing.managers import DictProxy, SyncManager
from multiprocessing import Manager, Process
from datetime import datetime


# THIRD PARTY LIBS

# CUSTOM LIBS
from batterypy.time.cal import get_trading_day_utc



# STANDARD LIBRARIES

from multiprocessing.managers import DictProxy
from typing import Any, List, Optional


# THIRD PARTY LIBRARIES
import pandas as pd
from pandas import DataFrame



# CUSTOM LIBRARIES
from batterypy.string.read import readf
from dimsumpy.web.crawler import get_html_dataframes



























######################################################
### 1ST PHASE : INITIALIZE_GURU WITH PRICE AND CAP ###
######################################################


def get_barchart_price_cap(symbol: str) -> Tuple[Optional[float], Optional[float]] :
    """
    * INDEPENDENT *

    IMPORTS: json, beautifulsoup4, batterypy, dimsumpy
        
    I can use this function to display the marketcap dictionary in formatted string:
        json_cap_pretty: str = json.dumps(json_cap, indent=2)

    """
    barchart_url: str = f'https://www.barchart.com/stocks/quotes/{symbol}'
    barchart_soup: BeautifulSoup = get_html_soup(barchart_url)
    # soup.find function below is safe, it will return None if it cannot find the target.
    price_soup_items: Optional[Tag] = barchart_soup.find('div', attrs={'data-ng-controller': 'symbolHeaderCtrl'})
    price_item: Optional[str] = price_soup_items.get('data-ng-init') if price_soup_items else None
    json_price: Optional[Dict[str, Any]] = json.loads(price_item[5:-1]) if price_item else None
    price: Optional[float] = readf(json_price.get('lastPrice')) if json_price else None

    cap_soup_items: ResultSet = barchart_soup.find('script', id='bc-dynamic-config')
    json_cap: Dict[str, Any] = json.loads(cap_soup_items.string)
    marketcaps: List[Any] = extract_nested_values(json_cap, 'marketCap')
    cap: Optional[float] = None if len(marketcaps) < 3 else readf(marketcaps[2])
    return price, cap


    

def initialize_guru(symbol: str) -> DictProxy:
    """
        
        IMPORTS: multiprocessing(DictProxy, SyncManager)
        DEPENDS: get_barchart_price_cap
        
        USED BY: make_option_proxy()

        I write `is not None` for testing below since price, cap might be 0, which is a false value.
    """
    manager: SyncManager = Manager()
    proxy: DictProxy = manager.dict()
    proxy['symbol'] = symbol
    proxy['td'] = get_trading_day_utc()
    proxy['t'] = datetime.now().replace(second=0, microsecond=0)

    price: Optional[float]
    cap: Optional[float]
    price, cap = get_barchart_price_cap(symbol)    
    proxy['price'] = price
    proxy['cap'] = cap
    proxy['cap_str'] = formatlarge(cap) if cap is not None else None
    return proxy


### END OF 1ST PHASE : INITIALIZE_GURU WITH PRICE AND CAP ###





###############################
### 2ND PHASE : GATHER_GURU ###
###############################



def get_guru_book_value(symbol: str) -> Optional[float]:
    """
    The returning value is Tangible Book Value Per Share.

    https://www.gurufocus.com/term/tangibles-book-per-share/AMD
    
Tangible book value per share is calculated as the total tangible equity divided by Shares Outstanding. Total tangible equity is calculated as the Total Stockholders Equity minus Preferred Stock minus Intangible Assets. 

https://www.gurufocus.com/term/Tangibles_book_per_share/NVDA/Tangible-Book-per-Share/

Try or not try? this module's proxy_guru_book_value() does not use try block,
this function is used in the last chain function in guru_proxy_model.py,
it is much faster to run 10 functions at the same time without nested try blocks.

"""

    book_value_url: str = f'https://www.gurufocus.com/term/tangibles-book-per-share/{symbol}'
    
    book_value_dfs: List[DataFrame] = get_html_dataframes(book_value_url)
    book_value_str: Any = '' if len(book_value_dfs) < 3 or book_value_dfs[1].empty else book_value_dfs[1].iloc[-1, -1] 
    book_value: Optional[float] = readf(book_value_str)
    return book_value




def proxy_guru_book_value(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS ON: get_guru_book_value
    
    USED BY: guru_proxy_model.py

    I use `is not None` to test because 0.0 is false.
    No need to use try block, as the last chaining function used this function will have tried.  
    """
    book_value: Optional[float] = get_guru_book_value(symbol)
    proxy['book_value'] = book_value

    book_value_pc: Optional[float] = round((book_value / proxy['price'] * 100.0), 2) if (proxy.get('price') and book_value) else None
    proxy['book_value_pc'] = book_value_pc
    return proxy












def gather_guru(SYMBOL: str) -> DictProxy:
    """
    DEPENDS: initialize_guru, proxy_guru_book_value() TO proxy_guru_zscore()
    
    """
    proxy: DictProxy = initialize_guru(SYMBOL)
    
    p1 = Process(target=proxy_guru_book_value, args=(SYMBOL, proxy))
    p2 = Process(target=proxy_guru_debt, args=(SYMBOL, proxy))
    p3 = Process(target=proxy_guru_earn, args=(SYMBOL, proxy))
    p4 = Process(target=proxy_guru_equity, args=(SYMBOL, proxy))
    p5 = Process(target=proxy_guru_interest, args=(SYMBOL, proxy))
    p6 = Process(target=proxy_guru_net_capital, args=(SYMBOL, proxy))
    p7 = Process(target=proxy_guru_net_margin, args=(SYMBOL, proxy))
    p8 = Process(target=proxy_guru_lynch, args=(SYMBOL, proxy))
    p9 = Process(target=proxy_guru_research, args=(SYMBOL, proxy))
    p10 = Process(target=proxy_guru_revenue, args=(SYMBOL, proxy))
    p11 = Process(target=proxy_guru_revenue_growths, args=(SYMBOL, proxy))
    p12 = Process(target=proxy_guru_strength, args=(SYMBOL, proxy))
    p13 = Process(target=proxy_guru_zscore, args=(SYMBOL, proxy))

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
    p12.start()
    p13.start()

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
    p12.join()
    p13.join()
    
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
    p12.close()
    p13.close()
    return proxy


### END OF 2ND PHASE : GATHER_GURU ###







#################################
### 3RD PHASE : FINALIZE_GURU ###
#################################


def calculate_wealth_pc(proxy: DictProxy) -> Optional[float]:
    """
    wealth_pc is the sum of NET CAPITAL + TANGIBLE BOOK VALUE + NEXT 5 YEARS EARNINGS, in percentage of market capitalization.
    
    USED BY: make_guru_proxy
    """
    wealth_keys: List[str] = ['cap', 'price', 'earn_pc', 'net_capital_pc', 'book_value_pc']
    valid_keys: bool = all(key in proxy for key in wealth_keys)    
    valid_values: bool = all(value is not None for key, value in proxy.items() if key in wealth_keys) if valid_keys else False
    wealth_pc: Optional[float] = round((proxy['earn_pc'] * 5.0 + proxy['net_capital_pc'] + proxy['book_value_pc']), 2) if valid_values else None
    return wealth_pc


def finalize_guru(symbol: str) -> DictProxy:
    """
    DEPENDS: gather_guru(), get_guru_wealth_pc()
    """
    proxy: DictProxy = gather_guru(symbol)
    wealth_pc: Optional[float] = calculate_wealth_pc(proxy)
    proxy['wealth_pc'] = wealth_pc
    return proxy


### END OF 3RD PHASE : FINALIZE_GURU ###



if __name__ == '__main__':
    stock = input('which stock do you want to check? ')
    
    x = finalize_guru(stock)
    
    print(x)

