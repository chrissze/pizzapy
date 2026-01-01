
"""
DEPENDS: pg_model.py

USED BY: 

"""

# STANDARD LIBS
import asyncio

from typing import Any

# PROGRAM MODULES

from pizzapy.pg_app.pg_model import drop_pg_table, print_current_db, print_databases, print_tables

from pizzapy.pg_app.pg_manage_database_model import create_table, loop_show_table, loop_show_table_rows


postgres_menu_text: str = """\n
    Which action do you want to do? 
        1) print_databases()   
        
        3) print_tables()
        4) loop_show_table()
        5) drop_pg_table()
        6) loop_show_table_rows()
        7) print_current_db()

        
        
        11) create_table('guru_stock')
        12) create_table('zacks_stock')
        13) create_table('stock_option')
        14) create_table('stock_price')
        15) create_table('stock_technical')
        16) create_table('technical_one')
        
        0) quit
    Choose your action: """


actions_dict: dict[str, Any] = {
    '1': lambda: asyncio.run(print_databases()),
    
    '3': lambda: asyncio.run(print_tables()),
    '4': lambda: loop_show_table(),

    '5': lambda: asyncio.run(drop_pg_table()),

    '6': lambda: loop_show_table_rows(),
    '7': lambda: asyncio.run(print_current_db()),
                            
    '11': lambda: create_table('guru_stock'),
    '12': lambda: create_table('zacks_stock'),
    '13': lambda: create_table('stock_option'),
    '14': lambda: create_table('stock_price'),
    '15': lambda: create_table('stock_technical'),
    '16': lambda: create_table('technical_one'),
    }


def cli(): 
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
    cli()

