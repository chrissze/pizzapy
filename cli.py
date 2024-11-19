"""
Run the program:
(venv) $ python3 -m pizzapy.cli


generate_file_model cannot be directly run in this CLI module because the auto generated file is a component of this CLI program, we cannot overwrite it when CLI is running.

"""

# STANDARD LIBS

import subprocess

from typing import List

# PROGRAM MODULES

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
            0) Exit the program
            
        please choose your action: """)
        if ans in actions:
            actions[ans]()
        else:
            print('invalid input')



if __name__ == '__main__':
    start()

