
"""
When Altman Z-Score is LESS THAN 1.8, it is in Distress Zones.
When Altman Z-Score is between 1.8 and 3, it is in Grey Zones.
When Altman Z-Score GREATER THAN 3, it is in Safe Zones.

Morgan Stanley zscore is None, because guru website states that
Altman Z-Score does not apply to banks and insurance companies.

https://www.gurufocus.com/term/zscore/NVDA

"""


# STANDARD LIBRARIES

from itertools import dropwhile
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pandas.core.frame import DataFrame
import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf
from dimsumpy.web.crawler import get_html_dataframes
#from dimsumpy.web.crawler import get_html_soup

# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy



def get_guru_zscore(symbol: str) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """

    https://www.gurufocus.com/term/zscore/NVDA

    https://www.gurufocus.com/term/zscore/WBD

    iloc first value -1 means the last row
    iloc second value -1 means the last column

    
    ALTERNATIVE: Use beautifulsoup to get zscore:

        zscore_soup: BeautifulSoup = get_html_soup(zscore_url)
        zscore_soup_items: ResultSet = zscore_soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not zscore_soup_items else zscore_soup_items[0].get('content')
        strlist: List[str] = content.split()
        short_strlist: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
        zscore: Optional[float] = None if len(short_strlist) < 3 else readf(short_strlist[1])
        
    """
    zscore_url: str = f'https://www.gurufocus.com/term/zscore/{symbol}'
    
    dfs: List[DataFrame] = get_html_dataframes(zscore_url)
    
    not_valid: bool = len(dfs) < 8



    x1_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[3].iloc[-1, 2] 
    x1: Optional[float] = readf(x1_str)
    
    x2_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[4].iloc[-1, 2] 
    x2: Optional[float] = readf(x2_str)
    
    x3_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[5].iloc[-1, 2] 
    x3: Optional[float] = readf(x3_str)
    
    x4_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[6].iloc[-1, 2] 
    x4: Optional[float] = readf(x4_str)
    
    x5_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[7].iloc[-1, 2] 
    x5: Optional[float] = readf(x5_str)
    
    zscore_str: Any = '' if not_valid else dfs[2].iloc[-1, 2] 
    zscore: Optional[float] = readf(zscore_str)
        
    year1z_str: Any = '' if not_valid else dfs[0].iloc[-1, -1] 
    year1z: Optional[float] = readf(year1z_str)
    
    year2z_str: Any = '' if not_valid else dfs[0].iloc[-1, -2] 
    year2z: Optional[float] = readf(year2z_str)
    
    year3z_str: Any = '' if not_valid else dfs[0].iloc[-1, -3] 
    year3z: Optional[float] = readf(year3z_str)
    

    return x1, x2, x3, x4, x5, zscore, year1z, year2z, year3z





def proxy_guru_zscore(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS ON: get_guru_zscore"""
    x1, x2, x3, x4, x5, zscore, year1z, year2z, year3z = get_guru_zscore(symbol)

    z1 = round(x1 * 1.2, 2) if x1 else None
    z2 = round(x2 * 1.4, 2) if x2 else None
    z3 = round(x3 * 3.3, 2) if x3 else None
    z4 = round(x4 * 0.6, 2) if x4 else None
    z5 = round(x5 * 1.0, 2) if x5 else None

    nocapz = round(zscore - z4, 2)  if z4 and zscore else None

    proxy['x1'] = x1
    proxy['x2'] = x2
    proxy['x3'] = x3
    proxy['x4'] = x4
    proxy['x5'] = x5
    

    proxy['z1'] = z1
    proxy['z2'] = z2
    proxy['z3'] = z3
    proxy['z4'] = z4
    proxy['z5'] = z5

    proxy['zscore'] = zscore
    proxy['nocapz'] = nocapz

    proxy['year1z'] = year1z
    proxy['year2z'] = year2z
    proxy['year3z'] = year3z

    return proxy



def test1():
    stock = input('which stock do you want to check zscore? ')
    x = get_guru_zscore(stock)
    
    print(x)
    
def test2():
    stock = input('which stock do you want to check zscore? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_zscore(stock, proxy=proxy)
    print(x)
    
if __name__ == '__main__':
    test2()