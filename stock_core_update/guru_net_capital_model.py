
# STANDARD LIBRARIES
import sys; sys.path.append('..')
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
import pandas
from pandas.core.frame import DataFrame

import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf

# PROGRAM MODULES
from price_cap_model import get_html_dataframes, proxy_price_cap


def get_guru_net_capital(symbol: str) -> Optional[float]:
    '''net_capital here is (cash equivalent + Receivable * certain percentage + inventory * percentage - total debt)'''
    net_capital_url: str = f'https://www.gurufocus.com/term/NCAV/{symbol}/Net-Net-Working-Capital/'
    net_capital_dfs: List[DataFrame] = get_html_dataframes(net_capital_url)
    # net_capital_value can be str or float64 type
    net_capital_value: Any = '' if len(net_capital_dfs) < 3 or net_capital_dfs[2].empty else net_capital_dfs[2].iloc[-1, -1]
    net_capital: Optional[float] = readf(net_capital_value)
    return net_capital


def tryget_guru_net_capital(symbol: str) -> Optional[float]:
    '''
    DEPENDS: get_guru_net_capital
    '''
    try:
        net_capital: Optional[float] =  get_guru_net_capital(symbol)
        return net_capital
    except requests.exceptions.RequestException as requests_error:
        print('tryget_guru_net_capital RequestException: ', requests_error)
        return None
    except Exception as error:
        print('tryget_guru_net_capital general Exception: ', error)
        return None



def proxy_guru_net_capital(symbol: str, proxy: DictProxy={}) -> DictProxy:
    '''
    DEPENDS: tryget_guru_net_capital > get_guru_net_capital
    tryget_guru_net_capital() can be changed to get_guru_net_capital()
    '''
    net_capital: Optional[float] = tryget_guru_net_capital(symbol)
    proxy['net_capital'] = net_capital if net_capital is not None else None

    net_capital_pc: Optional[float] = None if ('price' not in proxy or net_capital is None) else round((net_capital / proxy['price'] * 100.0), 2)
    proxy['net_capital_pc'] = net_capital_pc if net_capital_pc is not None else None
    return proxy


if __name__ == '__main__':
    
    stock = input('which stock do you want to check net_capital? ')
    proxy = proxy_price_cap(stock)
    x = proxy_guru_net_capital(stock, proxy=proxy)
    print(x)
    
