import sys; sys.path.append('..')
import subprocess

import json
import os
import pandas as pd
from pandas.core.frame import DataFrame

from psycopg2 import connect
from psycopg2.extensions import connection, cursor
from sqlalchemy import create_engine # sqlalchemy generates SQL statement and depends on psycopg2 to communicate the db
from sqlalchemy.engine.base import Engine
from typing import Any, Dict, List, Union

from dimsumpy.database.postgres import db_exec

with open('/etc/config.json', 'r') as f:
    config = json.load(f)


pg_db: str = config.get('POSTGRES_DB')
pg_user: str = config.get('POSTGRES_USER')
pg_pass: str = config.get('POSTGRES_PASS')
pg_host: str = config.get('POSTGRES_HOST')


cnx: connection = connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host)

cnx1: connection = connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host)
cnx2: connection = connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host)
cnx3: connection = connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host)


def get_con() -> connection:
    if cnx1: return cnx1
    elif cnx2: return cnx2
    elif cnx3: return cnx3
    else: return cnx


# used in pandas - read_sql() ; echo is for logging
postgres_engine: Engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:5432/{pg_db}', echo='debug')

#ino
fut_option_command: str = """CREATE TABLE fut_option             
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

# yahoo
usstock_price_command: str = """CREATE TABLE usstock_price       
    (id  BIGSERIAL, 
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
    );"""


usstock_tech_command: str = """CREATE TABLE usstock_tech       
    (id  BIGSERIAL, 
     t   TIMESTAMP,                    
     symbol   VARCHAR(10) NOT NULL,         
     td   DATE NOT NULL,  
     px   FLOAT8,    
     p20   FLOAT8,
     p50   FLOAT8,    
     p125   FLOAT8,    
     p200  FLOAT8,    
         
     PRIMARY KEY (symbol, td) 
    );"""





# nasdaq or barchart
usstock_option_command: str = """CREATE TABLE usstock_option             
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

# gurufocus
usstock_g_command: str = """CREATE TABLE usstock_g             
    (gid  BIGSERIAL, 
     t   TIMESTAMP,                    
     td   DATE,              
     symbol   VARCHAR(10),         
     px   FLOAT8,
     cap   FLOAT8,    
     capstr   VARCHAR(15),         
     coco   FLOAT8,  
     debt_per_share   FLOAT8,    
     debtpc   FLOAT8,    
     earn_per_share   FLOAT8,  
     earnpc   FLOAT8,    
     strength   INT,    
     interest   FLOAT8,    
     interestpc   FLOAT8,    
     rnd   FLOAT8, 
     rndpc   FLOAT8,    
     lynchvalue   FLOAT8,    
     lynchmove   FLOAT8,    
     net_capital   FLOAT8,    
     net_capital_pc   FLOAT8,    
     rev_per_share   FLOAT8,    
     revpc   FLOAT8,    
     growth5y   FLOAT8,    
     growth1y   FLOAT8,        
     qtlyrev   FLOAT8,    
     qtlyrev_x4   FLOAT8,    
     tangible_book   FLOAT8,    
     tbookpc   FLOAT8,    
     zscore   FLOAT8,
     PRIMARY KEY (symbol));"""

# zacks
usstock_z_command: str = """CREATE TABLE usstock_z             
    ( zid  BIGSERIAL, 
     t   TIMESTAMP,                    
     td   DATE,        
     symbol   VARCHAR(10),         
     edate   DATE,        
     recom   FLOAT8,    
     eps   FLOAT8,    
     feps   FLOAT8,    
     eps12   FLOAT8,     
     rankno   INT,    
     rankstr   VARCHAR(15),         
     salesgrow   FLOAT8,    
     egrow   FLOAT8,    
     surprise   FLOAT8,    
     vgm   VARCHAR(1),         
     cashyield   FLOAT8,    
     peg   FLOAT8,    
     pb   FLOAT8,    
     pcf   FLOAT8,    
     pe   FLOAT8,    
     psales   FLOAT8,    
     earnyield   FLOAT8,    
     cash_per_share   FLOAT8,    
     chg1d   FLOAT8,    
     chg5d   FLOAT8,  
     chg1m   FLOAT8,    
     chg3m   FLOAT8,    
     chg1y   FLOAT8,
     PRIMARY KEY (symbol));"""


db_dict: Dict[str, Any] = {
    'fut_option': {'pk': ['symbol', 'td'], 'command': fut_option_command},
    'usstock_price': {'pk': ['symbol', 'td'], 'command': usstock_price_command},
    'usstock_tech': {'pk': ['symbol', 'td'], 'command': usstock_tech_command},
    'usstock_option': {'pk': ['symbol', 'td'], 'command': usstock_option_command},
    'usstock_g': {'pk': ['symbol'], 'command': usstock_g_command},
    'usstock_z': {'pk': ['symbol'], 'command': usstock_z_command},
}

def describe_table(table: str) -> None:
    try:
        sql: str = f"SELECT column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}';"
        df: DataFrame = pd.read_sql(sql, con=cnx)
        print(df)
    except Exception as e:
        print(e)

def show_single_table() -> None:
    while True:
        show_tables()
        table: str = input('Input table name (0 to quit): ')
        if table == '0':
            break
        elif table in db_dict:
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

def create_table(table:str) -> None:
    if table in db_dict:
        db_exec(db_dict[table].get('command'), con=cnx)
        describe_table(table)
    else:
        print('invalid table name')



def create_db():
    dbname = input('Please input the desired database name then press ENTER: ')
    reply = input(f'Do you want to create a database - {dbname} (y/N)? ')
    if reply == 'y':
        cmd1 = f'createdb {dbname} -U postgres'
        subprocess.run(cmd1, stdin=True, shell=True)
        print('Created a database --', dbname)
    else:
        print('no database is created')


def drop_table():
    while True:
        table: str = input("\n\nWhich table do you want to DROP? input the table name or '0' to cancel: ")
        if table == '0':
            break
        elif table in db_dict:
            sql: str = f'DROP TABLE {table};'
            db_exec(sql, con=cnx)
        else:
            print('invalid table name')


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
    print(usstock_price_command)
    print('done')