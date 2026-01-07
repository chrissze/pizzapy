"""

USED BY: 
    terminal_scripts/option_operation_script.py, 
    core_stock_update/core_update_controller.py

    
"""

# STANDARD LIBS


from multiprocessing import Pool
from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS

# CUSTOM LIBS

from dimsumpy.database.postgres import upsert_psycopg


# PROGRAM MODULES
from pizzapy.stock_option_update.option_proxy_model import make_option_proxy
from pizzapy.database_update.postgres_command_model import table_list_dict
from pizzapy.database_update.postgres_connection_model import make_psycopg_connection





def upsert_option_by_proxy(proxy: DictProxy) -> str:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy(upsert_psycopg), table_list_dict, make_psycopg_connection()
    USED BY: upsert_option()
    
    This function will not test whether the input DictProxy contains valid data, 
    I will use upsert_option to validate the proxy and call this function.

    This function commits the upsert action. 
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
    DEPENDS ON: upsert_option_by_proxy()
    IMPORTS: make_option_proxy()
    USED BY: upsert_symbols_terminal(), core_stock_update/core_update_controller.py
    I could wrap this function into try_str(upsert_option, symbol).
    """
    SYMBOL: str = symbol.upper()
    proxy: DictProxy = make_option_proxy(SYMBOL)
    valid_data: bool = proxy.get('call_pc') is not None

    if valid_data:
        upsert_result: str = upsert_option_by_proxy(proxy)
        return f'{SYMBOL} {proxy} {upsert_result}'
    else:
        return f'{symbol} {proxy} DictProxy data does not have call_pc, it is invalid'





def test() -> None:
    symbol = 'NVDA'
    x = upsert_option(symbol)    
    print(x)

if __name__ == '__main__':
    test()


