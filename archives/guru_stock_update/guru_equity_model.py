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




def get_guru_equity(SYMBOL: str) -> Optional[float]:
    """

    https://www.gurufocus.com/term/total-stockholders-equity/NVDA
    """
    equity_url: str = f'https://www.gurufocus.com/term/total-stockholders-equity/{SYMBOL}'
    equity_soup: BeautifulSoup = get_html_soup(equity_url)
    equity_soup_items: ResultSet = equity_soup.find_all('meta', attrs={'name': 'description'})
    
    content: str = equity_soup_items[0].get('content') if equity_soup_items else ''
    equity_strlist: List[str] = content.split()
    equity_strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', equity_strlist))    

    equity_in_million: Optional[float] = None if len(equity_strlist_shortened) < 3 else readf(equity_strlist_shortened[1])
    equity: Optional[float] = None if equity_in_million is None else abs(equity_in_million) * 1000000.0
    equity: Optional[float] = equity_in_million * 1000000.0 if equity_in_million else None
    return equity





def proxy_guru_equity(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_equity > get_guru_equity"""
    equity: Optional[float]  = get_guru_equity(symbol)
    proxy['equity'] = equity
    equity_pc: Optional[float] = round((equity / proxy['cap'] * 100.0), 4) if proxy.get('cap') and equity else None
    proxy['equity_pc'] = equity_pc
    return proxy


def test():
    
    stock = input('which stock do you want to check equity? ')
    proxy = make_price_cap_proxy(stock)
    print(proxy)
    x = proxy_guru_equity(stock, proxy)
    print(x)
    

if __name__ == '__main__':
    test()