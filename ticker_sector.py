import yfinance as yf
import pandas as pd


stock = yf.Ticker("HGH.NZ")
print(stock.info["sector"])