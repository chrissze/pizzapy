

import requests

url = 'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo' 

r = requests.get(url) 

data = r.json()

print(data)

