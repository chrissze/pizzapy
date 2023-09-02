
'''
When Altman Z-Score is LESS THAN 1.8, it is in Distress Zones.
When Altman Z-Score is between 1.8 and 3, it is in Grey Zones.
When Altman Z-Score GREATER THAN 3, it is in Safe Zones.

https://www.gurufocus.com/term/zscore/NVDA/Altman-Z-Score/

Morgan Stanley zscore is None, need further investigate


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



def get_guru_zscore(symbol: str) -> Optional[float]:
    '''

    Morgan Stanley zscore is None, need further investigate
    '''
    zscore_url: str = f'https://www.gurufocus.com/term/zscore/{symbol}/Altman-Z-Score/'
    zscore_soup: BeautifulSoup = get_html_soup(zscore_url)
    zscore_soup_items: ResultSet = zscore_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not zscore_soup_items else zscore_soup_items[0].get('content')
    strlist: List[str] = content.split()
    short_strlist: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
    zscore: Optional[float] = None if len(short_strlist) < 3 else readf(short_strlist[1])
    return zscore





def proxy_guru_zscore(symbol: str, proxy: DictProxy={}) -> DictProxy:
    '''DEPENDS: try_get_guru_zscore > get_guru_zscore'''
    zscore: Optional[float] = get_guru_zscore(symbol)
    proxy['zscore'] = zscore if zscore is not None else None
    return proxy




if __name__ == '__main__':
    stock = input('which stock do you want to check zscore? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_zscore(stock, proxy=proxy)
    print(x)
    
