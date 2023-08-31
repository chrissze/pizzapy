'''

'''

# STANDARD LIB
import sys; sys.path.append('..')
import json
import subprocess
from typing import Any, Dict, List, Union


# THIRD PARTY LIB
import pandas
from pandas.core.frame import DataFrame
from psycopg import connect, Connection, Cursor



def make_postgres_connection() -> Connection:
    '''
    DEPENDS: /etc/config.json FILE
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


def make_postgres_cursor() -> Cursor: 
    '''
    If I want to return a Cursor, the make_connection function cannot be put into a with clause
    '''
    return make_postgres_connection().cursor()


def execute_postgres_command(cmd: str) -> None: 
    with make_cursor() as cur:
        cur.execute(cmd)

        


def create_new_postgres_db():
    '''
    DEPENDS: subprocess
    '''
    new_database_name = input('Please input the desired database name then press ENTER: ')
    reply = input(f'Do you want to create a new database in Postgresql - {new_database_name} (y/N)? ')
    if reply == 'y':
        createdb_cmd = f'createdb {new_database_name} -U postgres'
        subprocess.run(createdb_cmd, stdin=True, shell=True)
        print(f'Just created a database -- {new_database_name}')
    else:
        print('no database is created')




def describe_table(table_name: str) -> DataFrame:
    '''
    DEPENDS: cnx
    CALLED BY: show_single_table()
    '''
    describe_table_command: str = f"SELECT column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"
    dataframe: DataFrame = pandas.read_sql(describe_table_command, con=cnx)
    return dataframe



def show_single_table() -> None:
    '''
    DEPENDS: describe_table()
    '''
    while True:
        show_tables()
        table: str = input('Input table name (0 to quit): ')
        if table == '0':
            break
        elif table in db_table_command_dict:
            describe_table(table)
        else:
            print('invalid table name')




def show_tables():
    con: connection = connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host)
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    df: DataFrame = pd.read_sql(sql, con=cnx)
    print(df)
    if con: con.close()


def show_databases():
    con: connection = connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host)
    sql = "SELECT datname FROM pg_database WHERE datistemplate = false;"
    df: DataFrame = pd.read_sql(sql, con=con)
    print(df)
    if con: con.close()



def create_db():
    dbname = input('Please input the desired database name then press ENTER: ')
    reply = input(f'Do you want to create a database - {dbname} (y/N)? ')
    if reply == 'y':
        cmd1 = f'createdb {dbname} -U postgres'
        subprocess.run(cmd1, stdin=True, shell=True)
        print('Created a database --', dbname)
    else:
        print('no database is created')




test_command_1 = 'SELECT now();'
test_command_2 = 'SELECT 2+2;'
test_command_3 = 'SELECT version();'
test_command_4 = 'CREATE DATABASE corndb;'

def test_postgres_server() -> None:
    """ to ensure db, user, pw are all fine """
    q = test_command_3
    df: DataFrame = pd.read_sql(sql=q, con=postgres_engine)
    print(df)

if __name__ == '__main__':
    test_postgres_server()
    print('done')
