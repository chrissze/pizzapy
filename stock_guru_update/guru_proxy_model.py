# STANDARD LIBS
import sys; sys.path.append('..')

from typing import Any, List, Optional, Tuple, Union
from timeit import default_timer
from multiprocessing.managers import DictProxy, SyncManager
from multiprocessing import Manager, Process
from datetime import datetime


# THIRD PARTY LIBS

# CUSTOM LIBS
from batterypy.time.cal import get_trading_day_utc


# PROGRAM MODULES
from stock_general_update.price_cap_model import proxy_price_cap
from guru_book_value_model import proxy_guru_book_value   # dataframes
from guru_debt_model import proxy_guru_debt   # dataframes
from guru_earn_model import proxy_guru_earn
from guru_interest_model import proxy_guru_interest
from guru_lynch_model import proxy_guru_lynch
from guru_net_capital_model import proxy_guru_net_capital   # dataframes
from guru_research_model import proxy_guru_research
from guru_revenue_model import proxy_guru_revenue, proxy_guru_revenue_growths
from guru_strength_model import proxy_guru_strength
from guru_zscore_model import proxy_guru_zscore




def proxy_guru_process(symbol: str) -> DictProxy:
    '''
    DEPENDS: get_trading_day_utc, proxy_price_cap, proxy_guru_book_value TO proxy_guru_zscore
    '''
    SYMBOL: str = symbol.upper()
    manager: SyncManager = Manager()
    proxy: DictProxy = manager.dict()

    proxy['symbol'] = SYMBOL
    proxy['td'] = get_trading_day_utc()
    proxy['t'] = datetime.now().replace(microsecond=0)
    try:
        proxy_price_cap(SYMBOL, proxy)
        p1 = Process(target=proxy_guru_book_value, args=(SYMBOL, proxy))
        p2 = Process(target=proxy_guru_debt, args=(SYMBOL, proxy))
        p3 = Process(target=proxy_guru_earn, args=(SYMBOL, proxy))
        p4 = Process(target=proxy_guru_interest, args=(SYMBOL, proxy))
        p5 = Process(target=proxy_guru_net_capital, args=(SYMBOL, proxy))
        p6 = Process(target=proxy_guru_lynch, args=(SYMBOL, proxy))
        p7 = Process(target=proxy_guru_research, args=(SYMBOL, proxy))
        p8 = Process(target=proxy_guru_revenue, args=(SYMBOL, proxy))
        p9 = Process(target=proxy_guru_revenue_growths, args=(SYMBOL, proxy))
        p10 = Process(target=proxy_guru_strength, args=(SYMBOL, proxy))
        p11 = Process(target=proxy_guru_zscore, args=(SYMBOL, proxy))

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
        return proxy
    
    except Exception as error:
        print(f'{symbol} proxy_guru error: ', error)
        return {}
    finally:  # To make sure processes are closed in the end, even if errors happen
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



def get_guru_wealth_pc(proxy: DictProxy) -> Optional[float]:
    '''
    wealth_pc is the sum of NET CAPITAL + TANGIBLE BOOK VALUE + NEXT 5 YEARS EARNINGS, in percentage of market capitalization.
    '''
    wealth_keys: List[str] = ['cap', 'price', 'earn_pc', 'net_capital_pc', 'book_value_pc']
    valid_keys: bool = all(key in proxy for key in wealth_keys)    
    valid_values: bool = all(value is not None for key, value in proxy.items() if key in wealth_keys) if valid_keys else False
    wealth_pc: Optional[float] = round((proxy['earn_pc'] * 5.0 + proxy['net_capital_pc'] + proxy['book_value_pc']), 2) if valid_values else None
    return wealth_pc


def proxy_guru_wealth(symbol: str) -> DictProxy:
    '''
    DEPENDS: proxy_guru_process, get_guru_wealth_pc
    '''
    proxy: DictProxy = proxy_guru_process(symbol)
    wealth_pc: Optional[float] = get_guru_wealth_pc(proxy)
    proxy['wealth_pc'] = wealth_pc if wealth_pc is not None else None
    return proxy










if __name__ == '__main__':

    stock = input('which stock do you want to check? ')
    
    x = proxy_guru_wealth(stock)
    
    print(x)

