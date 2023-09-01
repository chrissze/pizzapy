'''
    
I can only put some postgres make connection functions for other functions to import.

I cannot place postgres execution functions in this module, as it will led to circular imports.

'''


# STANDARD LIB
import sys; sys.path.append('..')
import json
from typing import Any, Dict, Union

# THIRD PARTY LIB
import pandas
from pandas.core.frame import DataFrame
from psycopg import connect, Connection, Cursor
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def make_psycopg_connection() -> Connection:
    '''
    DEPENDS: json, /etc/config.json FILE
    DO NOT put with open config.json at the global scope, other it will run everytime we import this module
    '''
    with open('/etc/config.json', 'r') as f:
        config: Dict[str, Union[str, int]] = json.load(f)
    pg_db: str = config.get('POSTGRES_DB')
    pg_user: str = config.get('POSTGRES_USER')
    pg_pass: str = config.get('POSTGRES_PASS')
    pg_host: str = config.get('POSTGRES_HOST')
    pg_port: int = config.get('POSTGRES_PORT')
    return connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host, port=pg_port)


def make_psycopg_cursor() -> Cursor: 
    '''
    DEPENDS: make_postgres_connection()
    If I want to return a Cursor, the make_connection function cannot be put into a with clause
    '''
    return make_psycopg_connection().cursor()



def execute_psycopg_command(cmd: str) -> None: 
    '''
    DEPENDS: make_postgres_cursor() 

    cur.excute(cmd) returns None
    compare with - pandas.read_sql(sql=cmd, con=make_postgres_connection())
    pandas.read_sql returns a DataFrame which contains results.
    '''
    with make_psycopg_cursor() as cur:
        cur.execute(cmd)
        

def make_sqlalchemy_engine() -> Engine:
    '''
    DEPENDS: sqlalchemy, json, FILE /etc/config.json
    DO NOT put with open config.json at the global scope, other it will run everytime we import this module
    used in pandas - read_sql() ; echo='debug' is for verbose debugging; echo=None to surpress verbose terminal info.
    '''
    with open('/etc/config.json', 'r') as f:
        config: Dict[str, Union[str, int]] = json.load(f)
    pg_user: str = config.get('POSTGRES_USER')
    pg_pass: str = config.get('POSTGRES_PASS')
    pg_host: str = config.get('POSTGRES_HOST')
    pg_port: int = config.get('POSTGRES_PORT')
    pg_db: str = config.get('POSTGRES_DB')
    postgres_engine: Engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}', echo=None)
    return postgres_engine



def execute_pandas_read(cmd: str) -> DataFrame:
    '''
    psycopg Connection can be used in pandas.read_sql, it will have warnings in the terminal when I run it.
    pandas recommend SQLAlchemy connection

    we do not need to add semicolon to the end of the sql command used in read_sql
    '''
    dataframe: DataFrame = pandas.read_sql(sql=cmd, con=make_sqlalchemy_engine())
    return dataframe



if __name__ == '__main__':

    cmd1 = 'SELECT now()'
    cmd2 = 'SELECT 2+2'
    cmd3 = 'SELECT version()'

    df = execute_psycopg_command(cmd3)
    print(df)
    print('done')