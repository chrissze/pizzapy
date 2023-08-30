
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
from price_cap_model import get_html_dataframes


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



def tryget_guru_debt_per_share(symbol: str) -> Optional[float]:
    """ DEPENDS: get_guru_debt_per_share"""
    try:
        debt_per_share: Optional[float] =  get_guru_debt_per_share(symbol)
        return debt_per_share
    except requests.exceptions.RequestException as e:
        print('tryget_guru_debt RequestException: ', e)
        return None
    except Exception as e2:
        print('tryget_guru_debt Exception e2: ', e2)
        return None



def proxy_guru_debt(symbol: str, d: DictProxy={}) -> DictProxy:
    '''DEPENDS: tryget_guru_debt_per_share > get_guru_debt_per_share'''
    debt_per_share: Optional[float]  = tryget_guru_debt_per_share(symbol)
    debtpc: Optional[float] = None if ('price' not in d or debt_per_share is None) else round((debt_per_share / d['price'] * 100.0), 2)

    if debt_per_share is not None:
        d['debt_per_share'] = debt_per_share

    if debtpc is not None:
        d['debtpc'] = debtpc

    return d




if __name__ == '__main__':
    
    stock = input('which stock do you want to check? ')
    x = get_guru_debt_per_share(stock)
    print(x)
    
