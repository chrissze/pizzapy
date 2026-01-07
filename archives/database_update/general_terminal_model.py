"""

USED BY: 
    terminal_scripts/zacks_operation_script.py,     
"""

# STANDARD LIBS

from time import sleep
from timeit import default_timer
from typing import Any, Dict, List, Optional, Tuple, Union


# THIRD PARTY LIBS

# CUSTOM LIBS
from batterypy.control.trys import try_str


# PROGRAM MODULES
from pizzapy.database_update.stock_list_model import all_stocks, table_function_dict
from pizzapy.database_update.postgres_read_model import view_vertical_terminal
from pizzapy.database_update.generated_stock_list import nasdaq_100_stocks, sp_500_stocks, sp_nasdaq_stocks, nasdaq_listed_stocks, nasdaq_traded_stocks



def upsert_symbols_terminal(table: str, symbols: List[str], delay=0) -> None:
    """
    IMPORTS: table_function_dict
    USED BY: upsert_symbols_interactive()
    """
    if table == 'stock_option':
        delay = 30 
    length: int = len(symbols)
    func = table_function_dict.get(table)
    for i, symbol in enumerate(symbols, start=1):
        result: str = try_str(func, symbol)
        output: str = f'{i} / {length} {symbol} {result}'
        print(output)
        sleep(delay)



def upsert_symbols_interactive(table: str, symbols: List[str]) -> None:
    """
    DEPENDS ON: upsert_symbols_terminal()
    USED BY: make_actions_dict()
    """
    length: int = len(symbols)
    reply: str = input(f'\n\nAre you really want to UPDATE {length} stocks to {table} table (yes/no)? ')
    REPLY: str = reply.upper()
    if REPLY == 'YES':
        upsert_symbols_terminal(table, symbols)
    else:
        print(f'{table} - {length} stocks update cancelled.')



def browse_symbol_loop(table: str) -> None:
    """
    * INDEPENDENT *
    IMPORTS: all_stocks, view_vertical_terminal()
    USED BY: make_actions_dict()
    """
    func = table_function_dict.get(table)
    while True:
        symbol: str = input(f'\n\nWhich SYMBOL do you want to check from {table} (input * before the symbol to update, input 0 to quit)? ')
        SYMBOL: str = symbol.upper()
        if SYMBOL[:1] == '*' and SYMBOL[1:] in all_stocks:
            revised_symbol = SYMBOL[1:]
            result: str = func(revised_symbol)
            print(result)
            view_vertical_terminal(symbol=revised_symbol, table=table)
        elif symbol == '0':
            break
        elif SYMBOL in all_stocks:
            view_vertical_terminal(symbol=SYMBOL, table=table)
        else:
            print(f'you have entered an invalid symbol - {symbol}')




def upsert_symbol_loop(table: str) -> None:
    """
    IMPORTS: all_stocks, table_function_dict, view_vertical_terminal()
    USED BY: make_actions_dict()
    """
    func = table_function_dict.get(table)
    while True:
        symbol: str = input(f'\n\nWhich SYMBOL do you want to UPSERT to {table} (input 0 to quit)? ')
        SYMBOL: str = symbol.upper()
        if SYMBOL in all_stocks:
            result: str = func(SYMBOL)
            print(result)
            print('\n\n\n')
            view_vertical_terminal(symbol=SYMBOL, table=table)
        elif symbol == '0':
            break
        else:
            print(f'You have entered an invalid symbol {symbol}')





def make_text_menu(table: str) -> str:
    """
    * INDEPENDENT *
    USED BY: operate_table()
    """
    menu: str = f"""\n\n
        Which action do you want to do? 
                    
        Single stock operations:        
        1)  Browse a stock from {table} (loop)
        2)  Update a stock to {table} (loop)
        
        List operations:        
        10) Update {table} for S&P 500 
        11) Update {table} for Nasdaq 100
        12) Update {table} for S&P 500 + S&P 400 + Nasdaq 100
        13) Update {table} for Nasdaq Traded Stocks
        
        0)  quit
        Choose your action: """
    return menu



def make_actions_dict(table: str) -> Dict[str, Any]:
    """
    DEPENDS ON: browse_symbol_loop(), upsert_symbol_loop(), upsert_symbols_interactive()
    IMPORTS: get_sp_500(), get_nasdaq_100(), get_sp_nasdaq()
    USED BY: operate_table()
    """
    actions_dict: Dict[str, Any] = {
        '1': lambda: browse_symbol_loop(table),
        '2': lambda: upsert_symbol_loop(table),
        '10': lambda: upsert_symbols_interactive(table, sp_500_stocks),
        '11': lambda: upsert_symbols_interactive(table, nasdaq_100_stocks),
        '12': lambda: upsert_symbols_interactive(table, sp_nasdaq_stocks),
        '13': lambda: upsert_symbols_interactive(table, nasdaq_traded_stocks),
    }
    return actions_dict




def operate_stock_table(table: str):
    """
    DEPENDS ON: make_text_meun(), make_actions_dict()
    """
    text_menu: str = make_text_menu(table)
    actions_dict: Dict[str, Any] = make_actions_dict(table)
    while True:
        ans = input(text_menu)
        if ans in actions_dict:
            actions_dict[ans]()
        elif ans == '0':
            break
        else:
            print(f'INVALID INPUT - {ans}')




def test() -> None:
    start = default_timer()
    xs = ['MCD', 'GS', 'NVDA', 'MMM']
    upsert_symbols_terminal('stock_option', xs)
    print(default_timer() - start, ' seconds elapsed.')
    






if __name__ == '__main__':
    test()


