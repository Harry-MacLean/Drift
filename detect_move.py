import yfinance as yf
import pandas as pd


def detect_move(ticker, threshold=2):
   
    stock = yf.Ticker(ticker)
    data = stock.history(period="1mo")
    if data.empty:
        print("Ticker not found or no data available. Please try another ticker.")
        return 
    drift = data["Close"].pct_change() * 100
    significant_moves = drift[(drift >= threshold) | (drift <= -threshold)]
    df = significant_moves.to_frame()
    df.rename(columns={"Close": "PCT Change %"}, inplace=True)
    df.index = df.index.date
    df = df.round(3)
    df["ticker"] = ticker
    return df

result = detect_move("AIR.NZ")
print(result)
if result is not None:
    result.to_csv(r"C:\Users\harry\Desktop\Drift\significant_moves.csv")
    
