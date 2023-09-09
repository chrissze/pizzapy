"""

USED BY: 
    terminal_scripts/option_operation_script.py, 
    stock_option_update/core_update_controller.py

    
"""

# STANDARD LIBS
import sys; sys.path.append('..')

from multiprocessing import Pool
from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS

# CUSTOM LIBS
from dimsumpy.database.postgres import upsert_psycopg

# PROGRAM MODULES
from stock_option_update.option_proxy_model import make_option_proxy
from database_update.postgres_command_model import table_list_dict
from database_update.postgres_connection_model import make_psycopg_connection





def upsert_option_by_proxy(proxy: DictProxy) -> str:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy(upsert_psycopg), table_list_dict, make_psycopg_connection()
    USED BY: upsert_option()
    
    This function already commits the upsert action. 
    For successful execution, it will return the query string.
    For failed execution, it will return the error message as a string 

    Make sure the DictProxy parameter is valid before running this upsert function.

    upsert_psycopg returns the query_and_values string as a result.
    """
    table_name: str = 'stock_option'
    pk_list: List[str] = table_list_dict[table_name].get('primary_key_list')
    query_result: str = upsert_psycopg(dict=proxy, table=table_name, primary_key_list=pk_list, connection=make_psycopg_connection())
    return query_result



def upsert_option(symbol: str) -> str:
    """
    DEPENDS ON: upsert_option_by_proxy
    IMPORTS: 
    USED BY: upsert_options_by_terminal(), core_stock_update/core_update_controller.py
    I could wrap this function into try_str(upsert_option, symbol).
    """
    proxy: DictProxy = make_option_proxy(symbol)
    valid_data: bool = proxy.get('wealth_pc') is not None

    if valid_data:
        upsert_result: str = upsert_guru_by_proxy(proxy)
        return upsert_result
    else:
        return f'{symbol} DictProxy missed wealth_pc'




def upsert_gurus_by_terminal(symbols: List[str]) -> None:
    """
    DEPENDS ON: upsert_guru

    Since I have used multiprocess process in each upsert_guru call, 
    I might not further used pool.map() or pool.map_async() to speed up.    

    I can add try block by:
        upsert_result: str = try_str(upsert_guru, symbol)

    """
    for symbol in symbols:
        upsert_result: str = upsert_guru(symbol)
        print(upsert_result)



def test_upsert_gurus_by_terminal() -> None:
    start = default_timer()
    xs = ['MCD', 'GS', 'MS']
    upsert_gurus_by_terminal(xs)
    print(default_timer() - start, ' seconds elapsed.')  # 27 seconds
    






if __name__ == '__main__':
    test_upsert_gurus_by_terminal()


