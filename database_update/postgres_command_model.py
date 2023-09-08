"""
* INDEPENDENT MODULE *

USED BY: 
    guru_stock_update/

This module contains variables and dictionaries only, line below is for copy and paste:

                guru_stock_create_table_command, zacks_stock_create_table_command, stock_option_create_table_command, stock_price_create_table_command, stock_technical_create_table_command, futures_option_create_table_command,  table_list_dict

    
I cannot place postgres execution functions in this module, as it will led to circular imports.

"""

# STANDARD LIB
import sys; sys.path.append('..')
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
    growth5y   FLOAT8,    
    growth10y   FLOAT8,    
    
    strength   FLOAT8,    
    zscore   FLOAT8,
    
    wealth_pc   FLOAT8,  
    PRIMARY KEY (symbol)
    )
    """


zacks_stock_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS zacks_stock ( 
    zacks_id  BIGSERIAL, 
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
    )
    """


# yahoo
stock_price_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS stock_price (
    price_id  BIGSERIAL, 
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

# from stock_price
stock_technical_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS stock_tech (
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
stock_option_create_table_command: str = """
    CREATE TABLE IF NOT EXISTS stock_option (
    option_id  BIGSERIAL, 
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
    PRIMARY KEY (symbol, td) 
    )
    """






#ino
futures_option_create_table_command: str = """CREATE TABLE IF NOT EXISTS futures_option (
    id  BIGSERIAL, 
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
    'futures_option': {'primary_key_list': ['symbol', 'td'], 'command': futures_option_create_table_command},
}




if __name__ == '__main__':
    print('done')