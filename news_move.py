import yfinance as yf
import pandas as pd
from detect_move import detect_move

stock = yf.Ticker("AIR.NZ")
result = detect_move("AIR.NZ")
for dates in result.index:
    spike_date = dates
    for article in stock.news:
        article_date = pd.to_datetime(article['content']['pubDate']).date()
        if article_date <= spike_date and article_date >= spike_date - pd.Timedelta(days=2):
            print(f"Spike: {spike_date} | News: {article['content']['title']}")
    