
# STANDARD LIBRARIES
import sys; sys.path.append('..')
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
from stock_general_update.price_cap_model import proxy_price_cap




def get_guru_earn_per_share(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: beautifulsoup4
    
    https://www.gurufocus.com/term/eps_nri/NVDA/EPS-without-NRI/
    
    """
    earn_url: str = f'https://www.gurufocus.com/term/eps_nri/{symbol}/EPS-without-NRI/'
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
    proxy['earn_per_share'] = earn_per_share if earn_per_share is not None else None
    
    earn_pc: Optional[float] = None if ('price' not in proxy or earn_per_share is None) else round((earn_per_share / proxy['price'] * 100.0), 2)
    proxy['earn_pc'] = earn_pc if earn_pc is not None else None
    return proxy




if __name__ == '__main__':
    
    stock = input('which stock do you want to check? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_earn(stock, proxy=proxy)
    print(x)
    
