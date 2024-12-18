
# STANDARD LIBRARIES

import json
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from pandas.core.frame import DataFrame

import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf
from dimsumpy.web.crawler import get_html_soup

# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy




def get_guru_earn_per_share(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: beautifulsoup4

    https://www.gurufocus.com/term/eps-without-nri/NVDA
    
    """
    earn_url: str = f'https://www.gurufocus.com/term/eps-without-nri/{symbol}'
    earn_soup: BeautifulSoup = get_html_soup(earn_url)
    earn_soup_items: ResultSet = earn_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not earn_soup_items else earn_soup_items[0].get('content')
    earn_strlist: List[str] = content.split()
    earn_strlist2: List[str] = list(filter(lambda x: '$' in x, earn_strlist))
    earn_per_share: Optional[float] = readf(earn_strlist2[0][:-1]) if earn_strlist2 else None
    return earn_per_share




def proxy_guru_earn(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_earn_per_share > get_guru_earn_per_share"""
    earn_per_share: Optional[float]  = get_guru_earn_per_share(symbol)
    proxy['earn_per_share'] = earn_per_share
    
    earn_pc: Optional[float] = round((earn_per_share / proxy['price'] * 100.0), 2) if (proxy.get('price') and earn_per_share) else None
    proxy['earn_pc'] = earn_pc 
    return proxy




def test():
    
    stock = input('which stock do you want to check? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_earn(stock, proxy=proxy)
    print(x)
    


if __name__ == '__main__':
    test()