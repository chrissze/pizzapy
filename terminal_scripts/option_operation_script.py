"""

"""

# STANDARD LIBS
import sys; sys.path.append('..')
from typing import Any, Dict, List


# PROGRAM MODULES
from stock_option_update.option_update_database_model import upsert_option, upsert_options_by_terminal

from database_update.stock_list_model import all_stocks, get_sp_500, get_nasdaq_100, get_sp_nasdaq

from database_update.postgres_read_model import view_vertical_terminal



def browse_option_loop() -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_vertical_terminal()
    """
    while True:
        symbol: str = input('\n\nWhich symbol do you want to check (input * before the symbol to update, input 0 to quit)? ')
        SYMBOL: str = symbol.upper()
        if SYMBOL[:1] == '*' and SYMBOL[1:] in all_stocks:
            revised_symbol = SYMBOL[1:]
            upsert_result: str = upsert_option(revised_symbol)
            print(upsert_result)
            view_vertical_terminal(symbol=revised_symbol, table='stock_option')
        elif symbol == '0':
            break
        elif SYMBOL in all_stocks:
            view_vertical_terminal(symbol=SYMBOL, table='stock_option')
        else:
            print('you have entered an invalid symbol')




def update_option_loop() -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_vertical_terminal()
    """
    while True:
        symbol: str = input('\n\nWhich symbol do you want to UPDATE (input 0 to quit)? ')
        SYMBOL: str = symbol.upper()
        if SYMBOL in all_stocks:
            upsert_result: str = upsert_option(SYMBOL)
            print(upsert_result)
            print('\n\n\n')
            view_vertical_terminal(symbol=SYMBOL, table='stock_option')
        elif symbol == '0':
            break
        else:
            print('you have entered an invalid symbol')




def update_option_list(symbol_list: List[str]) -> None:
    """
    * INDEPENDENT *
    IMPORTS: upsert_options_by_terminal()
    """
    number_of_stocks: int = len(symbol_list)

    reply: str = input(f'\n\nAre you really want to UPDATE {number_of_stocks} stocks to stock_option table (yes/no)? ')
    REPLY: str = reply.upper()
    if REPLY == 'YES':
        upsert_options_by_terminal(symbol_list)
    else:
        print('Stock list update cancelled.')







option_menu_text: str = """\n\n
        Which action do you want to do? 
                    
        Single stock operations:        
        1)  Browse a stock's option data (loop)
        2)  Update a stock's option data (loop)
        
        List operations:        
        10) Update option data for S&P 500 
        11) Update option data for Nasdaq 100
        12) Update option data for S&P 500 + Nasdaq 100
        
        0)  quit
        Choose your action: """



option_actions_dict: Dict[str, Any] = {
        '1': lambda: browse_option_loop(),
        '2': lambda: update_option_loop(),
        '10': lambda: update_option_list(get_sp_500()),
        '11': lambda: update_option_list(get_nasdaq_100()),
        '12': lambda: update_option_list(get_sp_nasdaq()),

    }



def operate_stock_option():
    while True:
        ans = input(option_menu_text)
        if ans in option_actions_dict:
            option_actions_dict[ans]()
        elif ans == '0':
            break
        else:
            print('invalid input')





if __name__ == '__main__':
    operate_stock_option()





