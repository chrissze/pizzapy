
"""
NVIDA has 1, 3, 5, 10 years average growth rates. 
https://www.gurufocus.com/term/per+share+rev/NVDA/Revenue-per-Share/

COINBASE has only 1 and 3 years average grow rates (last update: 2023)
https://www.gurufocus.com/term/per+share+rev/COIN/Revenue-per-Share/

"""


# STANDARD LIBRARIES

from itertools import dropwhile
from multiprocessing.managers import DictProxy
import re
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf
from dimsumpy.web.crawler import get_html_soup, get_html_text

# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy


def get_guru_revenue_per_share(symbol: str) -> Optional[float]:
    """
    returns Revenue Per Share

    https://www.gurufocus.com/term/revenue-per-share/NVDA
    """
    revenue_url: str = f'https://www.gurufocus.com/term/revenue-per-share/{symbol}'
    revenue_soup: BeautifulSoup = get_html_soup(revenue_url)
    soup_items: ResultSet = revenue_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')
    strlist: List[str] = content.split()
    short_strlist: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
    revenue_per_share: Optional[float] = None if len(short_strlist) < 3 else readf(short_strlist[1])
    return revenue_per_share




def proxy_guru_revenue(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS: try_get_guru_revenue > get_guru_revenue
    
    """
    revenue_per_share: Optional[float] = get_guru_revenue_per_share(symbol)   
    proxy['revenue_per_share'] = revenue_per_share
    
    revenue_pc: Optional[float] = round((revenue_per_share / proxy['price'] * 100.0), 2) if (proxy.get('price') and revenue_per_share) else None
    proxy['revenue_pc'] = revenue_pc
    return proxy


def get_guru_revenue_growths(symbol: str) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """    
    returns Revenue Growths in years
    """
    revenue_url: str = f'https://www.gurufocus.com/term/revenue-per-share/{symbol}'
    html_text: str = get_html_text(revenue_url)
    # the + sign matches multiple occurrence of the same character, such as <<, >>, %%%, commonly use when there are spaces.
    # strlist is the result of spliting a whole page of html text.
    strlist: List[str] = re.split('[<>%]+', html_text)
    short_strlist: List[str] = list(dropwhile(lambda x: x != 'past 12 months', strlist))
    tiny_strlist: List[str] = short_strlist[:40]
    
    # growth strings of 1,3,5,10 years, some stocks such as COIN has fewer years of data.
    # filter out those words cannot be converted to numbers. 
    # growth_list (NVDA): ['11.70', '34.50', '25.70', '22.00']
    growth_list: list[str] = list(filter(lambda x: readf(x), tiny_strlist)) 
    rev_growth_1y: Optional[float] = None if len(growth_list) < 1 else readf(growth_list[0])
    rev_growth_3y: Optional[float] = None if len(growth_list) < 2 else readf(growth_list[1])
    rev_growth_5y: Optional[float] = None if len(growth_list) < 3 else readf(growth_list[2])
    rev_growth_10y: Optional[float] = None if len(growth_list) < 4 else readf(growth_list[3])

    return rev_growth_1y, rev_growth_3y, rev_growth_5y, rev_growth_10y




def proxy_guru_revenue_growths(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_revenue_growths"""
    rev_growth_1y, rev_growth_3y, rev_growth_5y, rev_growth_10y = get_guru_revenue_growths(symbol)
    proxy['rev_growth_1y'] = rev_growth_1y
    proxy['rev_growth_3y'] = rev_growth_3y
    proxy['rev_growth_5y'] = rev_growth_5y
    proxy['rev_growth_10y'] = rev_growth_10y
    return proxy


def test():
    stock = input('which stock do you want to check revenue? ')
    proxy = make_price_cap_proxy(stock)
    proxy2 = proxy_guru_revenue(stock, proxy=proxy)
    proxy3 = proxy_guru_revenue_growths(stock, proxy=proxy2)
    print(proxy3)
    
if __name__ == '__main__':
    test()