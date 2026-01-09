import os
import requests

API_KEY = os.environ["AV_API_KEY"]  # put your key in env

symbol = "SPY"

url = "https://www.alphavantage.co/query"

params = {
    "function": "ETF_PROFILE",
    "symbol": symbol,
    "apikey": API_KEY,
}

r = requests.get(url, params=params, timeout=30)

data = r.json()


print(data)


# Alpha Vantage ETF_PROFILE typically uses snake_case fields like net_assets
if "Error Message" in data or "Information" in data:
    raise RuntimeError(data)

net_assets = data.get("net_assets")  # this is the ETF “size” / AUM

print("SPY net assets:", net_assets)
