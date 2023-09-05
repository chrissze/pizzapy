

"""
    
"""
# STANDARD LIBS
import sys; sys.path.append('..')
from typing import Any, Dict, List, Tuple


# THIRD PARTY LIBS
from pandas import DataFrame, Series


# CUSTOM LIB
from dimsumpy.database.postgres import upsert_many_psycopg, make_upsert_psycopg_query

# PROGRAM MODULES
from database_update.postgres_connection_model import make_psycopg_connection
from stock_guru_update.guru_proxy_model import proxy_guru_wealth




if __name__ == '__main__':
    x = None
    print(type(x))
    if x:    
        print(f'{x} is truthy')
    else:
        print(f'{x} is falsy')