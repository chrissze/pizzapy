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


def get_guru_lynch(symbol: str) -> Optional[float]:
    """
    Lynch Value is Peter Lynch's estimation of fair price
    
    https://www.gurufocus.com/term/peter-lynch-fair-value/NVDA
    """

    lynch_url: str = f'https://www.gurufocus.com/term/peter-lynch-fair-value/{symbol}'

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
    proxy['lynch'] = lynch

    lynch_move_pc: Optional[float] = round((lynch - proxy['price']) / proxy['price'] * 100.0, 2) if (proxy.get('price') and lynch) else None
    proxy['lynch_move_pc'] = lynch_move_pc
    return proxy




def test():    
    stock = input('which stock do you want to check lynch? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_lynch(stock, proxy=proxy)
    print(x)
    


if __name__ == '__main__':    
    test()
    
