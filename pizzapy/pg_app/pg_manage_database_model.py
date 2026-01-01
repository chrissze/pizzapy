"""
This module's function are mainly called by terminal_scripts/postgres_operation_script.py.

Prerequites of Postgres Server connection:
    (1) local computer has correct server IP in /etc/config.json 59.149.100.105 (hetzner a9)
    (2) hetzner cloud portal firewall allow local computer's IP (eg Seymour home IP, Arion IP)

    
SQL commands format in execute_pandas_read() and execute_psycopg_command():
    (1) Optional to add semicolon add the end. That is, I can omit it.

    (2) Need to have conn.commit() in psycopg execute() function.
    
"""

# STANDARD LIB

import subprocess
from typing import Any, Dict, List, Union


# THIRD PARTY LIB
import pandas
from pandas.core.frame import DataFrame

# PROGRAM MODULES
from pizzapy.pg_app.pg_command_model import table_list_dict

from pizzapy.pg_app.pg_connection_model import execute_pandas_read, execute_psycopg_command

        
def show_table(table_name: str) -> DataFrame:
    """
    * INDEPENDENT *
    IMPORTS: execute_pandas_read() 
    CALLED BY: loop_show_table()
    {table_name} in the cmd needs to be single quoted. Semicolon at the end is optional.
    
    full_cmd: str = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"

    empty tables without any column will have empty dataframe result.
    """
    cmd: str = f"SELECT column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"
    df: DataFrame = execute_pandas_read(cmd)
    return df






def loop_show_table() -> None:
    """
    DEPENDS ON: show_tables(), show_table()
    IMPORTS: table_list_dict
    """
    while True:
        print()
        print(show_tables())
        table_name: str = input('\nInput a TABLE NAME to show table columns (0 to quit): ')
        if table_name == '0':
            break
        else:
            print(show_table(table_name))
        


def show_table_rows(table_name: str, limit_rows: int) -> DataFrame:
    """
    * INDEPENDENT *
    IMPORTS: execute_pandas_read() 
    CALLED BY: loop_show_table_rows()

    empty tables without any column will have empty dataframe result.
    """
    cmd: str = f"SELECT * FROM {table_name} LMIIT {limit_rows};"
    df: DataFrame = execute_pandas_read(cmd)
    return df



def loop_show_table_rows() -> None:
    """
    DEPENDS ON: show_table_rows()
    IMPORTS: execute_pandas_read() 

    """
    while True: 
        print(show_tables())
        print()
        table_name: str = input('Input a TABLE NAME to show content (0 to cancel): ')
        if table_name == '0':
            break
        elif table_name: 
            limit_rows: str = input('Input NUMBER OF ROWS: ')
            cmd: str = f"SELECT * FROM {table_name} LIMIT {limit_rows}"
            df: DataFrame = execute_pandas_read(cmd)
            print(df)
        else:
            print('Invalid input.')




def create_table(table_name:str) -> None:
    """
    DEPENDS ON: show_table(), show_tables()
    IMPORTS: table_list_dict, execute_psycopg_command()
    """
    if table_name in table_list_dict:
        cmd: str = table_list_dict[table_name].get('command')
        execute_psycopg_command(cmd)
        print(f"\nTable {table_name} columns: \n")
        print(show_table(table_name))
        print('\nLatest available tables in Postgresql database: \n')
        print(show_tables())
    
    elif table_name:
        reply = input(f"\nYour input '{table_name}' is not in table_list_dict, do you want to create a new table '{table_name}' with a single 'id' column (y/N)?")

        if reply == 'y':
            cmd: str = f'CREATE TABLE IF NOT EXISTS {table_name} ( id BIGSERIAL, PRIMARY KEY (id) );'
            execute_psycopg_command(cmd)
            print(f"\nTable {table_name} columns: \n")
            print(show_table(table_name))
            print('\nLatest available tables in Postgresql database: \n')
            print(show_tables())
    else:
        print('invalid table name')



def loop_drop_table():
    """
    DEPENDS ON: show_tables()
    IMPORTS:  table_list_dict, execute_psycopg_command()
    """
    while True:
        print('\nLatest available tables in Postgresql database: \n')
        print(show_tables())
        table_name: str = input("\nWhich table do you want to DROP? Input the TABLE NAME or '0' to cancel: ")
        drop_table_cmd: str = f'DROP TABLE IF EXISTS {table_name}'
        if table_name == '0':
            break
        elif table_name in table_list_dict:
            reply = input(f"\nYou are going to DROP TABLE '{table_name}', it is a CRITICAL TABLE in table_list_dict, do you really want to drop this table (y/N)?")
            if reply == 'y':
                execute_psycopg_command(drop_table_cmd)
        elif table_name:
                execute_psycopg_command(drop_table_cmd)
        else:
            print('invalid table name')



def test() -> None:


    s: str = input("\nWhich string do you want to input? ")
    x = s
    print(x)
    print(f'{__file__} done')



if __name__ == '__main__':
    test()