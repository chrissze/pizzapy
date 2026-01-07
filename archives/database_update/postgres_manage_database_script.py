
"""

USED BY: terminal_scripts/postgres_manage_database_script.py

"""

# STANDARD LIBS

import subprocess
from typing import Any, Dict, List

# PROGRAM MODULES
from pizzapy.database_update.postgres_manage_database_model import create_new_postgres_db, create_table,  loop_drop_table, loop_execute_sql, loop_show_table, loop_show_table_rows, show_current_database, show_databases, show_tables


postgres_menu_text: str = """\n
    Which action do you want to do? 
        1) show_databases()   
        2) create_new_postgres_db()
        3) show_tables()
        4) loop_show_table()
        5) loop_drop_table()
        6) loop_show_table_rows()
        7) show_current_database()

        9) Run a custom SQL command - loop_execute_sql()
        10) Print content of /etc/config.json            
        11) create_table('guru_stock')
        12) create_table('zacks_stock')
        13) create_table('stock_option')
        14) create_table('stock_price')
        15) create_table('stock_technical')
        16) create_table('technical_one')
        
        0) quit
    Choose your action: """


actions_dict: Dict[str, Any] = {
    '1': lambda: print(show_databases()),
    '2': lambda: create_new_postgres_db(),
    '3': lambda: print(show_tables()),
    '4': lambda: loop_show_table(),
    '5': lambda: loop_drop_table(),
    '6': lambda: loop_show_table_rows(),
    '7': lambda: print(show_current_database()),

    '9': lambda: loop_execute_sql(),
    '10': lambda: subprocess.run('cat /etc/config.json', stdin=True, shell=True),                             
    '11': lambda: create_table('guru_stock'),
    '12': lambda: create_table('zacks_stock'),
    '13': lambda: create_table('stock_option'),
    '14': lambda: create_table('stock_price'),
    '15': lambda: create_table('stock_technical'),
    '16': lambda: create_table('technical_one'),
    }


def manage_postgres_database(): 
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
    manage_postgres_database()

