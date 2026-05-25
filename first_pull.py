import yfinance as yf
import pandas as pd

# Pull Air New Zealand stock data from NZX
ticker = yf.Ticker("AIR.NZ")

# Get the last 5 days of price data
data = ticker.history(period="5d")

change = data["Close"].pct_change()*100
print(change[change >= 2])
# Print it
# print(data)