# STANDARD LIBRARIES

from itertools import dropwhile
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf
from dimsumpy.web.crawler import get_html_dataframes, get_html_soup

# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy





def get_guru_interest(symbol: str) -> Optional[float]:
    """    

    https://www.gurufocus.com/term/interest-expense/NVDA
    """

    interest_url: str = f'https://www.gurufocus.com/term/interest-expense/{symbol}'
    
    interest_dfs: List[DataFrame] = get_html_dataframes(interest_url)

    interest_str: Any = '' if len(interest_dfs) < 3 or interest_dfs[0].empty else interest_dfs[0].iloc[-1, -1] 
    
    negative_interest_in_million: Optional[float] = readf(interest_str)

    interest: Optional[float] = None if negative_interest_in_million is None else abs(negative_interest_in_million) * 1000000.0
    
    return interest






def proxy_guru_interest(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_interest > get_guru_interest"""
    interest: Optional[float]  = get_guru_interest(symbol)
    proxy['interest'] = interest
    
    interest_pc: Optional[float] = round((interest / proxy['cap'] * 100.0), 4) if (proxy.get('cap') and interest) else None
    proxy['interest_pc'] = interest_pc
    return proxy


def test():
    
    stock = input('which stock do you want to check interest? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_interest(stock)
    print(x)
    

if __name__ == '__main__':
    test()