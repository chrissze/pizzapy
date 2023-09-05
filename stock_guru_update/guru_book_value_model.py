"""    
Tangible book value per share is calculated as the total tangible equity divided by Shares Outstanding. Total tangible equity is calculated as the Total Stockholders Equity minus Preferred Stock minus Intangible Assets. 

https://www.gurufocus.com/term/Tangibles_book_per_share/NVDA/Tangible-Book-per-Share/

Try or not try? this module's proxy_guru_book_value() does not use try block,
this function is used in the last chain function in guru_proxy_model.py,
it is much faster to run 10 functions at the same time without nested try blocks.

"""

# STANDARD LIBRARIES
import sys; sys.path.append('..')
from multiprocessing.managers import DictProxy
from typing import Any, List, Optional


# THIRD PARTY LIBRARIES
from pandas.core.frame import DataFrame
import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf
from dimsumpy.web.crawler import get_html_dataframes

# PROGRAM MODULES
from stock_general_update.price_cap_model import proxy_price_cap



def get_guru_book_value(symbol: str) -> Optional[float]:
    """
    The returning value is Tangible Book Value Per Share.
    """
    book_value_url: str = f'https://www.gurufocus.com/term/Tangibles_book_per_share/{symbol}/Tangible-Book-per-Share/'
    book_value_dfs: List[DataFrame] = get_html_dataframes(book_value_url)
    book_value_str: Any = '' if len(book_value_dfs) < 3 or book_value_dfs[2].empty else book_value_dfs[2].iloc[-1, -1] 
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
    proxy['book_value'] = book_value if book_value is not None else None

    book_value_pc: Optional[float] = None if ('price' not in proxy or book_value is None) else round((book_value / proxy['price'] * 100.0), 2)
    proxy['book_value_pc'] = book_value_pc if book_value_pc is not None else None
    return proxy




def test_proxy_guru_book_value() -> None:    
    stock = input('which stock do you want to check book_value? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_book_value(stock, proxy=proxy)
    print(x)




if __name__ == '__main__':    
    test_proxy_guru_book_value()     
