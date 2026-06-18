from fastapi import FastAPI
app = FastAPI()
from detect_move import detect_move
from news_move import explanation

@app.get("/detect/{ticker}")
def get_moves(ticker: str):
    return detect_move(ticker)

@app.get("/explain/{ticker}/{date}")
def get_explanation(ticker: str, date: str):
    return explanation(ticker, date)