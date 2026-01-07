"""
https://www.gurufocus.com/term/rank-balancesheet/NVDA
"""


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


def get_guru_strength(symbol: str) -> Optional[float]:
    """
    https://www.gurufocus.com/term/rank-balancesheet/NVDA
    """
    strength_url: str = f'https://www.gurufocus.com/term/rank-balancesheet/{symbol}'
    strength_soup: BeautifulSoup = get_html_soup(strength_url)
    strength_soup_items: ResultSet = strength_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not strength_soup_items else strength_soup_items[0].get('content')

    strength_strlist: List[str] = content.split()
    strength_strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', strength_strlist))    
    strength: Optional[float] = None if strength_strlist_shortened.__len__() < 3 else readf(strength_strlist_shortened[1])
    return strength






def proxy_guru_strength(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_strength > get_guru_strength"""
    strength: Optional[float] = get_guru_strength(symbol)
    proxy['strength'] = strength
    return proxy




def test():
    stock = input('which stock do you want to check? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_strength(stock, proxy=proxy)
    print(x)
    
if __name__ == '__main__':
    test()