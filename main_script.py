#!/usr/bin/env python3

import subprocess
from datetime import date
from time import sleep
from pathlib import Path
from typing import List

import pandas as pd
from batterypy.string.read import int0
from batterypy.time.cal import get_trading_day_utc, add_days
from pandas import DataFrame
from dimsumpy.database.postgres import db_exec
from futures_update.ino_model import ino_upsert_all, ino_upsert_1s
from shared_model.fut_data_model import all_fut, fut_dict
from shared_model.sql_model import cnx, create_db, create_table, db_dict, show_single_table, drop_table, show_databases, \
    show_tables, get_con, cnx2, postgres_engine
from shared_model.st_data_model import all_stocks, stock_list_dict
from stock_core_update.guru_model import guru_upsert_1s
from stock_core_update.option_model import option_upsert_1s
from stock_core_update.zacks_model import zacks_upsert_1s
from stock_price_update.st_price_update_model import ya_px_upsert_1s


def start():
    actions = {
        '1': lambda: manage_stocks(),
        '2': lambda: manage_futures(),
        '3': lambda: manage_database(),
        '0': lambda: exit(),
    }
    while True:
        subprocess.run(['clear'])
        ans = input(f"""
        Stock Actions: 
            1) Manage Stocks
            2) Manage Futures            
            3) Manage Database, create or drop tables
            0) Exit the program
            
        please choose your action: """)
        if ans in actions:
            actions[ans]()
        else:
            print('invalid input')


#################################################

#################################################


def manage_stocks():
    actions = {
        '1': lambda: browse_single_st_core_1d(),
        '2': lambda: browse_st_table_from_list(),
        '3': lambda: update_single_st_gu(),
        '4': lambda: update_single_st_za(),
        '5': lambda: update_single_st_op(),
        '6': lambda: update_single_st_core(),
        '7': lambda: update_st_list_core(),
        '8': lambda: update_single_st_price(),

    }
    while True:
        ans = input("""\n\n
        Which action do you want to do? 
        1)  browse_single_st_core_1d
        2)  browse_st_table_from_list
        
        Update:
        3)  update_single_st_gu
        4)  update_single_st_za
        5)  update_single_st_op
        6)  update_single_st_core
        7)  update_st_list_core
        8)  update_single_st_price
        0)  go to home screen
        Choose your action: """)
        if ans in actions:
            actions[ans]()
        elif ans == '0':
            break
        else:
            print('invalid input')


def browse_st_table_from_list() -> None:
    while True:
        print('\n\n')
        list_names = list(db_dict.keys())
        list_len: int = len(list_names)
        for count, name in enumerate(list_names, start=1):
            print(f'{count} {name} ')
        st_list_num = input('\nQ1: Which list do you want to update? input list no. (0 to quit): ')
        num = int0(st_list_num)
        if num <= 0 or num > list_len:
            print('invalid stock list number, start over')
            sleep(1)
            break
        table: str = list_names[num - 1]
        browse_st_table_1s(table)


def browse_st_table_1s(table: str) -> None:
    while True:
        symbol: str = input('\n\nWhich symbol do you want to check (input 0 to quit) ?')
        s = symbol.upper()
        if symbol == '0':
            break
        elif s in all_stocks:
            sql: str = f"SELECT * FROM {table} WHERE symbol = '{s}' ORDER BY t DESC;"
            df: DataFrame = pd.read_sql(sql, con=postgres_engine)
            print(df)
        else:
            print('you have entered an invalid symbol')


def browse_single_st_core_1d() -> None:
    while True:
        symbol: str = input('\n\nWhich symbol do you want to check (input * before the symbol to update, input 0 to quit) ?')
        s = symbol.upper()
        if s[:1] == '*' and s[1:] in all_stocks:
            s = s[1:]
            guru_upsert_1s(s)
            zacks_upsert_1s(s)
            option_upsert_1s(s)

        if symbol == '0':
            break
        elif s in all_stocks:
            sql_option: str = f"SELECT * FROM usstock_option WHERE symbol = '{s}' ORDER BY t DESC;"
            sql_g: str = f"SELECT * FROM usstock_g WHERE symbol = '{s}' ORDER BY t DESC;"
            sql_z: str = f"SELECT * FROM usstock_z WHERE symbol = '{s}' ORDER BY t DESC;"
            df_option: DataFrame = pd.read_sql(sql_option, con=postgres_engine)
            df_g: DataFrame = pd.read_sql(sql_g, con=postgres_engine)
            df_z: DataFrame = pd.read_sql(sql_z, con=postgres_engine)
            latest_option = pd.DataFrame() if df_option.empty else df_option.iloc[0]
            latest_g = pd.DataFrame() if df_g.empty else df_g.iloc[0]
            latest_z = pd.DataFrame() if df_z.empty else df_z.iloc[0]
            print(f"""
Stock Options:
--------------------------------------------
{latest_option}

Fundamentals(z):
--------------------------------------------
{latest_z}

Fundamentals(g):
--------------------------------------------
{latest_g}

            """)
        else:
            print('you have entered an invalid symbol')


def update_st_list_core() -> None:
    while True:
        print('\n\n')
        list_names = list(stock_list_dict.keys())
        list_len: int = len(list_names)
        for count, name in enumerate(list_names, start=1):
            print(f'{count} {name} ')
        st_list_num = input('\nQ1: Which list do you want to update? input list no. (0 to quit): ')
        num = int0(st_list_num)
        if num <= 0 or num > list_len:
            print('invalid stock list number, start over')
            sleep(1)
            break
        else:
            func_list_num = input("""\nQ2: Which function do you want to execute?
            1)  guru_upsert_1s
            2)  zacks_upsert_1s
            3)  option_upsert_1s
            4)  all of the above
            input function no.: """)
        name = list_names[num - 1]
        start_str = input('\nQ3 input start number(press ENTER for 0): ')
        st_list: List[str] = stock_list_dict.get(name)[int0(start_str):]

        if func_list_num == '1':
            for count, s in enumerate(st_list, start=1):
                guru_upsert_1s(s)
                msg: str = f"{count} / {len(st_list)}  {s}"
        elif func_list_num == '2':
            for count, s in enumerate(st_list, start=1):
                zacks_upsert_1s(s)
                msg: str = f"{count} / {len(st_list)}  {s}"
        elif func_list_num == '3':
            for count, s in enumerate(st_list, start=1):
                option_upsert_1s(s)
                msg: str = f"{count} / {len(st_list)}  {s}"
        elif func_list_num == '4':
            for count, s in enumerate(st_list, start=1):
                guru_upsert_1s(s)
                zacks_upsert_1s(s)
                option_upsert_1s(s)
                msg: str = f"{count} / {len(st_list)}  {s}"
        else:
            print('invalid function list number, start over')
            sleep(1)
            break



def update_single_st_core() -> None:
    while True:
        symbol: str = input('Which stock do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            guru_upsert_1s(s)
            zacks_upsert_1s(s)
            option_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')



def update_single_st_gu() -> None:
    while True:
        symbol: str = input('Which stock do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            guru_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')


def update_single_st_za() -> None:
    while True:
        symbol: str = input('Which stock do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            zacks_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')


def update_single_st_op() -> None:
    while True:
        symbol: str = input('Which stock do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            option_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')




def update_single_st_price() -> None:
    while True:
        symbol: str = input('Which stock do you want to update price (input 0 to quit) ?')

        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            year_str: str = input('How many year? (ENTER for past 20-days only')
            year: int = int0(year_str)
            to: date = get_trading_day_utc()
            from_: date = add_days(to, 365 * (-year) - 20)
            ya_px_upsert_1s(from_, to, s)

        else:
            print('you have entered an invalid symbol')



#################################################

def manage_futures():
    actions = {
        '1': lambda: browse_single_fut_option_1d(),
        '2': lambda: browse_all_fut_option_1d(),

        '6': lambda: update_single_fut_option(),
        '7': lambda: ino_upsert_all(),
    }
    while True:
        ans = input("""\n\n
        Which action do you want to do? 
        1)  browse_single_fut_option_1d
        2)  browse_all_fut_option_1d
        6)  update_single_fut_option 
        7)  ino_upsert_all
            
        0) go to home screen
        Choose your action: """)
        if ans in actions:
            actions[ans]()
        elif ans == '0':
            break
        else:
            print('invalid input')


fut_dict_pagina = "\n".join(
    [f"                          {k} {v.get('type')} {v.get('name1')}" for k, v in fut_dict.items()])


def update_single_fut_option() -> None:
    while True:
        print(fut_dict_pagina)
        symbol: str = input('Which futures do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_fut:
            ino_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')


def browse_single_fut_option_1d() -> None:
    print(fut_dict_pagina)
    while True:
        symbol: str = input('\n\nWhich symbol do you want to check (input * before the symbol to update, input 0 to quit) ?')
        s = symbol.upper()
        if s[:1] == '*' and s[1:] in all_fut:
            s = s[1:]
            ino_upsert_1s(s)

        if symbol == '0':
            break
        elif s in all_fut:
            print(fut_dict_pagina)
            sql: str = f"SELECT * FROM fut_option WHERE symbol = '{s}' ORDER BY t DESC;"
            df: DataFrame = pd.read_sql(sql, con=postgres_engine)
            if df.empty:
                print('empty result')
            else:
                print(df.iloc[0])
        else:
            print('you have entered an invalid symbol')



def browse_all_fut_option_1d() -> None:
    td: date = get_trading_day_utc()
    cols = 'td, symbol, px, capstr, callratio, putratio, callpc, putpc'
    print(td)
    sql: str = f"SELECT {cols} FROM fut_option WHERE td = '{td}' ORDER BY t DESC;"
    df: DataFrame = pd.read_sql(sql, con=postgres_engine)
    print(df)


####################################################

def manage_database():
    actions = {
        '3': lambda: create_table('usstock_tech'),
        '4': lambda: create_table('usstock_price'),
        '5': lambda: create_table('usstock_option'),
        '6': lambda: create_table('usstock_g'),
        '7': lambda: create_table('usstock_z'),
        '8': lambda: create_table('fut_option'),
        '11': lambda: create_db(),
        '12': lambda: show_databases(),
        '13': lambda: show_tables(),
        '14': lambda: show_single_table(),
        '15': lambda: drop_table(),
        '20': lambda: subprocess.run('cat /etc/config.json', stdin=True, shell=True),
    }
    while True:
        ans = input("""\n\n
        Which action do you want to do? 
            3)  create_usstock_tech() 
            4)  create_usstock_price() 
            5)  create_usstock_option() 
            6)  create_usstock_g() 
            7)  create_usstock_z() 
            8)  create_fut_option()
            11) Create a database (NOT table)   
            12) Show all database  
            13) Show all Tables
            14) Show single table
            15) Drop a table      
            20) Print content of /etc/config.json
            0) go to home screen
        Choose your action: """)
        if ans in actions:
            actions[ans]()
        elif ans == '0':
            break
        else:
            print('invalid input')


if __name__ == '__main__':
    #update_single_st_price()
    start()

    #print(sys.path)

