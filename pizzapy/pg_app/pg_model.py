"""
* INDEPENDENT MODULE *

USED BY:
    pg_cli.py



BEWARE:
- postgres execution functions led to circular imports.

"""

# STANDARD LIB
import asyncio
import json

from typing import Any


# THIRD PARTY LIB
import asyncpg

from asyncpg import Record

from pandas import DataFrame







########################################
# CONSTANTS - PG CREATE TABLE COMMANDS #
########################################



guru_stock_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS guru_stock (
    guru_id BIGSERIAL, 
    t   TIMESTAMP,                    
    td   DATE,              
    symbol   VARCHAR(10),         

    price   FLOAT8,
    cap   FLOAT8,    
    cap_str   VARCHAR(15),

    book_value   FLOAT8,
    book_value_pc   FLOAT8,
    buyback_yield   FLOAT8,

    debt_per_share   FLOAT8,    
    debt_pc   FLOAT8,
    dividend_yield   FLOAT8,
    earn_per_share   FLOAT8,
    earn_pc   FLOAT8,
    earn_yield   FLOAT8,
    fcf_yield   FLOAT8,

    interest   FLOAT8,
    interest_pc   FLOAT8,  

    equity   FLOAT8,    
    equity_pc   FLOAT8,  

    lynch   FLOAT8,    
    lynch_move_pc   FLOAT8,    

    net_capital   FLOAT8,    
    net_capital_pc   FLOAT8, 

    net_margin   FLOAT8, 

    nocapz   FLOAT8,
    pay_debt_yield   FLOAT8,
    payout_yield   FLOAT8,

    research   FLOAT8, 
    research_pc   FLOAT8,    
    
    revenue_per_share   FLOAT8,    
    revenue_pc   FLOAT8,    
    rev_growth_1y   FLOAT8,    
    rev_growth_3y   FLOAT8,        
    rev_growth_5y   FLOAT8,    
    rev_growth_10y   FLOAT8,

    roic   FLOAT8,

    shareholder_yield   FLOAT8,

    strength   FLOAT8,
    x1   FLOAT8,
    x2   FLOAT8,
    x3   FLOAT8,
    x4   FLOAT8,
    x5   FLOAT8,
    wacc   FLOAT8,

    year1z   FLOAT8,
    year2z   FLOAT8,
    year3z   FLOAT8,


    z1   FLOAT8,
    z2   FLOAT8,
    z3   FLOAT8,
    z4   FLOAT8,
    z5   FLOAT8,
    zscore   FLOAT8,
    
    wealth_pc   FLOAT8,  
    PRIMARY KEY (symbol)
    );
    """


zacks_stock_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS zacks_stock ( 
    zacks_id  BIGSERIAL, 
    t   TIMESTAMP,                    
    td   DATE,        
    symbol   VARCHAR(10),
             
    next_earning_date   DATE,        
    broker_rating   FLOAT8,    
    eps   FLOAT8,    
    forward_eps   FLOAT8,    
    diluted_eps_ttm   FLOAT8,
        
    average_grade   VARCHAR(1),         
    value_grade   VARCHAR(1),         
    growth_grade   VARCHAR(1),         
    momentum_grade   VARCHAR(1),         
    
    pe   FLOAT8,    
    earning_yield   FLOAT8,    
    pe_growth_ratio   FLOAT8,    
    psales   FLOAT8,    
    pbook   FLOAT8,    
    pcashflow   FLOAT8,    
    profit_margin   FLOAT8,    
    cash_pc   FLOAT8,    
    
    chg_1d   FLOAT8,    
    chg_5d   FLOAT8,  
    chg_1m   FLOAT8,    
    chg_3m   FLOAT8,    
    chg_1y   FLOAT8,
    PRIMARY KEY (symbol)
    )
    """


# yahoo
stock_price_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS stock_price (
    price_id  BIGSERIAL, 
    t   TIMESTAMP,                    
    symbol   VARCHAR(10) NOT NULL,         
    td   DATE NOT NULL,  
    open   FLOAT8,    
    high   FLOAT8,
    low   FLOAT8,    
    close   FLOAT8 NOT NULL,    
    adjclose  FLOAT8 NOT NULL,    
    volume BIGINT,    
    PRIMARY KEY (symbol, td) 
    );
    """

# from stock_price
stock_technical_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS stock_technical (
    id  BIGSERIAL, 
    t   TIMESTAMP,                    
    symbol   VARCHAR(10),         
    td   DATE,  

    ma20  FLOAT8,
    ma50  FLOAT8,
    ma250  FLOAT8,
    steep20  FLOAT8,
    steep50  FLOAT8,
    steep250  FLOAT8,
    ma50_distance  FLOAT8,
    ma250_distance  FLOAT8,

    rsi  FLOAT8,        
    weekly_rsi  FLOAT8,        
    is_top  SMALLINT,
    is_bottom  SMALLINT,

    price   FLOAT8,    
    p20   FLOAT8,
    p50   FLOAT8,    
    p100   FLOAT8,    
    p200  FLOAT8,        
    p500  FLOAT8,

    increase20  FLOAT8,        
    decrease20  FLOAT8,        
    increase50  FLOAT8,        
    decrease50  FLOAT8,

    best20  FLOAT8,        
    worst20  FLOAT8,        
    best50  FLOAT8,        
    worst50  FLOAT8,

    gain20  FLOAT8,        
    fall20  FLOAT8,        
    gain50  FLOAT8,        
    fall50  FLOAT8,

    PRIMARY KEY (symbol, td) 
    )
    """


# 
technical_one_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS technical_one (
    id  BIGSERIAL, 
    t   TIMESTAMP,                    
    symbol   VARCHAR(10),         
    td   DATE,  

    ma20  FLOAT8,
    ma50  FLOAT8,
    ma250  FLOAT8,
    steep20  FLOAT8,
    steep50  FLOAT8,
    steep250  FLOAT8,
    ma50_distance  FLOAT8,
    ma250_distance  FLOAT8,

    rsi  FLOAT8,        
    weekly_rsi  FLOAT8,        
    is_top  SMALLINT,
    is_bottom  SMALLINT,

    price   FLOAT8,    
    p20   FLOAT8,
    p50   FLOAT8,    
    p100   FLOAT8,    
    p200  FLOAT8,        
    p500  FLOAT8,

    increase20  FLOAT8,        
    decrease20  FLOAT8,        
    increase50  FLOAT8,        
    decrease50  FLOAT8,

    best20  FLOAT8,        
    worst20  FLOAT8,        
    best50  FLOAT8,        
    worst50  FLOAT8,

    gain20  FLOAT8,        
    fall20  FLOAT8,        
    gain50  FLOAT8,        
    fall50  FLOAT8,

    PRIMARY KEY (symbol) 
    )
    """


# nasdaq or barchart
stock_option_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS stock_option (
    option_id  BIGSERIAL, 
    t   TIMESTAMP,                    
    td   DATE  NOT NULL,        
    symbol   VARCHAR(10) NOT NULL,         
    cap_str   VARCHAR(15),         
    cap   FLOAT8,    
    price   FLOAT8,    
    call_money   FLOAT8,    
    put_money   FLOAT8,  
    call_oi   FLOAT8,  
    put_oi   FLOAT8,  
    call_ratio   FLOAT8,    
    put_ratio   FLOAT8,    

    call_otm_ratio   FLOAT8,    
    call_itm_ratio   FLOAT8,    
    put_otm_ratio   FLOAT8,    
    put_itm_ratio   FLOAT8,    

    call_pc   FLOAT8,    
    put_pc   FLOAT8,    
    PRIMARY KEY (symbol, td) 
    )
    """







# This dictionary can be used to compose upsert commands
# option, price and technicals are from yahoo
table_list_dict: dict[str, Any] = {
    'guru_stock': {'primary_key_list': ['symbol'], 'command': guru_stock_create_table_command},
    'zacks_stock': {'primary_key_list': ['symbol'], 'command': zacks_stock_create_table_command},
    'stock_option': {'primary_key_list': ['symbol', 'td'], 'command': stock_option_create_table_command},
    'stock_price': {'primary_key_list': ['symbol', 'td'], 'command': stock_price_create_table_command},
    'stock_technical': {'primary_key_list': ['symbol', 'td'], 'command': stock_technical_create_table_command},
}

##################
# CLI FUNCTIONS  #
##################





async def create_table(table_name:str) -> None:
    """
    DEPENDS ON: show_table(), show_tables()
    IMPORTS: table_list_dict, execute_psycopg_command()
    """
    if table_name in table_list_dict:

        cmd: str = table_list_dict[table_name].get('command')
        try:
            conn = await asyncpg.connect()

            result = await conn.execute(cmd)

            print(result)

            await conn.close()
        except Exception as e:
            print(e)
    
        try:
            print('\nLatest available tables in Postgresql database: \n')
            await print_tables()
        except Exception as e:
            print(e)
    
    else:
        print(f"\nYour input `{table_name}` is not in table_list_dict")






async def get_databases() -> Any:
    """
    * INDEPENDENT *
    IMPORTS: asyncpg

    """
    cmd: str = "SELECT datname FROM pg_database WHERE datistemplate = false"
    try:
        conn = await asyncpg.connect()
        databases: list[Record] = await conn.fetch(cmd)
    finally:
        await conn.close()    
    
    return databases




async def print_databases() -> str:
    databases: list[Record] = await get_databases()

    for db in databases:
        db_dict: dict = dict(db)
        print(db_dict.get('datname'))







async def get_tables() -> list[Record]:
    """
    * INDEPENDENT *
    IMPORTS: asyncpg

    """
    cmd = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    try:
        conn = await asyncpg.connect()
        tables: list[Record] = await conn.fetch(cmd)
        await conn.close()    
    except Exception as e:
        return []
    
    return tables



async def print_tables() -> None:
    tables: list[Record] = await get_tables()

    for table in tables:
        print(table.get('table_name'))



async def get_table_columns(table_name: str) -> list[Record]:
    """
    * INDEPENDENT *
    IMPORTS: 
    
    {table_name} in the cmd needs to be single quoted. Semicolon at the end is optional.
    
    full_cmd: str = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"

    empty tables without any column will have empty dataframe result.
    """
    
    cmd: str = f"SELECT column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"
    try:
        conn = await asyncpg.connect()
        records: list[Record] = await conn.fetch(cmd)
        await conn.close()    
    except Exception as e:
        print(e)
    
    return records




async def print_table_columns() -> None:
    """
    df = DataFrame(dict(x) for x in records)      # handle edge cases better
    df = DataFrame(records)
    """
    
    await print_tables()

    table_name: str = input("\nInput a TABLE NAME to print details or '0' to cancel: ")
    
    if table_name in table_list_dict:
        records: list[Record] = await get_table_columns(table_name)
    else:
        print(f'Table name `{table_name}` is not in table_list_dict')
        return
    
    df = DataFrame(records)

    print(df)




    



async def get_current_db() -> str:
    """
    * INDEPENDENT *
    IMPORTS: asyncpg

    """

    cmd: str = "SELECT current_database();"
    try:
        conn = await asyncpg.connect()
        current_db = await conn.fetchval(cmd)
    finally:
        await conn.close()    
    
    return current_db



async def print_current_db() -> str:
    current_db = await get_current_db()

    print(current_db, type(current_db))



async def drop_pg_table() -> None:
    """
    DEPENDS ON: show_tables()
    IMPORTS:  table_list_dict, execute_psycopg_command()
    """
    
    table_name: str = input("\nWhich table do you want to DROP? Input the TABLE NAME or '0' to cancel: ")
    
    cmd: str = f'DROP TABLE IF EXISTS {table_name};'
    
    if table_name == '0':
        return
    elif table_name in table_list_dict:
        reply = input(f"\nYou are going to DROP TABLE '{table_name}', it is a CRITICAL TABLE in table_list_dict, do you really want to drop this table (y/N)?")
        if reply == 'y':
            try:
                conn = await asyncpg.connect()
                result = await conn.execute(cmd)
                print(result)
                await conn.close()
            except Exception as e:
                print(e)
        else:
            print('Abort drop table')
    else:
        print(f'Invalid table name: {table_name}')











if __name__ == '__main__':
    asyncio.run(print_current_db())
    asyncio.run(print_tables())
    asyncio.run(print_databases())
    asyncio.run(drop_pg_table())
    print('done')
