
"""
DEPENDS: pg_model.py

USED BY: 

"""

# STANDARD LIBS
import asyncio

from typing import Any

# PROGRAM MODULES

from pizzapy.pg_app.pg_model import ask_generate_stock_list_file, create_table, drop_table, print_current_db, print_databases, print_tables, print_table_columns




postgres_menu_text: str = """\n
    Which action do you want to do? 
        1) print_databases() 

        2) print_current_db()
        
        3) print_tables()

        4) print_table_columns()

        5) drop_table()
        
        11) create_table('guru_stock')
        12) create_table('zacks_stock')
        13) create_table('stock_option')
        14) create_table('stock_price')
        15) create_table('stock_technical')
        
        20) ask_generate_stock_list_file()

        0) quit
    Choose your action: """


actions_dict: dict[str, Any] = {
    '1': lambda: asyncio.run(print_databases()),
    
    '2': lambda: asyncio.run(print_current_db()),

    '3': lambda: asyncio.run(print_tables()),

    '4': lambda:  asyncio.run(print_table_columns()),

    '5': lambda: asyncio.run(drop_table()),

    '11': lambda: asyncio.run(create_table('guru_stock')),
    '12': lambda: asyncio.run(create_table('zacks_stock')),
    '13': lambda: asyncio.run(create_table('stock_option')),
    '14': lambda: asyncio.run(create_table('stock_price')),
    '15': lambda: asyncio.run(create_table('stock_technical')),
    '20': lambda: ask_generate_stock_list_file(),
    
    }


def pg_cli(): 
    """
    DEPENDS ON: postgres_menu_text, actions_dict
    """
    while True:
        ans: str = input(postgres_menu_text)
        if ans in actions_dict:
            print()
            actions_dict[ans]()
        elif ans == '0':
            break
        else:
            print('invalid input')



if __name__ == '__main__':
    pg_cli()
    print('DONE')

