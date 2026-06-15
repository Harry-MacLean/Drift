import yfinance as yf
import pandas as pd


def macro_data(ticker):
   
    stock = yf.Ticker(ticker)
    data = stock.history(period="10y")
    if data.empty:
        print("Ticker not found or no data available. Please try another ticker.")
        return 
    drift = data["Close"].pct_change() * 100
    df = drift.to_frame()
    df.rename(columns={"Close": "PCT Change %"}, inplace=True)
    df.index = df.index.date
    df = df.round(3)
    df["Factor"] = ticker
    return df



oil = macro_data("BZ=F")
nzd_usd = macro_data("NZDUSD=X")
ten_year_rate = macro_data("^TNX")
air_nz = macro_data("AIR.NZ")

result = pd.concat([oil, nzd_usd, ten_year_rate, air_nz], keys=["Oil", "NZD/USD", "ten-yr-rate", "AIR.NZ"], axis=1)
for lag in range(0, 11):
    correlation = result["AIR.NZ"]["PCT Change %"].corr(result["ten-yr-rate"]["PCT Change %"].shift(lag))
    print(correlation)
print(result)
if result is not None:
    result.to_csv(r"C:\Users\harry\Desktop\Drift\macro_data.csv")


