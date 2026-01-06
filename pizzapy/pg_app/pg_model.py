"""
* INDEPENDENT MODULE *

USED BY:
    pg_cli.py



BEWARE:
- postgres execution functions led to circular imports.



"""

# STANDARD LIB
import asyncio

from timeit import timeit
from typing import Any, List, Set


# THIRD PARTY LIB
import asyncpg

from asyncpg import Record

import pandas as pd

# PROGRAM MODULES
from dimsumpy.web.crawler import get_html_dataframes, get_html_soup

from pizzapy.pg_app.computer_generated_model import nasdaq_100_stocks, sp_400_stocks, sp_500_stocks, sp_nasdaq_stocks

####################################
# COMPUTER GENERATED FILE IMPORTS  #
####################################

# STANDARD LIBS

from datetime import datetime
from io import StringIO
import re
import subprocess
from timeit import timeit
from typing import Any
import urllib.request as request


# THIRD PARTY LIBS
from bs4 import BeautifulSoup, ResultSet

#import pandas as pd

from pandas import DataFrame

# CUSTOM LIBS
from dimsumpy.web.crawler import get_html_dataframes, get_html_soup











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
    call_money_ratio   FLOAT8,    
    put_money_ratio   FLOAT8,    

    call_itm_premium_ratio   FLOAT8,    
    call_otm_premium_ratio   FLOAT8,    
    put_itm_premium_ratio   FLOAT8,    
    put_otm_premium_ratio   FLOAT8,    

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


# need to comment out all_stocks when I use code to generate 
all_stocks: list[str] = sp_nasdaq_stocks + ['FNMA', 'FMCC']

stock_list_dict: dict[str, list[str]] = {
    f'Nasdaq 100 ({len(nasdaq_100_stocks)})': nasdaq_100_stocks,
    f'S&P 500 ({len(sp_500_stocks)})': sp_500_stocks,
    f'S&P 400 ({len(sp_400_stocks)})': sp_400_stocks,
    f'S&P 500, 400 + Nasdaq 100 ({len(sp_nasdaq_stocks)})': sp_nasdaq_stocks,
    f'All Stocks ({len(all_stocks)})': all_stocks,
}


##################
# CLI FUNCTIONS  #
##################





async def create_table(table_name:str) -> None:
    """
    DEPENDS ON: show_table(), show_tables()
    IMPORTS: table_list_dict, execute_psycopg_command()
    """

    tables: list[Record] = await get_tables()

    existing_tables: list[str] = [x.get('table_name') for x in tables]

    if table_name in existing_tables:
        print(f'{table_name} already exists, no action.')
        return

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

    for i, table in enumerate(tables, start=1):
        print(i, table.get('table_name'))



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
    
    tables: list[Record] = await get_tables()

    tables_len: int = len(tables)

    await print_tables()


    table_num: str = input("\nInput a TABLE NUMBER to print details or '0' to cancel: ")

    try:
        ind = int(table_num) - 1
        
        if ind == -1:        # User entered '0'
            return
        elif ind >= 0 and ind < tables_len: 
            table_name: str = tables[ind].get('table_name')
        else:
            print(f'\nYou have entered an invalid number: {table_num}')
            return

    except Exception as e:
        print(e)
        return

    if table_name in table_list_dict:
        records: list[Record] = await get_table_columns(table_name)
    else:
        print(f'Table name `{table_name}` is not in table_list_dict')
        return
    
    df = pd.DataFrame(dict(x) for x in records)
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



async def drop_table() -> None:
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





####################################
### COMPUTER GENERATED FUNCTIONS ###
####################################

bank_stocks: list[str] = ['ASB', 'BAC', 'BK', 'C', 'CADE', 'CBSH', 'CFG', 'CFR', 'CMA', 'COF', 'COLB', 'DFS', 'EWBC', 'FFIN', 'FHN', 'FITB', 'FNB', 'GBCI', 'GS', 'HOMB', 'HWC', 'IBOC', 'JPM', 'HBAN', 'MS', 'MTB', 'NTRS', 'NYCB', 'KEY', 'ONB', 'OZK', 'PB', 'PNC', 'PNFP', 'RF', 'SCHW', 'SNV', 'SSB', 'STT', 'SYF', 'TCBI', 'TFC', 'UBSI', 'UMBF', 'USB', 'VLY', 'WBS', 'WFC', 'WTFC', 'ZION']

bank_stocks_set: set[str] = set(bank_stocks)



def get_sp_400() -> dict:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy
    execution time: 1 second
    """
    sp_400_url: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_400_companies'
    dfs: list[DataFrame] = get_html_dataframes(sp_400_url)
    df = dfs[0]
    df.columns = ['Symbol', 'Company', 'Sector', 'Industry', 'Headquarters', 'Filing']
    stocks_dict = df.set_index('Symbol').to_dict(orient='index')
    return stocks_dict


def get_sp_500() -> dict:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy
    execution time: 1 second

    The S&P 500 index undergoes a quarterly rebalancing to ensure it accurately reflects the U.S. large-cap equity market. These rebalancing events typically occur after third Friday of March, June, September, and December. 
    """
    sp_500_url: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    dfs: list[DataFrame] = get_html_dataframes(sp_500_url)
    df = dfs[0]
    df.columns = ['Symbol', 'Company', 'Sector', 'Industry', 'Headquarters', 'Added', 'CIK', 'Founded']
    stocks_dict = df.set_index('Symbol').to_dict(orient='index')
    return stocks_dict



def get_nasdaq_100() -> list[str]:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy
    execution time: 1 second

    Note: 
    I could not simply use get_html_dataframes() in this function, the html source structure is different.

    Nasdaq-100 Index undergoes an annual reconstitution in year end, usually November and December.
    2023 Additions: TTWO (20231218)
    2024 Additions: APP(20241118), PLTR(20241126)


    """
    nasdaq_100_url: str = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    soup: BeautifulSoup = get_html_soup(nasdaq_100_url)
    soup_item: ResultSet = soup.find('table', id='constituents')
    dfs: list[DataFrame] = pd.read_html(StringIO(str(soup_item)), header=0)
    df = dfs[0]
    df.columns = ['Ticker', 'Company', 'Industry', 'Sector']
    stocks_dict = df.set_index('Ticker').to_dict(orient='index')
    return stocks_dict
#    stock_list: list[str] = list(stocks_dict.keys())
#    return stock_list



def get_sp_nasdaq() -> list[str]:
    """
    DEPENDS ON: get_sp_500(), get_nasdaq_100()
    USED BY: guru_operation_script.py

    The result is not including bank stocks.
    """
    sp_500_stocks: List[str] = list(get_sp_500().keys())
    sp_400_stocks: List[str] = list(get_sp_400().keys())
    nasdaq_100_stocks: List[str] = list(get_nasdaq_100().keys())
    sp_nasdaq_set: Set[str] = set(sp_500_stocks + sp_400_stocks + nasdaq_100_stocks)
    sp_nasdaq_stocks: List[str] = sorted(list(sp_nasdaq_set - bank_stocks_set))
    return sp_nasdaq_stocks






def get_option_traded() -> list[str]:
    """
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    execution time: 2 minutes
    file size is about 50mb, need several minutes to process, unique symbols are about 3129
    """
    url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/options.txt'
    with request.urlopen(url1) as r:
        text = r.read().decode()
    df_nasdaq: DataFrame = pd.read_csv(StringIO(text), sep='|', header=0)

    stocks: list[str] = list(df_nasdaq.iloc[:-1, 0])

    # There is some floats value in `stocks` variable, if I don't filtered it to make it str only,
    # sorted function in the next line will have errors.
    # df_nasdaq.to_csv("output.csv", index=False)
    filtered_stocks : list[str] = [x for x in set(stocks) if isinstance(x, str)]

    option_stocks: list[str] = sorted(filtered_stocks)

    return option_stocks



def prepare_stock_list_file_content() -> str:
    """
    DEPENDS ON: get_sp_500(), get_sp_nasdaq(), get_nasdaq_100(),  get_nasdaq_listed(), get_nasdaq_traded(), get_option_traded()
    IMPORTS: datetime
    USED BY: generate_stock_list_file() 

    when I replace string BY re or replace('nan,', 'None,'), it will miss some items with special comma char, so I have to use ': nan'
    """
    current_time: datetime = datetime.now().replace(second=0, microsecond=0)
    file_comment: str = f'""" THIS FILE IS GENERATED AT {current_time} BY generate_stock_list_file() FUNCTION IN generate_file_model.py """'

    sp_500_dict: dict =  get_sp_500()
    sp_500_dict_comment: str = f'# {len(sp_500_dict)}'
    sp_500_raw_string: str = f'sp_500_dict: dict = {sp_500_dict}'
    sp_500_dict_variable: str = re.sub(': nan', ': None', sp_500_raw_string)

    sp_400_dict: dict =  get_sp_400()
    sp_400_dict_comment: str = f'# {len(sp_400_dict)}'
    sp_400_raw_string: str = f'sp_400_dict: dict = {sp_400_dict}'
    sp_400_dict_variable: str = re.sub(': nan', ': None', sp_400_raw_string)

    nasdaq_100_dict: dict =  get_nasdaq_100()
    nasdaq_100_dict_comment: str = f'# {len(nasdaq_100_dict)}'
    nasdaq_100_dict_variable: str = f'nasdaq_100_dict: dict = {nasdaq_100_dict}'

    sp_500: list[str] =  list(sp_500_dict.keys())
    sp_500_comment: str = f'# {len(sp_500)}'
    sp_500_variable: str = f'sp_500_stocks: list[str] = {sp_500}'
    
    sp_400: list[str] =  list(sp_400_dict.keys())
    sp_400_comment: str = f'# {len(sp_400)}'
    sp_400_variable: str = f'sp_400_stocks: list[str] = {sp_400}'

    nasdaq_100: list[str] = list(nasdaq_100_dict.keys())
    nasdaq_100_comment: str = f'# {len(nasdaq_100)}'
    nasdaq_100_variable: str = f'nasdaq_100_stocks: list[str] = {nasdaq_100}'

    sp_nasdaq: list[str] = get_sp_nasdaq()
    sp_nasdaq_comment: str = f'# {len(sp_nasdaq)}'
    sp_nasdaq_variable: str = f'sp_nasdaq_stocks: list[str] = {sp_nasdaq}'

    #option_traded: list[str] = get_option_traded()
    #option_traded_comment: str = f'# {len(option_traded)}'
    #option_traded_variable: str = f'option_traded_stocks: list[str] = {option_traded}'
    
    content: str = f'''
{file_comment}\n\n


{sp_500_dict_comment}
{sp_500_dict_variable}\n\n

{sp_400_dict_comment}
{sp_400_dict_variable}\n\n

{nasdaq_100_dict_comment}
{nasdaq_100_dict_variable}\n\n

{sp_500_comment}
{sp_500_variable}\n\n

{sp_400_comment}
{sp_400_variable}\n\n

{nasdaq_100_comment}
{nasdaq_100_variable}\n\n

{sp_nasdaq_comment}
{sp_nasdaq_variable}\n\n
'''
    return content



def generate_stock_list_file() -> None:
    """
    DEPENDS ON: prepare_stock_list_file_content()
    USED BY: terminal_scripts/central_script.py

    execution time: 
    4 minutes if get_option_traded() is included.

    30s if get_option_traded() is excluded.
    
    When I re-run this file, it will overwrite the original content
    
    A "list of stocks" is data, so it belongs to the Model.

    """
    filename = 'computer_generated_model.py'
    
    print(f'Generating `{filename}` now ...')
    
    content: str = prepare_stock_list_file_content()
    
    with open(filename, 'w') as f:
        f.write(content)

    print(f'write {filename} done, now using black to format it according to PEP8...')
    
    black_cmd = f'black {filename}'
    
    subprocess.run(black_cmd, stdin=True, shell=True)
    
    print('ALL DONE')
    
    return None



def ask_generate_stock_list_file() -> None:
    def run() -> None:
        reply: str = input('Do you want to generate stock list module (yes/no)? ')
        if reply.lower() == 'yes': 
            x =  generate_stock_list_file()
            print(x)
        elif reply.lower() == 'no':
            print('No action')
        else:
            print(f'Invalid input `{reply}`. No action')

    seconds = timeit(run, number=1)
    print(seconds)
    
### END OF COMPUTER GENERATED FUNCTIONS ###





########################
### COMMON FUNCTIONS ###
########################


async def get_latest_row(symbol: str, table: str ) -> DataFrame:
    """
    * INDEPENDENT *
    IMPORTS: 
    USED BY: 
    
    Note:
    (1) the table name MUST be available in the database, otherwise there will be exception.
    (2) The symbol can be non-exist in the table, conn.fetch() returns an empty list [] if no rows match.


    """    
    cmd: str = f"SELECT * FROM {table} WHERE symbol = '{symbol}' ORDER BY t DESC"
    
    conn = await asyncpg.connect()
    
    rows: list[Record] = await conn.fetch(cmd)
    
    await conn.close()
    
    first_row_list: list[Record] = rows[:1]  # can be an empty list
    
    first_row_df: DataFrame = pd.DataFrame([dict(x) for x in first_row_list])
                
    df = first_row_df.T   # df can be an empty DataFrame

    return df       
    


### END OF COMMON FUNCTIONS ###



if __name__ == '__main__':
    ask_generate_stock_list_file()
    
    #xs = get_nasdaq_100()
    #print(xs) 



 



