
"""

USED BY: 

"""

# STANDARD LIBS

from typing import Any, Dict

# PROGRAM MODULES

from pizzapy.pg_app.pg_manage_database_model import create_new_postgres_db, create_table,  loop_drop_table, loop_show_table, loop_show_table_rows, show_current_database, show_databases, show_tables


postgres_menu_text: str = """\n
    Which action do you want to do? 
        1) show_databases()   
        2) create_new_postgres_db()
        3) show_tables()
        4) loop_show_table()
        5) loop_drop_table()
        6) loop_show_table_rows()
        7) show_current_database()

        
        
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
                            
    '11': lambda: create_table('guru_stock'),
    '12': lambda: create_table('zacks_stock'),
    '13': lambda: create_table('stock_option'),
    '14': lambda: create_table('stock_price'),
    '15': lambda: create_table('stock_technical'),
    '16': lambda: create_table('technical_one'),
    }


def pg_cli_main(): 
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
    pg_cli_main()

