
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


def get_guru_net_capital(symbol: str) -> Optional[float]:
    """
    net_capital here is (cash equivalent + Receivable * certain percentage + inventory * percentage - total debt)
    
    https://www.gurufocus.com/term/net-net-working-capital/NVDA
    """
    
    net_capital_url: str = f'https://www.gurufocus.com/term/net-net-working-capital/{symbol}'
    
    net_capital_dfs: List[DataFrame] = get_html_dataframes(net_capital_url)
    
    # net_capital_value can be str or float64 type
    net_capital_value: Any = '' if len(net_capital_dfs) < 3 or net_capital_dfs[1].empty else net_capital_dfs[1].iloc[-1, -1]
    
    net_capital: Optional[float] = readf(net_capital_value)
    
    return net_capital




def proxy_guru_net_capital(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS: try_get_guru_net_capital > get_guru_net_capital
    try_get_guru_net_capital() can be changed to get_guru_net_capital()
    """
    net_capital: Optional[float] = get_guru_net_capital(symbol)
    proxy['net_capital'] = net_capital

    net_capital_pc: Optional[float] = round((net_capital / proxy['price'] * 100.0), 2) if (proxy.get('price') and net_capital) else None
    proxy['net_capital_pc'] = net_capital_pc
    return proxy


def test():
    
    stock = input('which stock do you want to check net_capital? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_net_capital(stock, proxy=proxy)
    print(x)
    
if __name__ == '__main__':
    test()