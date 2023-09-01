
'''

https://www.gurufocus.com/term/RD/INTC/Research-&-Development


'''


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

# PROGRAM MODULES
from price_cap_model import get_html_soup, proxy_price_cap



def get_guru_research(symbol: str) -> Optional[float]:
    '''
    Research & Development expense
    '''
    research_url: str = f'https://www.gurufocus.com/term/RD/{symbol}/Research-&-Development/'
    research_soup: BeautifulSoup = get_html_soup(research_url)
    research_soup_items: ResultSet = research_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not research_soup_items else research_soup_items[0].get('content')
    strlist: List[str] = content.split()
    #print(strlist)
    short_strlist: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
    research_in_million: Optional[float] = None if len(short_strlist) < 3 else readf(short_strlist[1])
    research: Optional[float] = None if research_in_million is None else research_in_million * 1000000
    return research


def try_get_guru_research(symbol: str) -> Optional[float]:
    """ DEPENDS: get_guru_research"""
    try:
        research: Optional[float] =  get_guru_research(symbol)
        return research
    except requests.exceptions.RequestException as requests_error:
        print('try_get_guru_research RequestException: ', requests_error)
        return None
    except Exception as error:
        print('try_get_guru_research general Exception: ', error)
        return None



def proxy_guru_research(symbol: str, proxy: DictProxy={}) -> DictProxy:
    '''DEPENDS: try_get_guru_research > get_guru_research'''
    research: Optional[float] = try_get_guru_research(symbol)
    proxy['research'] = research if research is not None else None
    
    research_pc: Optional[float] = None if ('cap' not in proxy or research is None) else round((research / proxy['cap'] * 100.0), 2)
    proxy['research_pc'] = research_pc if research_pc is not None else None
    return proxy




if __name__ == '__main__':
    stock = input('which stock do you want to check research? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_research(stock, proxy=proxy)
    print(x)
    
