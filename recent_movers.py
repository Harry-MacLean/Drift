import pandas as pd 
import yfinance as yf
from detect_move import detect_move


def get_recent_movers():
    recent_movers = []
    tickers = ["MEL.NZ", "AIR.NZ", "MFT.NZ", "CEN.NZ", "SPK.NZ", "ANZ.NZ", "FBU.NZ", "FPH.NZ", "RYM.NZ", "PCT.NZ", "HGH.NZ", "IFT.NZ", "NZK.NZ", "BAI.NZ", "MCY.NZ", "SKO.NZ"] 
    for ticker in tickers:
        result = detect_move(ticker)
        if result is not None and not result.empty:
            for date, row in result.iterrows():
                recent_movers.append({
                    "ticker": ticker,
                    "date": date,
                    "pct_change": row["PCT Change %"]
                })
    recent_movers.sort(key=lambda x: x["date"], reverse=True)
    return recent_movers[:5]
print(get_recent_movers())