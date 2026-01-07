

# STANDARD LIBS


from multiprocessing.managers import DictProxy

from typing import Any, List, Optional, Tuple, Union


# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy, initialize_proxy
from pizzapy.stock_option_update.option_money_model import proxy_option_money



def make_option_proxy(symbol: str) -> DictProxy:
    """
        IMPORTS: initialize_proxy(), make_price_cap_proxy(), proxy_option_money()
    """
    proxy: DictProxy = initialize_proxy(symbol)
    make_price_cap_proxy(symbol, proxy)
    proxy_option_money(symbol, proxy)
    return proxy



def test_make_option_proxy() -> None:
    symbol = input('What SYMBOL do you want to input? ')
    
    option_proxy: DictProxy = make_option_proxy(symbol)
    print(option_proxy)    



if __name__ == '__main__':
    test_make_option_proxy()