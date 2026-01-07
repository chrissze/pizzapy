"""

DEPENDS ON: raw_price_model.py

"""


# STANDARD LIBS

from datetime import date, datetime, timezone
from multiprocessing import Pool
from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS
import pandas
from pandas import DataFrame


# CUSTOM LIBS
from batterypy.control.trys import try_str
from dimsumpy.database.postgres import upsert_many_dataframe


# PROGRAM MODULES
from pizzapy.database_update.postgres_command_model import table_list_dict
from pizzapy.database_update.postgres_connection_model import make_psycopg_connection
from pizzapy.stock_price_update.raw_price_model import get_price_dataframe, get_price_dataframe_odict



def upsert_price_by_dataframe(df: DataFrame) -> str:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy(upsert_many_dataframe), table_list_dict, make_psycopg_connection()
    USED BY: upsert_price()
    
    """
    table_name: str = 'stock_price'
    pk_list: List[str] = table_list_dict[table_name].get('primary_key_list')
    query_result: str = upsert_many_dataframe(df, table=table_name, primary_key_list=pk_list, connection=make_psycopg_connection())
    return query_result



def upsert_price(FROM: date, TO: date, SYMBOL: str) -> str:
    """
    DEPENDS ON: upsert_price_by_dataframe()
    IMPORTS: get_price_dataframe()
    USED BY:
    
    small letter 'from' is a reserved keyword
    dates can be created by  d1 = date(2017, 2, 25)

    I should wrap upsert_price into a try block when I call it, because getting dataframe might have error when the date range has no data.
        result = try_str(upsert_price, d1, d2, symbol)
    """
    df: DataFrame = get_price_dataframe(FROM, TO, SYMBOL)
    result: str = upsert_price_by_dataframe(df)
    return result


def upsert_latest_price(SYMBOL: str) -> str:
    """
    DEPENDS ON: upsert_price_by_dataframe()
    IMPORTS: get_price_dataframe()
    USED BY:
    
    small letter 'from' is a reserved keyword
    dates can be created by  d1 = date(2017, 2, 25)

    I should wrap upsert_price into a try block when I call it, because getting dataframe might have error when the date range has no data.
        result = try_str(upsert_price, d1, d2, symbol)
    """
    FROM: date = date(2005, 7, 1)
    TO: date = date.today()
    result: str = upsert_price(FROM, TO, SYMBOL)
    return result



def test():
    d1 = date(2023, 2, 4)
    d2 = date(2023, 2, 4)
    symbol = 'NVDA'
    
    x = upsert_latest_price(symbol)
    print(x)

if __name__ == '__main__':
    test()