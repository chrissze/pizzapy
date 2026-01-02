import os
from pprint import pprint

from alpha_vantage.options import Options  # pip install alpha_vantage

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "demo")

opt = Options(key=API_KEY, output_format="json")

# Equivalent to:
# https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo
data, meta_data = opt.get_historical_options(symbol="IBM")

pprint(meta_data)
pprint(data)
