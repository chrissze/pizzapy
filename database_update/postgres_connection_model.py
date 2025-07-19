"""
    
I can only put some postgres make connection functions for other functions to import.

I cannot place postgres execution functions in this module, as it will led to circular imports.

"""


# STANDARD LIB

import os
from typing import Any, Dict, List, Optional, Union

# THIRD PARTY LIB
import pandas
from pandas.core.frame import DataFrame
from psycopg import connect, Connection, Cursor
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import requests
from requests.models import Response

# CUSTOM LIBS
from dimsumpy.database.postgres import make_upsert_psycopg_query, upsert_psycopg



def make_psycopg_connection() -> Connection:
    """
    DEPENDS: os, postgresql environment variables
    
    """
    pg_host: Optional[str] = os.getenv('PGHOST')
    pg_port: Optional[str] = os.getenv('PGPORT')
    pg_db: Optional[str] = os.getenv('PGDATABASE')
    pg_user: Optional[str] = os.getenv('PGUSER')
    pg_pass: Optional[str] = os.getenv('PGPASSWORD')
    return connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host, port=pg_port)


def make_psycopg_cursor() -> Cursor: 
    """
    DEPENDS: make_postgres_connection(), os

    If I want to return a Cursor, the make_connection function cannot be put into a with clause
    
    Not sure if I can do conn.commit() 
    """
    return make_psycopg_connection().cursor()





def execute_psycopg_command(cmd: str) -> list: 
    """
    
    DEPENDS: make_postgres_connection(), os

    I must include conn.commit(), otherwise the cmd will not be executed.
    cur.excute(cmd) returns None
    
    In psycopg 3, the connection object can directly execute SQL commands
    without creating a cursor object, The conn.execute() function returns a cursor object, 
    so we can access the execution result by this cursor object

    Optional to include semicolon at the end of the SQL command in psycopg.
    sample cmd: 'DROP TABLE emptytable1'

    compare with - pandas.read_sql(sql=cmd, con=make_postgres_connection())
    pandas.read_sql returns a DataFrame which contains results.
    """
    
    with make_psycopg_connection() as conn:
        cursor = conn.execute(cmd)
        result = cursor.fetchall() if cursor.description else [] 
        conn.commit()
        return result


def execute_psycopg_cursor_command(cmd: str) -> list: 
    """

    DEPENDS: make_postgres_connection(), /etc/config.json FILE

    psycopg cursor can return the execution result such as 

    [(5,)]
    [('mydb',)]

    I have made a pytest in pizzapy/tests/

    The execute_psycopg_cursor_command() and execute_psycopg_command()
    are functionally equivalent.

    """
    with make_psycopg_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(cmd)
            if cursor.description:
                result = cursor.fetchall() 
            else:
                result = []
            conn.commit()
            return result




def make_sqlalchemy_engine() -> Engine:
    """
    DEPENDS: sqlalchemy, os
    
    used in pandas - read_sql() ; echo='debug' is for verbose debugging; echo=None to surpress verbose terminal info.
    """
    pg_host: Optional[str] = os.getenv('PGHOST')
    pg_port: Optional[str] = os.getenv('PGPORT')
    pg_db: Optional[str] = os.getenv('PGDATABASE')
    pg_user: Optional[str] = os.getenv('PGUSER')
    pg_pass: Optional[str] = os.getenv('PGPASSWORD')
    postgres_engine: Engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}', echo=None)
    return postgres_engine



def execute_pandas_read(cmd: str) -> DataFrame:
    """
    psycopg Connection can be used in pandas.read_sql, it will have warnings in the terminal when I run it.
    pandas recommend SQLAlchemy connection

    we do not need to add semicolon to the end of the sql command used in read_sql
    """
    dataframe: DataFrame = pandas.read_sql(sql=cmd, con=make_sqlalchemy_engine())
    return dataframe





if __name__ == '__main__':

    cmd1 = 'SELECT now()'
    cmd2 = 'SELECT 2+3'
    cmd3 = 'SELECT version()'
    
    df = execute_pandas_read(cmd2)
    x = df.iloc[-1, -1]
    print(x)
    print('done')