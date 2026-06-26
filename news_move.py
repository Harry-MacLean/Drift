import yfinance as yf
import pandas as pd
from detect_move import detect_move
import anthropic
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"C:\Users\harry\Desktop\Drift\.env")
api_key = os.getenv("ANTHROPIC_API_KEY")
#print(api_key)
client = anthropic.Anthropic(api_key=api_key)

def news_available(ticker, date):
    stock = yf.Ticker(ticker)
    spike_date = pd.to_datetime(date).date()
    for article in stock.news:
        article_date = pd.to_datetime(article['content']['pubDate']).date()
        if article_date <= spike_date and article_date >= spike_date - pd.Timedelta(days=2):
            return True
    return False


def explanation(ticker: str, date: str):
    stock = yf.Ticker(ticker)
    result = detect_move(ticker)
    for dates in result.index:
        spike_date = dates
        if spike_date == pd.to_datetime(date).date():
            for article in stock.news:
                article_date = pd.to_datetime(article['content']['pubDate']).date()
                if article_date <= spike_date and article_date >= spike_date - pd.Timedelta(days=2):
                    print(f"Spike: {spike_date} | News: {article['content']['title']}")
            
                    prompt = f"Ticker: {ticker} | Move: {result.loc[spike_date, 'PCT Change %']}% | Spike: {spike_date} | News: {article['content']['title']} | Message: Websearch the news article provided and explain why {ticker} moved {result.loc[spike_date, 'PCT Change %']}% on {spike_date}. Structure your response with clear headers and bullet points covering: (1) what the news said, (2) how it connects to the price move, (3) a very brief conclusion. Keep each section concise — 2 short bullets maximum per section. If you are approaching your response limit, wrap up your current section with a concluding sentence rather than starting a new section. Never cut off mid-sentence or mid-bullet. No emojis."
                    message = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=600,
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
    return "No news articles found within two day threshold of the spike date. Please try another date."
