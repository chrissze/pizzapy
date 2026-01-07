"""
This is a common module for guru_stock, zacks, stock_option

"""

# STANDARD LIB

import subprocess
from typing import Any, Dict, List, Union


# THIRD PARTY LIB
import pandas
from pandas import DataFrame, Series

# CUSTOM LIBS
from batterypy.string.read import format_number_with_commas

# PROGRAM MODULES

from pizzapy.database_update.postgres_connection_model import execute_pandas_read, execute_psycopg_command



    

def get_column_from_table(column: str, table: str) -> List[Any]:
    """
    * INDEPENDENT *
    IMPORTS: pandas, execute_pandas_read()
    USED BY:

    I can use this function to get a list of symbols that is present a particular table. 

    get_column_from_table(column='symbol', table='guru_stock')
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
    USED BY: view_vertical()    
    
    Note:
    (1) the table name MUST be available in the database, otherwise there will be exception.
    (2) The symbol can be non-exist in the table, the result will be just an empty Series for non-exist symbol. So I do not need to test if the symbol's row is present.
    (3) The targeted table MUST have a t column, so the result will be the latest row.

    When I call this function, I might put table as keyword argument,
    so I put it on the second place.

    No need to uppercase symbol, it will be changed in later function.

    This function will be a common function for guru, zacks, option, technical, in both terminal and GUI.
    """    
    cmd: str = f"SELECT * FROM {table} WHERE symbol = '{symbol}' ORDER BY t DESC"
    df: DataFrame = execute_pandas_read(cmd)
    first_row: Series = Series() if df.empty else df.iloc[0]
    return first_row
    


def view_vertical(symbol: str, table: str) -> DataFrame:
    """
    DEPENDS ON: get_symbol_row_result()
    IMPORTS: batterypy(format_number_with_commas)
    USED BY:  view_vertical_terminal()
    
    This function will be a common function for guru, zacks, option, technical in terminal scripts.

    There will a '0' at the top of the returning DataFrame, it just mean there is no DataFrame name.
    
    I need to_frame() to convert the Series to a DataFrame, 
    so that I can use DataFrame's map() method.
    exapmle:
        view_vertical('amd', 'guru_stock')

    .applymap() will be deprecated in future releases.
    
    """
    SYMBOL: str = symbol.upper()
    series_result: Series = get_symbol_row_result(symbol=SYMBOL, table=table)
    if not series_result.empty:
        #commas_df: DataFrame = series_result.to_frame().applymap(format_number_with_commas)
        commas_df: DataFrame = series_result.to_frame().map(format_number_with_commas)
        return commas_df
    else:
        return DataFrame()



def view_vertical_terminal(symbol: str, table: str) -> None:
    """
    DEPENDS ON: view_vertical()
    USED BY:  guru_operation_script.py, option_operation_script.py, 
    This function will be a common function for guru, zacks, option, technical in terminal scripts.

    exapmle:
        view_vertical_terminal('amd', 'guru_stock')
    """
    commas_df: DataFrame = view_vertical(symbol, table)
    if not commas_df.empty:
        print(commas_df)
    else:
        print(f'{symbol} is not in {table}')





def test() -> None:
    symbol:str = input('Which SYMBOL do you want to input? ')
    view_vertical_terminal(symbol, 'stock_option')


if __name__ == '__main__':
    test()

