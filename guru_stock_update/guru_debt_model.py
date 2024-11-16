
# STANDARD LIBRARIES

import json
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from pandas.core.frame import DataFrame

import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf

from dimsumpy.web.crawler import get_html_dataframes

# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy


def get_guru_debt_per_share(symbol: str) -> Optional[float]:

    """ 
    REQUIRES: pandas

    TTWO debt is 0.00 with tables, ttwo's debt is really 0.00
        USO is None
    
        https://www.gurufocus.com/term/total-debt-per-share/NVDA

    """
    debt_url: str = f'https://www.gurufocus.com/term/total-debt-per-share/{symbol}'

    debt_dfs: List[DataFrame] = get_html_dataframes(debt_url)

    debt_str: Any = '' if len(debt_dfs) < 3 or debt_dfs[1].empty else debt_dfs[1].iloc[-1, -1] # can be str or float64 type

    debt_per_share: Optional[float] = readf(debt_str)

    return debt_per_share




def proxy_guru_debt(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS: try_get_guru_debt_per_share > get_guru_debt_per_share
    try_get_guru_debt_per_share() can be changed to get_guru_debt_per_share()
    """
    debt_per_share: Optional[float]  = get_guru_debt_per_share(symbol)
    proxy['debt_per_share'] = debt_per_share

    debt_pc: Optional[float] = round((debt_per_share / proxy['price'] * 100.0), 2) if (proxy.get('price') and debt_per_share) else None
    proxy['debt_pc'] = debt_pc
    return proxy




def test() -> None:
    
    stock = input('which stock do you want to check? ')
    x = get_guru_debt_per_share(stock)
    print(x)
    


if __name__ == '__main__':
    
    test()