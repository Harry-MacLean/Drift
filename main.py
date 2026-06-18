from fastapi import FastAPI
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
from detect_move import detect_move
from news_move import explanation

@app.get("/detect/{ticker}")
def get_moves(ticker: str):
    return detect_move(ticker)

@app.get("/explain/{ticker}/{date}")
def get_explanation(ticker: str, date: str):
    return explanation(ticker, date)