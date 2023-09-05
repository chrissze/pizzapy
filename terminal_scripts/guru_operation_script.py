"""

"""

# STANDARD LIBS
import sys; sys.path.append('..')
import subprocess
from typing import Any, Dict, List

# THIRD PARTY LIB
import pandas
from pandas import DataFrame, Series


# PROGRAM MODULES
from stock_guru_update.guru_update_database_model import upsert_guru, upsert_gurus_by_terminal

from database_update.stock_list_model import all_stocks, get_sp_500, get_nasdaq_100, get_sp_nasdaq
from database_update.postgres_command_model import db_table_command_dict
from database_update.postgres_connection_model import execute_pandas_read

from database_update.postgres_read_model import view_symbol_row_terminal



def browse_guru_loop() -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_symbol_row_terminal()
    """
    while True:
        symbol: str = input('\n\nWhich symbol do you want to check (input * before the symbol to update, input 0 to quit)? ')
        SYMBOL: str = symbol.upper()
        if SYMBOL[:1] == '*' and SYMBOL[1:] in all_stocks:
            revised_symbol = SYMBOL[1:]
            upsert_result: str = upsert_guru(revised_symbol)
            print(upsert_result)
            view_symbol_row_terminal(symbol=revised_symbol, table='stock_guru')
        elif symbol == '0':
            break
        elif SYMBOL in all_stocks:
            view_symbol_row_terminal(symbol=SYMBOL, table='stock_guru')
        else:
            print('you have entered an invalid symbol')




def update_guru_loop() -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_symbol_row_terminal()
    """
    while True:
        symbol: str = input('\n\nWhich symbol do you want to UPDATE (input 0 to quit)? ')
        SYMBOL: str = symbol.upper()
        if SYMBOL in all_stocks:
            upsert_result: str = upsert_guru(SYMBOL)
            print(upsert_result)
            print('\n\n\n')
            view_symbol_row_terminal(symbol=SYMBOL, table='stock_guru')
        elif symbol == '0':
            break
        else:
            print('you have entered an invalid symbol')




def update_guru_list(symbol_list: List[str]) -> None:
    """
    * INDEPENDENT *
    IMPORTS: upsert_gurus_by_terminal()
    """
    number_of_stocks: int = len(symbol_list)

    reply: str = input(f'\n\nAre you really want to UPDATE {number_of_stocks} stocks to stock_guru table (yes/no)? ')
    REPLY: str = reply.upper()
    if REPLY == 'YES':
        upsert_gurus_by_terminal(symbol_list)
    else:
        print('Stock list update cancelled.')







guru_menu_text: str = """\n\n
        Which action do you want to do? 
                    
        Single stock operations:        
        1)  Browse a stock's guru data (loop)
        2)  Update a stock's guru data (loop)
        
        List operations:        
        10) Update guru data for S&P 500 
        11) Update guru data for Nasdaq 100
        12) Update guru data for S&P 500 + Nasdaq 100
         

        
        0)  quit
        Choose your action: """



guru_actions_dict: Dict[str, Any] = {
        '1': lambda: browse_guru_loop(),
        '2': lambda: update_guru_loop(),
        '10': lambda: update_guru_list(get_sp_500()),
        '11': lambda: update_guru_list(get_nasdaq_100()),
        '12': lambda: update_guru_list(get_sp_nasdaq()),

    }



def operate_stock_guru():
    while True:
        ans = input(guru_menu_text)
        if ans in guru_actions_dict:
            guru_actions_dict[ans]()
        elif ans == '0':
            break
        else:
            print('invalid input')





if __name__ == '__main__':
    operate_stock_guru()





