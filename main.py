from fastapi import FastAPI
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
import json
from news_correlation import news_correlation, confirm_correlation

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
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


@app.get("/chain/{ticker}/{date}")
def get_chain(ticker: str, date: str):
    cause = explanation(ticker, date)
    candidates_raw = news_correlation(ticker, date, cause)
    start = candidates_raw.find('[')
    end = candidates_raw.rfind(']') + 1
    clean_json = candidates_raw[start:end]
    verified_candidates = confirm_correlation(json.loads(clean_json), date, ticker)
    return verified_candidates
