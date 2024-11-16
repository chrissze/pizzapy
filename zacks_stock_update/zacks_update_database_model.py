"""

USED BY: 
    terminal_scripts/zacks_operation_script.py, 
    core_stock_update/core_update_controller.py

    
"""

# STANDARD LIBS


from multiprocessing import Pool
from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS

# CUSTOM LIBS
from batterypy.control.trys import try_str
from dimsumpy.database.postgres import upsert_psycopg


# PROGRAM MODULES
from pizzapy.zacks_stock_update.zacks_proxy_model import make_zacks_proxy
from pizzapy.database_update.postgres_command_model import table_list_dict
from pizzapy.database_update.postgres_connection_model import make_psycopg_connection





def upsert_zacks_by_proxy(proxy: DictProxy) -> str:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy(upsert_psycopg), table_list_dict, make_psycopg_connection()
    USED BY: upsert_zacks()
    
    This function will not test whether the input DictProxy contains valid data, 
    I will use upsert_zacks to validate the proxy and call this function.

    This function commits the upsert action. 
    For successful execution, it will return the query string.
    For failed execution, it will return the error message as a string 

    Make sure the DictProxy parameter is valid before running this upsert function.

    upsert_psycopg returns the query_and_values string as a result.
    """
    table_name: str = 'zacks_stock'
    pk_list: List[str] = table_list_dict[table_name].get('primary_key_list')
    query_result: str = upsert_psycopg(dict=proxy, table=table_name, primary_key_list=pk_list, connection=make_psycopg_connection())
    return query_result



def upsert_zacks(symbol: str) -> str:
    """
    DEPENDS ON: upsert_zacks_by_proxy()
    IMPORTS: make_zacks_proxy()
    USED BY: upsert_symbols_terminal(), core_stock_update/core_update_controller.py
    I could wrap this function into try_str(upsert_zacks, symbol).
    
    print('THE PROXY IS: ')
    print(proxy, '\n\n\n\n')
    """
    SYMBOL: str = symbol.upper()
    proxy: DictProxy = make_zacks_proxy(SYMBOL)
    
    valid_data: bool = proxy.get('eps') is not None

    if valid_data:
        upsert_result: str = upsert_zacks_by_proxy(proxy)
        return  f'{SYMBOL} {proxy} {upsert_result}'
    else:
        return f'{symbol} {proxy} DictProxy data is not valid'








if __name__ == '__main__':
    pass


