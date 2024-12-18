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
from dimsumpy.web.crawler import get_html_soup

# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy




def get_guru_interest(symbol: str) -> Optional[float]:
    """    

    https://www.gurufocus.com/term/interest-expense/NVDA
    """

    interest_url: str = f'https://www.gurufocus.com/term/interest-expense/{symbol}'
    
    interest_soup: BeautifulSoup = get_html_soup(interest_url)
    
    interest_soup_items: ResultSet = interest_soup.find_all('meta', attrs={'name': 'description'})
    
    content: str = '' if not interest_soup_items else interest_soup_items[0].get('content')
    
    interest_strlist: List[str] = content.split()
    
    interest_strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', interest_strlist))    

    negative_interest_in_million: Optional[float] = None if len(interest_strlist_shortened) < 3 else readf(interest_strlist_shortened[1])
    
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