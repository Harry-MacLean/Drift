import yfinance as yf



def detect_move(ticker, threshold=2):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1mo")
    drift = data["Close"].pct_change() * 100
    significant_moves = drift[(drift >= threshold) | (drift <= -threshold)]
    return significant_moves

result = detect_move("AIR.NZ")
print(result)