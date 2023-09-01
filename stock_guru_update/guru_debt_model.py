
# STANDARD LIBRARIES
import sys; sys.path.append('..')
import json
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from pandas.core.frame import DataFrame

import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf

# PROGRAM MODULES
from price_cap_model import get_html_dataframes, proxy_price_cap


def get_guru_debt_per_share(symbol: str) -> Optional[float]:

    ''' 
    REQUIRES: pandas

    TTWO debt is 0.00 with tables, ttwo's debt is really 0.00
        USO is None
    
        https://www.gurufocus.com/term/Total_Debt_Per_Share/nvda/Total-Debt-per-Share
        will divert to
        https://www.gurufocus.com/term/Total_Debt_Per_Share/NVDA/Total-Debt-per-Share/NVDA

    '''
    debt_url: str = f'https://www.gurufocus.com/term/Total_Debt_Per_Share/{symbol}/Total-Debt-per-Share'
    debt_dfs: List[DataFrame] = get_html_dataframes(debt_url)
    debt_str: Any = '' if len(debt_dfs) < 3 or debt_dfs[2].empty else debt_dfs[2].iloc[-1, -1] # can be str or float64 type
    debt_per_share: Optional[float] = readf(debt_str)
    return debt_per_share



def try_get_guru_debt_per_share(symbol: str) -> Optional[float]:
    """ DEPENDS: get_guru_debt_per_share"""
    try:
        debt_per_share: Optional[float] =  get_guru_debt_per_share(symbol)
        return debt_per_share
    except requests.exceptions.RequestException as requests_error:
        print('try_get_guru_debt RequestException: ', requests_error)
        return None
    except Exception as error:
        print('try_get_guru_debt general Exception: ', error)
        return None



def proxy_guru_debt(symbol: str, proxy: DictProxy={}) -> DictProxy:
    '''
    DEPENDS: try_get_guru_debt_per_share > get_guru_debt_per_share
    try_get_guru_debt_per_share() can be changed to get_guru_debt_per_share()
    '''
    debt_per_share: Optional[float]  = try_get_guru_debt_per_share(symbol)
    proxy['debt_per_share'] = debt_per_share if debt_per_share is not None else None

    debt_pc: Optional[float] = None if ('price' not in proxy or debt_per_share is None) else round((debt_per_share / proxy['price'] * 100.0), 2)
    proxy['debt_pc'] = debt_pc if debt_pc is not None else None
    return proxy




if __name__ == '__main__':
    
    stock = input('which stock do you want to check? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_debt(stock, proxy=proxy)
    print(x)
    
