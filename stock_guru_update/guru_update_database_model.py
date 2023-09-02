# STANDARD LIBS
import sys; sys.path.append('..')

from typing import Any, List, Optional, Tuple, Union
from multiprocessing.managers import DictProxy


# THIRD PARTY LIBS

# CUSTOM LIBS
from batterypy.control.tools import trys
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

    I could wrap this function into trys(upsert, symbol),  
    because this function returns None.
    '''
    proxy: DictProxy = proxy_guru_wealth(symbol)
    valid_data: bool = proxy.get('wealth_pc') is not None

    if valid_data:
        query_and_values: str = upsert_guru_proxy(proxy)
        return query_and_values
    else:
        return f'{symbol} ProxyDict missed wealth_pc'


if __name__ == '__main__':

    s = input('which string to input? ')

    x = execute_psycopg(s, make_psycopg_connection())

    print(x)

