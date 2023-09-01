'''
This module's function are mainly called by terminal scripts.

Prerequites of Postgres Server connection:
    (1) local computer has correct server IP in /etc/config.json 59.149.100.105 (hetzner a9)
    (2) hetzner cloud portal firewall allow local computer's IP (eg Seymour home IP, Arion IP)

    
SQL commands format in execute_pandas_read() and execute_psycopg_command():
    (1) Optional to add semicolon add the end. That is, I can omit it.

    
    
'''

# STANDARD LIB
import sys; sys.path.append('..')
import json
import subprocess
from typing import Any, Dict, List, Union


# THIRD PARTY LIB
import pandas
from pandas.core.frame import DataFrame

# PROGRAM MODULES
from postgres_command_model import stock_guru_create_table_command, stock_zacks_create_table_command, stock_option_create_table_command, stock_price_create_table_command, stock_technical_create_table_command,futures_option_create_table_command, db_table_command_dict

from postgres_connection_model import execute_pandas_read, execute_psycopg_command

        


def create_new_postgres_db():
    '''
    * INDEPENDENT *
    IMPORTS: subprocess
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
    * INDEPENDENT *
    IMPORTS: execute_pandas_read() 
    CALLED BY: show_single_table()
    '''
    describe_table_cmd: str = f"SELECT column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"
    dataframe: DataFrame = execute_pandas_read(describe_table_cmd)
    return dataframe



def show_tables() -> DataFrame:
    '''
    * INDEPENDENT *
    IMPORTS: execute_pandas_read()
    '''
    cmd = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    df: DataFrame = execute_pandas_read(cmd)
    return df


def show_single_table() -> None:
    '''
    DEPENDS ON: show_tables(), describe_table()
    IMPORTS: db_table_command_dict
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





def show_databases() -> DataFrame:
    '''
    * INDEPENDENT *
    IMPORTS: execute_pandas_read()
    '''
    cmd: str = "SELECT datname FROM pg_database WHERE datistemplate = false"
    df: DataFrame = execute_pandas_read(cmd)
    return df



def create_table(table_name:str) -> None:
    '''
    DEPENDS ON: describe_table()
    IMPORTS: db_table_command_dict, execute_psycopg_command()
    '''
    if table_name in db_table_command_dict:
        cmd: str = db_table_command_dict[table_name].get('command')
        execute_psycopg_command(cmd)
        describe_table(table_name)
    else:
        print('invalid table name')



def drop_table():
    '''
    * INDEPENDENT *
    IMPORTS:  db_table_command_dict, execute_psycopg_command()
    '''
    while True:
        table_name: str = input("\n\nWhich table do you want to DROP? input the table name or '0' to cancel: ")
        if table_name == '0':
            break
        elif table_name in db_table_command_dict:
            cmd: str = f'DROP TABLE {table_name}'
            execute_psycopg_command(cmd)
        else:
            print('invalid table name')




if __name__ == '__main__':
    cmd1 = 'SELECT now()'
    cmd2 = 'SELECT 2+2'
    cmd3 = 'SELECT version()'
    
    x = show_tables()    
    print(x)

    print(f'{__file__} done')
