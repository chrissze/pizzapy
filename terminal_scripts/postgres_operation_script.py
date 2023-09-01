#!/usr/bin/env python3

'''
This script must be run in Virtual Environment so that the required packages are available.

The postgres server settings is in /etc/config.json in local computer.
'''

# STANDARD LIBS
import sys; sys.path.append('..')
import subprocess
from typing import Any, Dict, List



# PROGRAM MODULES
from database_update.postgres_execution_model import create_new_postgres_db, create_table,  drop_table, loop_show_table, show_databases, show_tables



def manage_database():
    actions: Dict[str, Any] = {
        '1': lambda: show_databases(),
        '2': lambda: create_new_postgres_db(),
        '3': lambda: show_tables(),
        '4': lambda: loop_show_table(),
        '5': lambda: drop_table(),
        '6': lambda: subprocess.run('cat /etc/config.json', stdin=True, shell=True),
                                     
        '11': lambda: create_table('stock_guru'),
        '12': lambda: create_table('stock_zacks'),
        '13': lambda: create_table('stock_option'),
        '14': lambda: create_table('stock_price'),
        '15': lambda: create_table('stock_technical'),
        '16': lambda: create_table('futures_option'),
    }
    while True:
        ans: str = input("""\n\n
        Which action do you want to do? 
            
            1) show_databases()   
            2) create_new_postgres_db()
            3) show_tables()
            4) loop_show_table()
            5) drop_table()      
            6) Print content of /etc/config.json
                            
            11) create_table('stock_guru')
            12) create_table('stock_zacks')
            13) create_table('stock_option')
            14) create_table('stock_price')
            15) create_table('stock_technical')
            16) create_table('futures_option')
            
            0) go to home screen
        Choose your action: """)
        if ans in actions:
            actions[ans]()
        elif ans == '0':
            break
        else:
            print('invalid input')





if __name__ == '__main__':
    manage_database()

