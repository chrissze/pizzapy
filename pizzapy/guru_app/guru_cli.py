
"""
DEPENDS: guru_model.py

USED BY: 

"""

# STANDARD LIBS
import asyncio

from typing import Any

# PROGRAM MODULES

from pizzapy.guru_app.guru_model import print_guru_from_db, upsert_guru, upsert_gurus

from pizzapy.pg_app.computer_generated_model import nasdaq_100_stocks, sp_500_stocks, sp_nasdaq_stocks



TABLE: str = 'guru_stock'



async def browse_upsert_guru_interactive() -> None:
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
            result: str = await upsert_guru(revised_symbol)
            print(result)
            await print_guru_from_db(symbol=revised_symbol)

        else:
            await print_guru_from_db(symbol=SYMBOL)





async def upsert_gurus_interactive(stock_list: list[str]) -> None:
    """
    DEPENDS ON: upsert_av_options()
    
    """
    length: int = len(stock_list)
    reply: str = input(f'\n\nAre you really want to UPSERT {length} stocks to {TABLE} table (yes/no)? ')
    REPLY: str = reply.lower()
    if REPLY == 'yes':
        await upsert_gurus(stock_list)
    else:
        print(f'{TABLE} - {length} stocks upsert cancelled.')


















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
        2) Upsert {table} for S&P 500 
        3) Upsert {table} for Nasdaq 100
        4) Upsert {table} for S&P 500 + S&P 400 + Nasdaq 100
        
        0)  quit
        Choose your action: """
    return menu


action_dict: dict[str, Any] = {
    '1': lambda: asyncio.run(browse_upsert_guru_interactive()),
    '2': lambda: asyncio.run(upsert_gurus_interactive(sp_500_stocks)),
    '3': lambda: asyncio.run(upsert_gurus_interactive(nasdaq_100_stocks)),
    '4': lambda: asyncio.run(upsert_gurus_interactive(sp_nasdaq_stocks)),
    }


def guru_cli(): 
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
    guru_cli()
    print('DONE')
