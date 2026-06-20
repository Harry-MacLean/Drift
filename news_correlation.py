import yfinance as yf
import pandas as pd
from detect_move import detect_move
import anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path=r"C:\Users\harry\Desktop\Drift\.env")
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def news_correlation(ticker, date, news_articles):
    prompt = (
        f"Ticker: {ticker} | Date: {date} | "
        f"Cause: {news_articles} | "
        f"Message: Given the cause of this tickers significant movement,"
        f"Find 5 to 10 other NZX/ASX listed companies that may be affected by the same underlying event. "
        f"Exclude the original ticker from the new list."
        f"respond only in this JSON format, with no other text: "
        F'[{{"ticker": "ticker1", "reason": "reason1", "news": ["headline1", "headline2"]}}, '
        F'{{"ticker": "ticker2", "reason": "reason2", "news": ["headline1"]}}]'
    
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        tools=[
            {
            "type": "web_search_20250305",
            "name": "web_search"
            }
        ],
        messages=[
            {"role": "user", "content": prompt}
        ]

    )
    full_response = "".join([block.text for block in message.content if hasattr(block, 'text')])
    return(full_response)



def confirm_correlation(parsed, date, ticker):
    og_ticker = yf.Ticker(ticker).info.get("longName")
    confirmed = []
    for company in parsed:
        ticker_adjustment = company['ticker'].replace(".ASX", ".AX").replace(".NZX", ".NZ")
        chain = detect_move(ticker_adjustment)
        if chain is None:
            continue
        candidate_name = yf.Ticker(ticker_adjustment).info.get("longName")
        if candidate_name == og_ticker:
            continue
        for dates in chain.index:
            if dates <= pd.to_datetime(date).date() and dates >= pd.to_datetime(date).date() - pd.Timedelta(days=2):
                confirmed.append({
                    "ticker": ticker_adjustment,
                    "date": dates,
                    "spike": float(chain.loc[dates, 'PCT Change %']),
                    "news": company['news']
                })
    return(confirmed)



