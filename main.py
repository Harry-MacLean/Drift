from fastapi import FastAPI
app = FastAPI()
from detect_move import detect_move

@app.get("/detect/{ticker}")
def get_moves(ticker: str):
    return detect_move(ticker)