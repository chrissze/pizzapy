# STANDARD LIBS
import sys; sys.path.append('..')

from multiprocessing import Pool
from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS

# CUSTOM LIBS
from batterypy.control.trys import try_str
from dimsumpy.database.postgres import upsert_psycopg, execute_psycopg

# PROGRAM MODULES
from guru_proxy_model import proxy_guru_wealth
from database_update.postgres_command_model import db_table_command_dict
from database_update.postgres_connection_model import make_psycopg_connection





def upsert_guru_proxy(proxy: DictProxy) -> str:
    '''
    * INDEPENDENT *
    IMPORTS: dimsumpy(upsert_dict), db_table_command_dict, make_psycopg_connection()
    USED BY: upsert_guru()
    
    Make sure the DictProxy parameter is valid before running this upsert function.

    upsert_psycopg returns the query_and_values string.
    '''
    pk_list: List[str] = db_table_command_dict['stock_guru'].get('pk')
    query_and_values: str = upsert_psycopg(dict=proxy, table='stock_guru', primary_key_list=pk_list, connection=make_psycopg_connection())
    return query_and_values


def upsert_guru(symbol: str) -> str:
    '''
    DEPENDS ON: upsert_guru_proxy
    IMPORTS: proxy_guru_wealth()

    I could wrap this function into try_str(upsert, symbol).
    '''
    proxy: DictProxy = proxy_guru_wealth(symbol)
    valid_data: bool = proxy.get('wealth_pc') is not None

    if valid_data:
        query_and_values: str = upsert_guru_proxy(proxy)
        return query_and_values
    else:
        return f'{symbol} ProxyDict missed wealth_pc'




def upsert_gurus(symbols: List[str]) -> None:
    '''
    DEPENDS ON: upsert_guru

    Since I have used multiprocess process in each upsert_guru call, 
    I might not further used pool.map() or pool.map_async() to speed up.    
    '''
    for symbol in symbols:
        s = upsert_guru(symbol)
        print(s)


def try_upsert_gurus(symbols: List[str]) -> None:
    '''
    DEPENDS ON: upsert_guru
    IMPORTS: batterypy(try_str)
    '''
    for symbol in symbols:
        s = try_str(upsert_guru, symbol)
        print(s)



def test_upsert_gurus() -> None:
    start = default_timer()
    xs = ['MCD', 'GS', 'MS']
    try_upsert_gurus(xs)
    print(default_timer() - start, ' seconds elapsed.')  # 27 seconds
    






if __name__ == '__main__':
    test_upsert_gurus()


