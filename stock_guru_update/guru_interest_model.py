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




def get_guru_interest(symbol: str) -> Optional[float]:
    """    """
    interest_url: str = f'https://www.gurufocus.com/term/InterestExpense/{symbol}/Interest-Expense/'
    interest_soup: BeautifulSoup = get_html_soup(interest_url)
    interest_soup_items: ResultSet = interest_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not interest_soup_items else interest_soup_items[0].get('content')
    interest_strlist: List[str] = content.split()
    interest_strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', interest_strlist))    

    negative_interest_in_million: Optional[float] = None if len(interest_strlist_shortened) < 3 else readf(interest_strlist_shortened[1])
    interest: Optional[float] = None if negative_interest_in_million is None else abs(negative_interest_in_million) * 1000000.0
    return interest





def proxy_guru_interest(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_interest > get_guru_interest"""
    interest: Optional[float]  = get_guru_interest(symbol)
    proxy['interest'] = interest if interest is not None else None

    interest_pc: Optional[float] = None if ('cap' not in proxy or interest is None) \
        else round((interest / proxy['cap'] * 100.0), 4)
    proxy['interest_pc'] = interest_pc if interest_pc is not None else None
    return proxy


if __name__ == '__main__':
    
    stock = input('which stock do you want to check interest? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_interest(stock)
    print(x)
    
