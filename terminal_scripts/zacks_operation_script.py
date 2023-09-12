"""

"""

# STANDARD LIBS
import sys; sys.path.append('..')
from typing import Any, Dict, List


# PROGRAM MODULES
from zacks_stock_update.zacks_update_database_model import upsert_zacks, upsert_zackses_by_terminal

from database_update.stock_list_model import all_stocks, get_sp_500, get_nasdaq_100, get_sp_nasdaq

from database_update.postgres_read_model import view_vertical_terminal



def browse_zacks_loop() -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_vertical_terminal()
    """
    while True:
        symbol: str = input('\n\nWhich symbol do you want to check (input * before the symbol to update, input 0 to quit)? ')
        SYMBOL: str = symbol.upper()
        if SYMBOL[:1] == '*' and SYMBOL[1:] in all_stocks:
            revised_symbol = SYMBOL[1:]
            upsert_result: str = upsert_zacks(revised_symbol)
            print(upsert_result)
            view_vertical_terminal(symbol=revised_symbol, table='zacks_stock')
        elif symbol == '0':
            break
        elif SYMBOL in all_stocks:
            view_vertical_terminal(symbol=SYMBOL, table='zacks_stock')
        else:
            print('you have entered an invalid symbol')




def update_zacks_loop() -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_vertical_terminal()
    """
    while True:
        symbol: str = input('\n\nWhich symbol do you want to UPDATE (input 0 to quit)? ')
        SYMBOL: str = symbol.upper()
        if SYMBOL in all_stocks:
            upsert_result: str = upsert_zacks(SYMBOL)
            print(upsert_result)
            print('\n\n\n')
            view_vertical_terminal(symbol=SYMBOL, table='zacks_stock')
        elif symbol == '0':
            break
        else:
            print('you have entered an invalid symbol')




def update_zacks_list(symbol_list: List[str]) -> None:
    """
    * INDEPENDENT *
    IMPORTS: upsert_zackses_by_terminal()
    """
    number_of_stocks: int = len(symbol_list)

    reply: str = input(f'\n\nAre you really want to UPDATE {number_of_stocks} stocks to zacks_stock table (yes/no)? ')
    REPLY: str = reply.upper()
    if REPLY == 'YES':
        upsert_zackses_by_terminal(symbol_list)
    else:
        print('Stock list update cancelled.')







zacks_menu_text: str = """\n\n
        Which action do you want to do? 
                    
        Single stock operations:        
        1)  Browse a stock's zacks data (loop)
        2)  Update a stock's zacks data (loop)
        
        List operations:        
        10) Update zacks data for S&P 500 
        11) Update zacks data for Nasdaq 100
        12) Update zacks data for S&P 500 + Nasdaq 100
        
        0)  quit
        Choose your action: """



zacks_actions_dict: Dict[str, Any] = {
        '1': lambda: browse_zacks_loop(),
        '2': lambda: update_zacks_loop(),
        '10': lambda: update_zacks_list(get_sp_500()),
        '11': lambda: update_zacks_list(get_nasdaq_100()),
        '12': lambda: update_zacks_list(get_sp_nasdaq()),

    }



def operate_zacks_stock():
    while True:
        ans = input(zacks_menu_text)
        if ans in zacks_actions_dict:
            zacks_actions_dict[ans]()
        elif ans == '0':
            break
        else:
            print('invalid input')





if __name__ == '__main__':
    operate_zacks_stock()





