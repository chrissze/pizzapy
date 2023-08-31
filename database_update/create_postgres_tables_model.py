'''
Variables such as command strings and dictionaries will be placed at the top

    stock_guru_create_table_command
    stock_zacks_create_table_command
    stock_option_create_table_command
    stock_price_create_table_command
    stock_technical_create_table_command
    futures_option_create_table_command

    db_table_command_dict




Functions will be placed in the second section.

'''



import sys; sys.path.append('..')
import subprocess

import json
import os
import pandas
from pandas.core.frame import DataFrame

from psycopg2 import connect
from psycopg2.extensions import connection, cursor
from sqlalchemy import create_engine # sqlalchemy generates SQL statement and depends on psycopg2 to communicate the db
from sqlalchemy.engine.base import Engine
from typing import Any, Dict, List, Union

from dimsumpy.database.postgres import execute_postgres_command




# gurufocus
stock_guru_create_table_command: str = '''
    CREATE TABLE stock_guru (
    gid BIGSERIAL, 
    update_time   TIMESTAMP,                    
    trade_date   DATE,              
    symbol   VARCHAR(10),         
    
    price   FLOAT8,
    cap   FLOAT8,    
    capstr   VARCHAR(15),

    book_value   FLOAT8,    
    book_value_pc   FLOAT8,    

    debt_per_share   FLOAT8,    
    debt_pc   FLOAT8,    
    earn_per_share   FLOAT8,  
    earn_pc   FLOAT8,    

    interest   FLOAT8,    
    interest_pc   FLOAT8,  

    lynch   FLOAT8,    
    lynch_move_pc   FLOAT8,    
    
    net_capital   FLOAT8,    
    net_capital_pc   FLOAT8, 

    research   FLOAT8, 
    research_pc   FLOAT8,    
    
    revenue_per_share   FLOAT8,    
    revenue_pc   FLOAT8,    
    growth1y   FLOAT8,    
    growth3y   FLOAT8,        
    qrowth5y   FLOAT8,    
    qrowth10y   FLOAT8,    
    
    strength   FLOAT8,    
    zscore   FLOAT8,
    
    wealth_pc   FLOAT8,  
    PRIMARY KEY (symbol)
    );
    '''


# zacks
stock_zacks_create_table_command: str = '''
    CREATE TABLE stock_zacks ( 
    zid  BIGSERIAL, 
    t   TIMESTAMP,                    
    td   DATE,        
    symbol   VARCHAR(10),         
    edate   DATE,        
    recom   FLOAT8,    
    eps   FLOAT8,    
    feps   FLOAT8,    
    eps12   FLOAT8,     
    vgm_grade   VARCHAR(1),         
    value_grade   VARCHAR(1),         
    growth_grade   VARCHAR(1),         
    momentum_grade   VARCHAR(1),         
    peg   FLOAT8,    
    pb   FLOAT8,    
    pcf   FLOAT8,    
    pe   FLOAT8,    
    psales   FLOAT8,    
    earn_yield   FLOAT8,    
    cash_pct   FLOAT8,    
    chg1d   FLOAT8,    
    chg5d   FLOAT8,  
    chg1m   FLOAT8,    
    chg3m   FLOAT8,    
    chg1y   FLOAT8,
    PRIMARY KEY (symbol)
    );
    '''


# yahoo
stock_price_create_table_command: str = """
    CREATE TABLE usstock_price (
    id  BIGSERIAL, 
    t   TIMESTAMP,                    
    symbol   VARCHAR(10) NOT NULL,         
    td   DATE NOT NULL,  
    op   FLOAT8,    
    hi   FLOAT8,
    lo   FLOAT8,    
    cl   FLOAT8 NOT NULL,    
    adjcl  FLOAT8 NOT NULL,    
    vol BIGINT,    
    PRIMARY KEY (symbol, td) 
    );
    """


stock_technical_create_table_command: str = """
    CREATE TABLE usstock_tech (
    id  BIGSERIAL, 
    t   TIMESTAMP,                    
    symbol   VARCHAR(10) NOT NULL,         
    td   DATE NOT NULL,  
    px   FLOAT8,    
    p20   FLOAT8,
    p50   FLOAT8,    
    p125   FLOAT8,    
    p200  FLOAT8,        
    PRIMARY KEY (symbol, td) 
    );
    """



# nasdaq or barchart
stock_option_create_table_command: str = """CREATE TABLE usstock_option             
    (oid  BIGSERIAL, 
     t   TIMESTAMP,                    
     td   DATE  NOT NULL,        
     symbol   VARCHAR(10) NOT NULL,         
     capstr   VARCHAR(15),         
     cap   FLOAT8,    
     px   FLOAT8,    
     callmoney   FLOAT8,    
     putmoney   FLOAT8,  
     callratio   FLOAT8,    
     putratio   FLOAT8,    
     callpc   FLOAT8,    
     putpc   FLOAT8,    
     PRIMARY KEY (symbol, td) );"""






#ino
futures_option_create_table_command: str = """CREATE TABLE fut_option             
    (id  BIGSERIAL, 
     t   TIMESTAMP,                    
     td   DATE  NOT NULL,        
     symbol   VARCHAR(10) NOT NULL,         
     capstr   VARCHAR(15),         
     cap   FLOAT8,    
     oi   FLOAT8,    
     px   FLOAT8,    
     callmoney   FLOAT8,    
     putmoney   FLOAT8,  
     callratio   FLOAT8,    
     putratio   FLOAT8,    
     callpc   FLOAT8,    
     putpc   FLOAT8,    
     PRIMARY KEY (symbol, td)
    );"""



'''
This dictionary can be used to compose upsert commands
option, price and technicals are from yahoo
'''
db_table_command_dict: Dict[str, Any] = {
    'stock_guru': {'pk': ['symbol'], 'command': stock_guru_create_table_command},
    'stock_zacks': {'pk': ['symbol'], 'command': stock_zacks_create_table_command},
    'stock_option': {'pk': ['symbol', 'td'], 'command': stock_option_create_table_command},
    'stock_price': {'pk': ['symbol', 'td'], 'command': stock_price_create_table_command},
    'stock_technical': {'pk': ['symbol', 'td'], 'command': stock_technical_create_table_command},
    'futures_option': {'pk': ['symbol', 'td'], 'command': futures_option_create_table_command},
}





def create_table(table_name:str) -> None:
    '''
    DEPENDS: execute_postgres_command (dimsumpy)
    There might be similar function in the official psycopg
    '''
    if table_name in db_table_command_dict:
        execute_postgres_command(db_table_command_dict[table_name].get('command'), con=cnx)
        describe_table(table)
    else:
        print('invalid table name')



def drop_table():
    '''
    DEPENDS: execute_postgres_command (dimsumpy)
    There might be similar function in the official psycopg
    '''
    while True:
        table: str = input("\n\nWhich table do you want to DROP? input the table name or '0' to cancel: ")
        if table == '0':
            break
        elif table in db_table_command_dict:
            sql: str = f'DROP TABLE {table};'
            execute_postgres_command(sql, con=cnx)
        else:
            print('invalid table name')



if __name__ == '__main__':
