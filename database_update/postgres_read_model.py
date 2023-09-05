"""
This is a common module for guru_stock, zacks, stock_option

"""

# STANDARD LIB
import sys; sys.path.append('..')
import subprocess
from typing import Any, Dict, List, Union


# THIRD PARTY LIB
import pandas
from pandas import DataFrame, Series

# PROGRAM MODULES

from database_update.postgres_connection_model import execute_pandas_read, execute_psycopg_command



    

def get_column_from_table(column: str, table: str) -> List[Any]:
    """
    * INDEPENDENT *
    IMPORTS: pandas, execute_pandas_read()
    USED BY:

    I can use this function to get a list of symbols that is present a particular table. 

    get_column_from_table(column='symbol', table='stock_guru')
    """
    cmd: str = f'SELECT {column} FROM {table} ORDER BY {column}'
    df: DataFrame = execute_pandas_read(cmd)  
    # the df shape is like (500, 1), one column only. 
    result_list: List[Any] = df.iloc[:, 0].to_list()
    return result_list





def get_symbol_row_result(symbol: str, table: str ) -> Series:
    """
    * INDEPENDENT *
    IMPORTS: pandas, execute_pandas_read()
    
    
    Note:
    (1) the table name MUST be available in the database, otherwise there will be exception.
    (2) The symbol can be non-exist in the table, the result will be just an empty Series for non-exist symbol. So I do not need to test if the symbol's row is present.
    (3) The targeted table MUST have a t column.

    When I call this function, I might put table as keyword argument,
    so I put it on the second place.

    No need to uppercase symbol, it will be changed in later function.

    This function will be a common function for guru, zacks, option, technical, in both terminal and GUI.
    """    
    cmd: str = f"SELECT * FROM {table} WHERE symbol = '{symbol}' ORDER BY t DESC"
    df: DataFrame = execute_pandas_read(cmd)
    first_row: Series = Series() if df.empty else df.iloc[0]
    return first_row
    


def view_symbol_row_terminal(symbol: str, table: str) -> None:
    """
    DEPENDS ON: get_symbol_row_result()
    USED BY:  guru_operation_script.py
    This function will be a common function for guru, zacks, option, technical in terminal scripts.

    exapmle:
        view_symbol_row_terminal('amd', 'stock_guru')
    """
    SYMBOL: str = symbol.upper()
    vertical_result: Series = get_symbol_row_result(symbol=SYMBOL, table=table)
    if not vertical_result.empty:
        print(vertical_result)
    else:
        print(f'{SYMBOL} is not in {table}')



def test() -> None:
    view_symbol_row_terminal('amd', 'stock_guru')


if __name__ == '__main__':
    test()

