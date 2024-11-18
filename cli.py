"""
Run the program:
(venv) $ python3 -m pizzapy.cli

    
"""

# STANDARD LIBS

import subprocess

from typing import List

# PROGRAM MODULES

from pizzapy.database_update.generate_file_model import generate_stock_list_file

from pizzapy.database_update.general_terminal_model import operate_stock_table

from pizzapy.database_update.postgres_manage_database_script import manage_postgres_database



def start():
    actions = {
        '1': lambda: operate_stock_table('guru_stock'),
        '2': lambda: operate_stock_table('zacks_stock'),
        '3': lambda: operate_stock_table('stock_option'),
        '4': lambda: operate_stock_table('stock_technical'),
        '5': lambda: operate_stock_table('technical_one'),
        '9': lambda: manage_postgres_database(),
        '10': generate_stock_list_file,
        '0': lambda: exit(),
    }
    while True:
        subprocess.run(['clear'])
        ans = input(f"""
        Stock Actions: 
            1) Operate Guru
            2) Operate Zacks
            3) Operate Stock Option
            4) Operate Stock Technical
            5) Operate Technical One
            9) Manage Database, create or drop tables
            10) CREATE database_update/generated_stock_list.py
            0) Exit the program
            
        please choose your action: """)
        if ans in actions:
            actions[ans]()
        else:
            print('invalid input')



if __name__ == '__main__':
    start()
