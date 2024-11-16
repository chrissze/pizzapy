"""
*** INDEPENDENT MODULE ***

USED BY: 
    core_stock_update/

"""

# STANDARD LIBS
from timeit import timeit
from typing import Any, Dict, List, Set, Union


# THIRD PARTY LIBS

# CUSTOM LIBS
from dimsumpy.web.crawler import get_html_dataframes, get_html_soup

# PROGRAM MODULES
from pizzapy.database_update.generated_stock_list import nasdaq_100_stocks, nasdaq_listed_stocks, nasdaq_traded_stocks, sp_400_stocks, sp_500_stocks, sp_nasdaq_stocks


from pizzapy.guru_stock_update.guru_update_database_model import upsert_guru
from pizzapy.stock_option_update.option_update_database_model import upsert_option
from pizzapy.zacks_stock_update.zacks_update_database_model import upsert_zacks
from pizzapy.stock_price_update.price_update_database_model import upsert_latest_price
from pizzapy.stock_price_update.technical_update_database_model import upsert_recent_technical, upsert_technical_one






# need to comment out all_stocks when I use code to generate 
all_stocks: List[str] = nasdaq_traded_stocks + ['FNMA', 'FMCC']

stock_list_dict: Dict[str, List[str]] = {
    f'Nasdaq 100 ({len(nasdaq_100_stocks)})': nasdaq_100_stocks,
    f'S&P 500 ({len(sp_500_stocks)})': sp_500_stocks,
    f'S&P 400 ({len(sp_400_stocks)})': sp_400_stocks,
    f'S&P 500, 400 + Nasdaq 100 ({len(sp_nasdaq_stocks)})': sp_nasdaq_stocks,
    #f'Option Stocks ({len(option_traded_stocks)})': option_traded_stocks,
    f'Nasdaq Listed ({len(nasdaq_listed_stocks)})': nasdaq_listed_stocks,
    f'Nasdaq Traded ({len(nasdaq_traded_stocks)})': nasdaq_traded_stocks,
    f'All Stocks ({len(all_stocks)})': all_stocks,
}


# This dictionary can be used to compose upsert commands
# option, price and technicals are from yahoo
table_function_dict: Dict[str, Any] = {
    'guru_stock': upsert_guru ,
    'zacks_stock': upsert_zacks,
    'stock_option': upsert_option,
    'stock_price': upsert_latest_price,
    'stock_technical': upsert_recent_technical,
    'technical_one': upsert_technical_one,
    #'futures_option': upsert_guru ,
}


    

def test() -> None:
    print('hi')


if __name__ == '__main__':
    test()
