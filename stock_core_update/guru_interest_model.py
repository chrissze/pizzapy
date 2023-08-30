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
from price_cap_model import get_html_soup




def get_guru_interest(symbol: str) -> Optional[float]:
    '''    '''
    interest_url: str = f'https://www.gurufocus.com/term/InterestExpense/{symbol}/Interest-Expense/'
    interest_soup: BeautifulSoup = get_html_soup(interest_url)
    interest_soup_items: ResultSet = interest_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not interest_soup_items else interest_soup_items[0].get('content')
    interest_strlist: List[str] = content.split()
    interest_strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', interest_strlist))    

    negative_interest_in_million: Optional[float] = None if len(interest_strlist_shortened) < 3 else readf(interest_strlist_shortened[1])
    interest: Optional[float] = None if negative_interest_in_million is None else abs(negative_interest_in_million) * 1000000.0
    return interest



def tryget_guru_interest(symbol: str) -> Optional[float]:
    """ DEPENDS: get_guru_interest"""
    try:
        interest: Optional[float] =  get_guru_interest(symbol)
        return interest
    except requests.exceptions.RequestException as requests_error:
        print('tryget_guru_interest RequestException: ', requests_error)
        return None
    except Exception as error:
        print('tryget_guru_interest general Exception: ', error)
        return None



def proxy_guru_interest(symbol: str, d: DictProxy={}) -> DictProxy:
    '''DEPENDS: tryget_guru_interest > get_guru_interest'''
    interest: Optional[float]  = tryget_guru_interest(symbol)
    if interest is not None:
        d['interest'] = interest

    interestpc: Optional[float] = None if ('cap' not in d or interest is None) \
        else round((interest / d['cap'] * 100.0), 4)
    
    if interestpc is not None:
            d['interestpc'] = interestpc
    return d


if __name__ == '__main__':
    
    stock = input('which stock do you want to check interest? ')
    x = proxy_guru_interest(stock)
    print(x)
    
