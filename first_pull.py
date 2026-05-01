import yfinance as yf

# Pull Air New Zealand stock data from NZX
ticker = yf.Ticker("AIR.NZ")

# Get the last 5 days of price data
data = ticker.history(period="5d")

# Print it
print(data)