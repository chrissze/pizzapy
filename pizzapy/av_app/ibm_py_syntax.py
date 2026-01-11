"""

# Equivalent to:
# https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo


"""

import os

import pandas as pd

from alpha_vantage.options import Options

API_KEY = os.getenv("AV_API_KEY")

def get_chain(symbol: str) -> pd.DataFrame:

    opt = Options(key=API_KEY, output_format='pandas')

    data, _ = opt.get_historical_options(symbol=symbol)

    return data

print(get_chain('AMD'))