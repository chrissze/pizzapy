"""
* INDEPENDENT MODULE *

USED BY:
    guru_stock_update/

This module contains variables and dictionaries only, line below is for copy and paste:

                guru_stock_create_table_command, zacks_stock_create_table_command, stock_option_create_table_command, stock_price_create_table_command, stock_technical_create_table_command, futures_option_create_table_command


I cannot place postgres execution functions in this module, as it will led to circular imports.

"""

# STANDARD LIB

import json
from typing import Any, Dict


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






#ino
futures_option_create_table_command: str = """CREATE TABLE IF NOT EXISTS futures_option (
    id  BIGSERIAL, 
    t   TIMESTAMP,                    
    td   DATE  NOT NULL,        
    symbol   VARCHAR(10) NOT NULL,         
    cap_str   VARCHAR(15),         
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
    );
    """




# This dictionary can be used to compose upsert commands
# option, price and technicals are from yahoo
table_list_dict: Dict[str, Any] = {
    'guru_stock': {'primary_key_list': ['symbol'], 'command': guru_stock_create_table_command},
    'zacks_stock': {'primary_key_list': ['symbol'], 'command': zacks_stock_create_table_command},
    'stock_option': {'primary_key_list': ['symbol', 'td'], 'command': stock_option_create_table_command},
    'stock_price': {'primary_key_list': ['symbol', 'td'], 'command': stock_price_create_table_command},
    'stock_technical': {'primary_key_list': ['symbol', 'td'], 'command': stock_technical_create_table_command},
    'technical_one': {'primary_key_list': ['symbol'], 'command': technical_one_create_table_command},
    #'futures_option': {'primary_key_list': ['symbol', 'td'], 'command': futures_option_create_table_command},
}




if __name__ == '__main__':
    print('done')
