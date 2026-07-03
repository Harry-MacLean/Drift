from fastapi import FastAPI
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
import json
from news_correlation import news_correlation, confirm_correlation
from recent_movers import get_recent_movers
from news_move import news_available
from fastapi.responses import StreamingResponse

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
    return StreamingResponse(explanation(ticker, date), media_type="text/plain")


def chain_generator(ticker, date):
    yield "Analysing price move...\n"

    full_explanation = ""
    for chunk in explanation(ticker, date):
        full_explanation += chunk
        
    yield "Searching for correlated stocks...\n"
    candidates_raw = news_correlation(ticker, date, full_explanation)
    start = candidates_raw.find('[')
    end = candidates_raw.rfind(']') + 1
    clean_json = candidates_raw[start:end]

    yield "Verifying against real price data...\n"
    verified_candidates = confirm_correlation(json.loads(clean_json), date, ticker)

    yield json.dumps(verified_candidates)



@app.get("/chain/{ticker}/{date}")
def get_chain(ticker: str, date: str):
    return StreamingResponse(chain_generator(ticker, date), media_type="text/plain")

@app.get("/recent")
def get_recent():
    return get_recent_movers()

@app.get("/news_available/{ticker}/{date}")
def get_news_availability(ticker: str, date: str):
    return news_available(ticker, date)
    