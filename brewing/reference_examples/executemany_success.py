

"""
sameple query for upsert_many_psycopg:
        INSERT INTO domain5 (domain) VALUES (%s)
        ON CONFLICT (domain)
        DO NOTHING

sample list of values  (list of dictionary) for upsert_many_psycopg:
    dicts = [{'domain': 'aaaaaa.com'}, {'domain': 'bbbbbb.com'}]

    CONVERTED INTO:    [('aaaaaa.com',),('bbbbbb.com',)]


def make_upsert_psycopg_query(table: str, columns: List[str], primary_key_list: List[str]) -> str:
    
"""
# STANDARD LIB

from typing import Any, Dict, List, Tuple


# CUSTOM LIB
from batterypy.control.tools import trys
from dimsumpy.database.postgres import upsert_many_psycopg, make_upsert_psycopg_query

# PROGRAM MODULES
from pizzapy.database_update.postgres_connection_model import make_psycopg_connection
from pizzapy.guru_stock_update.guru_proxy_model import make_guru_proxy


def make_query() -> str:
    dict1 = make_guru_proxy('KO')

    pk_list = ['symbol']
    sql: str = make_upsert_psycopg_query('guru_stock', columns=dict1.keys(), primary_key_list=pk_list)
    return sql



def make_values() -> List[List]:
    dict1 = make_guru_proxy('KO')
    dict2 = make_guru_proxy('MS')

    value1 = dict1.values()    # List
    value2 = dict2.values()
    return [value1, value2]


def upsert_many_example() -> None:
    with make_psycopg_connection() as con:
        with con.cursor() as cur:
            query = make_query()
            values = make_values()
            cur.executemany(query, values)
        con.commit()


def make_dicts() -> List[Dict]:
    dict1 = make_guru_proxy('KO')
    dict2 = make_guru_proxy('MS')
    return [dict1, dict2]


def upsert_dicts_example() -> None:
    """
    It is not practical to fetch mutiple DictProxies and accumulate them, then run upsert_many_psycopg. As this increase the code complexity and harder to debug. Not much time saved.

    I would rather loop through a list of stock symbols, fetch a DictProxy, and run upsert_psycopg() one by one.

    FUNCION SIGNATURE:
        def upsert_many_psycopg(dictionaries: List[Dict], table: str, primary_key_list: List[str], connection: Connection) -> str:
    
    """
    dicts = make_dicts()
    pk_list = ['symbol']
    upsert_many_psycopg(dicts, 'guru_stock', pk_list, connection=make_psycopg_connection())

if __name__ == '__main__':
    upsert_dicts_example()
    print('done')