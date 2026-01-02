from alpha_vantage.timeseries import TimeSeries

# Replace "demo" with your real API key
api_key = "demo"

# Create a TimeSeries client in "raw" mode so we get the JSON response
ts = TimeSeries(key=api_key, output_format='json')

# Call the HISTORICAL_OPTIONS function manually
data, meta = ts.get_batch_stock_quotes(
    symbol='IBM',
    function='HISTORICAL_OPTIONS'
)

print(data)
