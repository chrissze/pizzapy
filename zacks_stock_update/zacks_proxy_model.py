"""

"""
# STANDARD LIBS


from multiprocessing.managers import DictProxy
from typing import Any, List, Optional, Tuple, Union


# PROGRAM MODULES
from pizzapy.general_update.general_model import initialize_proxy
from pizzapy.zacks_stock_update.zacks_earnings_model import proxy_zacks_earnings
from pizzapy.zacks_stock_update.zacks_scores_model import proxy_zacks_scores





def make_zacks_proxy(symbol: str) -> DictProxy:
    """
    IMPORTS: initialize_proxy(), proxy_zacks_earnings(), proxy_zacks_scores()
    USED BY: zacks_update_database_model.py (upsert_zacks)
    
    the symbol will be changed to upper case at upsert_zacks()
    """
    proxy: DictProxy = initialize_proxy(symbol)
    proxy_zacks_earnings(symbol, proxy)
    proxy_zacks_scores(symbol, proxy)
    return proxy




def test() -> None:
    symbol: str = input('What SYMBOL do you want to check? ')
    proxy = make_zacks_proxy(symbol)
    print(proxy)

if __name__ == '__main__':
    test()
