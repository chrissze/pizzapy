"""
In order for this script to works, the following must be satisfied:
    (1) each module in a subfolder must have sys.path.append('..')

    (2)  each module in a subfolder must have full path import even for same folder module,
    see database_update/postgres_execution_model.py

    
"""


import subprocess
from typing import List

# PROGRAM MODULES
from terminal_scripts.stocks_operation_script import manage_stocks
from terminal_scripts.futures_operation_script import manage_futures
from terminal_scripts.postgres_operation_script import manage_database



def start():
    actions = {
        '1': lambda: manage_stocks(),
        '2': lambda: manage_futures(),
        '3': lambda: manage_database(),
        '0': lambda: exit(),
    }
    while True:
        subprocess.run(['clear'])
        ans = input(f"""
        Stock Actions: 
            1) Manage Stocks
            2) Manage Futures            
            3) Manage Database, create or drop tables
            0) Exit the program
            
        please choose your action: """)
        if ans in actions:
            actions[ans]()
        else:
            print('invalid input')



if __name__ == '__main__':
    start()

