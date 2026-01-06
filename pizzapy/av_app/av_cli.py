
"""
DEPENDS: av_model.py

USED BY: 

"""

# STANDARD LIBS
import asyncio

from typing import Any

# PROGRAM MODULES

from pizzapy.av_app.av_model import upsert_av_option






async def browse_upsert_option_interactive() -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_vertical_terminal()
    USED BY: make_actions_dict()
    """

    table: str = 'stock_option'
    
    while True:
        symbol: str = input(f'\n\nWhich SYMBOL do you want to check from {table} (input * before the symbol to update, input 0 to quit)? ')

        if symbol == '0':
            break
        
        SYMBOL: str = symbol.upper()
        
        if SYMBOL[:1] == '*':
            revised_symbol = SYMBOL[1:]
            result: str = await upsert_av_option(revised_symbol)
            print(result)
            view_vertical_terminal(symbol=revised_symbol, table=table)

        else:
            view_vertical_terminal(symbol=SYMBOL, table=table)



def make_text_menu(table: str) -> str:
    """
    * INDEPENDENT *
    USED BY: operate_table()
    """
    menu: str = f"""\n\n
        Which action do you want to do? 
                    
        Single stock operations:        
        1)  Browse or upsert {table} (loop)
        
        List operations:        
        10) Update {table} for S&P 500 
        11) Update {table} for Nasdaq 100
        12) Update {table} for S&P 500 + S&P 400 + Nasdaq 100
        
        0)  quit
        Choose your action: """
    return menu


action_dict: dict[str, Any] = {
    '1': lambda: asyncio.run(browse_upsert_option_interactive()),

    '4': lambda:  asyncio.run(),

    '5': lambda: asyncio.run(),

    
    }


def av_cli(): 
    """
    DEPENDS ON: make_text_menu, action_dict
    """
    table: str = 'stock_option'
    while True:
        ans: str = input(make_text_menu(table))
        if ans in action_dict:
            print()
            action_dict[ans]()
        elif ans == '0':
            break
        else:
            print(f'INVALID INPUT - {ans}')



if __name__ == '__main__':
    av_cli()
    print('DONE')
