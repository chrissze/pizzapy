'''
    https://www.gurufocus.com/term/rank_balancesheet/NVDA/Financial-Strength/

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
from dimsumpy.web.crawler import get_html_soup

# PROGRAM MODULES
from stock_general_update.price_cap_model import proxy_price_cap


def get_guru_strength(symbol: str) -> Optional[float]:
    '''

    '''
    strength_url: str = f'https://www.gurufocus.com/term/rank_balancesheet/{symbol}/Financial-Strength/'
    strength_soup: BeautifulSoup = get_html_soup(strength_url)
    strength_soup_items: ResultSet = strength_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not strength_soup_items else strength_soup_items[0].get('content')

    strength_strlist: List[str] = content.split()
    strength_strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', strength_strlist))    
    strength: Optional[float] = None if strength_strlist_shortened.__len__() < 3 else readf(strength_strlist_shortened[1])
    return strength



def try_get_guru_strength(symbol: str) -> Optional[float]:
    """ DEPENDS: get_guru_strength"""
    try:
        strength: Optional[float] =  get_guru_strength(symbol)
        return strength
    except requests.exceptions.RequestException as requests_error:
        print('try_get_guru_strength RequestException: ', requests_error)
        return None
    except Exception as error:
        print('try_get_guru_strength general Exception: ', error)
        return None



def proxy_guru_strength(symbol: str, proxy: DictProxy={}) -> DictProxy:
    '''DEPENDS: try_get_guru_strength > get_guru_strength'''
    strength: Optional[float] = get_guru_strength(symbol)
    proxy['strength'] = strength if strength is not None else None
    return proxy




if __name__ == '__main__':
    
    stock = input('which stock do you want to check? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_strength(stock, proxy=proxy)
    print(x)
    
