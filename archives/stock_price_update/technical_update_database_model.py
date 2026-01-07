"""

"""


# STANDARD LIBS

from datetime import date
from typing import Any, Dict, Generator, List, Optional, Tuple, Union


# THIRD PARTY LIBS


# CUSTOM LIBS
from batterypy.time.cal import get_trading_day_utc
from batterypy.time.date import make_date_ranges

from dimsumpy.database.postgres import upsert_many_dicts


# PROGRAM MODULES
from pizzapy.database_update.postgres_command_model import table_list_dict
from pizzapy.database_update.postgres_connection_model import make_psycopg_connection
from pizzapy.stock_price_update.technical_analysis_model import construct_technical_proxies



def upsert_technical_by_dicts(table_name: str, dicts: List[Dict]) -> str:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy(upsert_many_dataframe), table_list_dict, make_psycopg_connection()
    USED BY: upsert_technical()
    
    """
    #table_name: str = 'stock_technical'
    pk_list: List[str] = table_list_dict[table_name].get('primary_key_list')
    query_result: str = upsert_many_dicts(dicts, table=table_name, primary_key_list=pk_list, connection=make_psycopg_connection())
    return query_result



def upsert_technical(FROM: date, TO: date, SYMBOL: str) -> Generator[str, None, None]:
    """
    DEPENDS ON: upsert_technical_by_dicts()
    IMPORTS: get_technical_proxies()
    USED BY:
    
    small letter 'from' is a reserved keyword
    dates can be created by  d1 = date(2017, 2, 25)

    I should wrap upsert_technical into a try block when I call it, because getting dicts might have error when the date range has no data.
        result = try_str(upsert_technical, from_date, to_date, symbol)
    """
    date_ranges = make_date_ranges(FROM, TO, 3)
    #generator = (x for x in [])
    for start, end in date_ranges:
        proxies: List[Dict] = construct_technical_proxies(start, end, SYMBOL)
        result: str = upsert_technical_by_dicts('stock_technical', proxies)
        yield result
    

def upsert_technical_one(SYMBOL: str) -> str:
    """
    DEPENDS ON: upsert_technical_by_dicts()
    IMPORTS: get_technical_proxies()
    USED BY:
    
    small letter 'from' is a reserved keyword
    dates can be created by  d1 = date(2017, 2, 25)

    I should wrap upsert_technical into a try block when I call it, because getting dicts might have error when the date range has no data.
        result = try_str(upsert_technical, from_date, to_date, symbol)
    """
    TO: date = date.today()
    FROM: date = get_trading_day_utc()
    proxies: List[Dict] = construct_technical_proxies(FROM, TO, SYMBOL)
    result: str = upsert_technical_by_dicts('technical_one', proxies)
    return result


def upsert_recent_technical(SYMBOL: str) -> None:
    """
    DEPENDS ON: upsert_technical_by_dicts()
    IMPORTS: get_technical_proxies()
    USED BY:
    
    small letter 'from' is a reserved keyword
    dates can be created by  d1 = date(2017, 2, 25)

    I should wrap upsert_price into a try block when I call it, because getting dataframe might have error when the date range has no data.
        result = try_str(upsert_technical, d1, d2, symbol)
    """
    TO: date = date.today()
    FROM: date = date(TO.year - 2, TO.month, TO.day)
    result_gen = upsert_technical(FROM, TO, SYMBOL)
    for result in result_gen:
        print(result)



def test():
    d1 = date(2023, 2, 4)
    d2 = date(2023, 2, 4)
    symbol = 'NVDA'
    
    x = upsert_recent_technical(symbol)
    print(x)

if __name__ == '__main__':
    test()