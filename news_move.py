import yfinance as yf
import pandas as pd

stock = yf.Ticker("AIR.NZ")
## for article in stock.news:
   ## print(article['content']['title'])

article = stock.news[0]
date = pd.to_datetime(article['content']['pubDate']).date()
print(date)