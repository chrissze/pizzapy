# STANDARD LIBRARIES
import sys; sys.path.append('..')
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
from general_update.price_cap_model import proxy_price_cap


def get_guru_lynch(symbol: str) -> Optional[float]:
    """Lynch Value is Peter Lynch's estimation of fair price"""
    lynch_url: str = f'https://www.gurufocus.com/term/lynchvalue/{symbol}/Peter-Lynch-Fair-Value/'
    soup: BeautifulSoup = get_html_soup(lynch_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')
    strlist: List[str] = content.split()
    #print(strlist)
    strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
    lynch: Optional[float] = None if len(strlist_shortened) < 3 else readf(strlist_shortened[1])
    return lynch



def proxy_guru_lynch(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_lynch > get_guru_lynch
    
    lynch is Peter Lynch's fair price.

    lynchmove is the expected movement in percentage, 20.0 means expecting to have 20% price increase; -30 means expecting to have 20% price drop.
    
    try_get_guru_lynch() below can be changed to get_guru_lynch()
    """
    lynch: Optional[float]  = get_guru_lynch(symbol)   
    proxy['lynch'] = lynch if lynch is not None else None

    lynch_move_pc: Optional[float] = None if ('price' not in proxy or lynch is None) \
        else round((lynch - proxy['price']) / proxy['price'] * 100.0, 2)
    proxy['lynch_move_pc'] = lynch_move_pc if lynch_move_pc is not None else None
    return proxy




if __name__ == '__main__':    
    stock = input('which stock do you want to check lynch? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_lynch(stock, proxy=proxy)
    print(x)
    
