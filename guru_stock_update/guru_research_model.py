
"""

https://www.gurufocus.com/term/RD/INTC/Research-&-Development


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



def get_guru_research(symbol: str) -> Optional[float]:
    """
    Research & Development expense

    https://www.gurufocus.com/term/research-development/NVDA
    """
    research_url: str = f'https://www.gurufocus.com/term/research-development/{symbol}'
    
    research_soup: BeautifulSoup = get_html_soup(research_url)

    research_soup_items: ResultSet = research_soup.find_all('meta', attrs={'name': 'description'})
    
    content: str = '' if not research_soup_items else research_soup_items[0].get('content')
    
    strlist: List[str] = content.split()
    #print(strlist)

    short_strlist: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
    
    research_in_million: Optional[float] = None if len(short_strlist) < 3 else readf(short_strlist[1])
    
    research: Optional[float] = None if research_in_million is None else research_in_million * 1000000
    
    return research





def proxy_guru_research(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_research > get_guru_research"""
    research: Optional[float] = get_guru_research(symbol)
    proxy['research'] = research
    
    research_pc: Optional[float] = round((research / proxy['cap'] * 100.0), 2) if (proxy.get('cap') and research) else None
    proxy['research_pc'] = research_pc
    return proxy



def test():
    stock = input('which stock do you want to check research? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_research(stock, proxy=proxy)
    print(x)
    
if __name__ == '__main__':
    test()