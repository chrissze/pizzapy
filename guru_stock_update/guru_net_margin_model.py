
# STANDARD LIBRARIES

from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
import pandas
from pandas.core.frame import DataFrame

import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf
from dimsumpy.web.crawler import get_html_dataframes

# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy


def get_guru_net_margin(symbol: str) -> Optional[float]:
    """
    
    https://www.gurufocus.com/term/net-margin/MSFT
    https://www.gurufocus.com/term/net-margin/NVDA
    """
    
    net_margin_url: str = f'https://www.gurufocus.com/term/net-margin/{symbol}'
    
    net_margin_dfs: List[DataFrame] = get_html_dataframes(net_margin_url)
    
    # net_margin_value can be str or float64 type
    net_margin_value: Any = '' if len(net_margin_dfs) < 3 or net_margin_dfs[1].empty else net_margin_dfs[1].iloc[-1, -1]
    
    net_margin: Optional[float] = readf(net_margin_value)
    
    return net_margin




def proxy_guru_net_margin(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS: get_guru_net_margin
    """
    net_margin: Optional[float] = get_guru_net_margin(symbol)
    proxy['net_margin'] = net_margin
    return proxy


def test1():
    
    stock = input('which stock do you want to check net_margin? ')
    
    x = get_guru_net_margin(stock)
    print(x)
    
def test2():
    
    stock = input('which stock do you want to check net_margin? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_net_margin(stock, proxy=proxy)
    print(x)
    


if __name__ == '__main__':
    test1()