"""

"""


# STANDARD LIBS
import sys; sys.path.append('..')
from datetime import date, datetime, timezone
from multiprocessing import Pool
from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, Dict, List, Optional, Tuple, Union


# THIRD PARTY LIBS
import pandas
from pandas import DataFrame


# CUSTOM LIBS
from batterypy.control.trys import try_str
from dimsumpy.database.postgres import upsert_many_dicts


# PROGRAM MODULES
from database_update.postgres_command_model import table_list_dict
from database_update.postgres_connection_model import make_psycopg_connection
from stock_price_update.technical_analysis_model import construct_technical_proxies



def upsert_technical_by_dicts(dicts: List[Dict]) -> str:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy(upsert_many_dataframe), table_list_dict, make_psycopg_connection()
    USED BY: upsert_technical()
    
    """
    table_name: str = 'stock_technical'
    pk_list: List[str] = table_list_dict[table_name].get('primary_key_list')
    query_result: str = upsert_many_dicts(dicts, table=table_name, primary_key_list=pk_list, connection=make_psycopg_connection())
    return query_result



def upsert_technical(FROM: date, TO: date, SYMBOL: str) -> str:
    """
    DEPENDS ON: upsert_technical_by_dicts()
    IMPORTS: get_technical_proxies()
    USED BY:
    
    small letter 'from' is a reserved keyword
    dates can be created by  d1 = date(2017, 2, 25)

    I should wrap upsert_technical into a try block when I call it, because getting dicts might have error when the date range has no data.
        result = try_str(upsert_technical, from_date, to_date, symbol)
    """
    proxies: List[Dict] = construct_technical_proxies(FROM, TO, SYMBOL)
    result: str = upsert_technical_by_dicts(proxies)
    return result


def upsert_latest_technical(SYMBOL: str) -> str:
    """
    DEPENDS ON: upsert_technical_by_dicts()
    IMPORTS: get_technical_proxies()
    USED BY:
    
    small letter 'from' is a reserved keyword
    dates can be created by  d1 = date(2017, 2, 25)

    I should wrap upsert_price into a try block when I call it, because getting dataframe might have error when the date range has no data.
        result = try_str(upsert_technical, d1, d2, symbol)
    """
    FROM: date = date(2023, 1, 1)
    TO: date = date.today()
    result: str = upsert_technical(FROM, TO, SYMBOL)
    return result



def test():
    d1 = date(2023, 2, 4)
    d2 = date(2023, 2, 4)
    symbol = 'AMD'
    
    x = upsert_latest_technical(symbol)
    print(x)

if __name__ == '__main__':
    test()