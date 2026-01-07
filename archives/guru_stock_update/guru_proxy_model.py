# STANDARD LIBS


from typing import Any, List, Optional, Tuple, Union
from timeit import default_timer
from multiprocessing.managers import DictProxy, SyncManager
from multiprocessing import Manager, Process
from datetime import datetime


# THIRD PARTY LIBS

# CUSTOM LIBS
from batterypy.time.cal import get_trading_day_utc


# PROGRAM MODULES
from pizzapy.general_update.general_model import initialize_proxy, make_price_cap_proxy
from pizzapy.guru_stock_update.guru_book_value_model import proxy_guru_book_value   # dataframes
from pizzapy.guru_stock_update.guru_debt_model import proxy_guru_debt   # dataframes
from pizzapy.guru_stock_update.guru_earn_model import proxy_guru_earn
from pizzapy.guru_stock_update.guru_equity_model import proxy_guru_equity
from pizzapy.guru_stock_update.guru_interest_model import proxy_guru_interest
from pizzapy.guru_stock_update.guru_lynch_model import proxy_guru_lynch
from pizzapy.guru_stock_update.guru_net_capital_model import proxy_guru_net_capital   # dataframes
from pizzapy.guru_stock_update.guru_net_margin_model import proxy_guru_net_margin   # dataframes
from pizzapy.guru_stock_update.guru_research_model import proxy_guru_research
from pizzapy.guru_stock_update.guru_revenue_model import proxy_guru_revenue, proxy_guru_revenue_growths
from pizzapy.guru_stock_update.guru_strength_model import proxy_guru_strength
from pizzapy.guru_stock_update.guru_zscore_model import proxy_guru_zscore




def process_guru(SYMBOL: str) -> DictProxy:
    """
    IMPORTS: initialize_proxy(), make_price_cap_proxy(), proxy_guru_book_value() TO proxy_guru_zscore()
    """
    proxy: DictProxy = initialize_proxy(SYMBOL)
    make_price_cap_proxy(SYMBOL, proxy)
    p1 = Process(target=proxy_guru_book_value, args=(SYMBOL, proxy))
    p2 = Process(target=proxy_guru_debt, args=(SYMBOL, proxy))
    p3 = Process(target=proxy_guru_earn, args=(SYMBOL, proxy))
    p4 = Process(target=proxy_guru_equity, args=(SYMBOL, proxy))
    p5 = Process(target=proxy_guru_interest, args=(SYMBOL, proxy))
    p6 = Process(target=proxy_guru_net_capital, args=(SYMBOL, proxy))
    p7 = Process(target=proxy_guru_net_margin, args=(SYMBOL, proxy))
    p8 = Process(target=proxy_guru_lynch, args=(SYMBOL, proxy))
    p9 = Process(target=proxy_guru_research, args=(SYMBOL, proxy))
    p10 = Process(target=proxy_guru_revenue, args=(SYMBOL, proxy))
    p11 = Process(target=proxy_guru_revenue_growths, args=(SYMBOL, proxy))
    p12 = Process(target=proxy_guru_strength, args=(SYMBOL, proxy))
    p13 = Process(target=proxy_guru_zscore, args=(SYMBOL, proxy))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()
    p11.start()
    p12.start()
    p13.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()
    p11.join()
    p12.join()
    p13.join()
    
    p1.close()
    p2.close()
    p3.close()
    p4.close()
    p5.close()
    p6.close()
    p7.close()
    p8.close()
    p9.close()
    p10.close()
    p11.close()
    p12.close()
    p13.close()
    return proxy



def get_guru_wealth_pc(proxy: DictProxy) -> Optional[float]:
    """
    wealth_pc is the sum of NET CAPITAL + TANGIBLE BOOK VALUE + NEXT 5 YEARS EARNINGS, in percentage of market capitalization.
    """
    wealth_keys: List[str] = ['cap', 'price', 'earn_pc', 'net_capital_pc', 'book_value_pc']
    valid_keys: bool = all(key in proxy for key in wealth_keys)    
    valid_values: bool = all(value is not None for key, value in proxy.items() if key in wealth_keys) if valid_keys else False
    wealth_pc: Optional[float] = round((proxy['earn_pc'] * 5.0 + proxy['net_capital_pc'] + proxy['book_value_pc']), 2) if valid_values else None
    return wealth_pc


def make_guru_proxy(symbol: str) -> DictProxy:
    """
    DEPENDS: process_guru(), get_guru_wealth_pc()
    """
    proxy: DictProxy = process_guru(symbol)
    wealth_pc: Optional[float] = get_guru_wealth_pc(proxy)
    proxy['wealth_pc'] = wealth_pc
    return proxy




def test():
    stock = input('which stock do you want to check? ')
    
    x = make_guru_proxy(stock)
    
    print(x)


if __name__ == '__main__':
    test()