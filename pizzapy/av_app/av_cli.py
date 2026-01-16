
"""
DEPENDS: av_model.py

USED BY: 

"""

# STANDARD LIBS
import asyncio

from typing import Any

# PROGRAM MODULES

from pizzapy.av_app.av_model import upsert_av_option, upsert_av_options, upsert_interval_option, upsert_prices

from pizzapy.pg_app.pg_model import print_latest_row, get_nasdaq_100, get_sp_500, get_sp_nasdaq



######################
###  STOCK OPTION  ###
######################


TABLE: str = 'stock_option'


async def browse_upsert_option_interactive() -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_vertical_terminal()
    USED BY: make_actions_dict()
    """

    
    while True:
        symbol: str = input(f'\n\nWhich SYMBOL do you want to check from {TABLE} (input * before the symbol to update, input 0 to quit)? ')

        if symbol == '0':
            break
        
        SYMBOL: str = symbol.upper()
        
        if SYMBOL[:1] == '*':
            revised_symbol = SYMBOL[1:]
            result: str = await upsert_av_option(revised_symbol)
            print(result)
            await print_latest_row(revised_symbol, TABLE)

        else:
            await print_latest_row(SYMBOL, TABLE)


async def browse_upsert_interval_option_interactive() -> None:
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
            
            interval: str = input(f"\n\nWhich interval? 'monthly' (default), 'fortnite', 'weekly', 'daily'")
        
            if interval not in ['fortnite', 'weekly', 'daily']:
                interval = 'monthly'
            
            result: str = await upsert_interval_option(revised_symbol, interval=interval)
            print(result)
            await print_latest_row(revised_symbol, TABLE)

        else:
            await print_latest_row(SYMBOL, TABLE)





async def upsert_options_interactive(stock_list: list[str]) -> None:
    """
    DEPENDS ON: upsert_av_options()
    
    """
    length: int = len(stock_list)
    reply: str = input(f'\n\nAre you really want to UPSERT {length} stocks to {TABLE} TABLE (yes/no)? ')
    REPLY: str = reply.lower()
    if REPLY == 'yes':
        await upsert_av_options(stock_list)
    else:
        print(f'{TABLE} - {length} stocks upsert cancelled.')


######################
###  STOCK PRICE  ###
######################


async def browse_upsert_price_interactive() -> None:
    """
    DEPENDS: upsert_prices
    
    IMPORTS: print_latest_row()

    USED BY: make_actions_dict()
    """
    table: str = 'stock_price'
    
    while True:
        symbol: str = input(f'\n\nWhich SYMBOL do you want to check from {table} (input * before the symbol to update, input 0 to quit)? ')

        if symbol == '0':
            break
        
        SYMBOL: str = symbol.upper()
        
        if SYMBOL[:1] == '*':
            revised_symbol = SYMBOL[1:]
            result: str = await upsert_prices([revised_symbol])
            print(result)
            await print_latest_row(revised_symbol, table)

        else:
            await print_latest_row(SYMBOL, table)

















def make_text_menu(table: str) -> str:
    """
    * INDEPENDENT *
    USED BY: operate_table()
    """
    menu: str = f"""\n\n
        Which action do you want to do? 
                    
        Single stock operations:        
        1)  Browse or upsert stock_option (loop)
        2)  Browse or upsert interval option (loop)
        4)  Browse or upsert stock_price (loop)
        
        List operations:        
        12) Upsert {table} for S&P 500 
        13) Upsert {table} for Nasdaq 100
        14) Upsert {table} for S&P 500 + S&P 400 + Nasdaq 100
        
        0)  quit
        Choose your action: """
    return menu


action_dict: dict[str, Any] = {
    '1': lambda: asyncio.run(browse_upsert_option_interactive()),

    '2': lambda: asyncio.run(browse_upsert_interval_option_interactive()),
    '4': lambda: asyncio.run(browse_upsert_price_interactive()),

    '12': lambda: asyncio.run(upsert_options_interactive(get_sp_500())),
    '13': lambda: asyncio.run(upsert_options_interactive(get_nasdaq_100())),
    '14': lambda: asyncio.run(upsert_options_interactive(get_sp_nasdaq())),
    }


def av_cli(): 
    """
    DEPENDS ON: make_text_menu, action_dict
    """
    while True:
        ans: str = input(make_text_menu(TABLE))
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
