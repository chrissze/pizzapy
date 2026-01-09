import os


import pandas as pd

from pprint import pprint

from alpha_vantage.options import Options  # pip install alpha_vantage

API_KEY = os.getenv("AV_API_KEY")

opt = Options(key=API_KEY, output_format="json")

# Equivalent to:
# https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo

data: pd.DataFrame

data, meta_data = opt.get_historical_options(symbol="SPY")


print(data)

print(type(data))
