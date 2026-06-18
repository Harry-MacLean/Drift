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
            
                    prompt = f"Ticker: {ticker} | Move: {result.loc[spike_date, 'PCT Change %']} | Spike: {spike_date} | News: {article['content']['title']} | Message: {'Websearch the news articles provided, correlate the recent stock movement to them and explain the possible reasons for the movement. If there is no correlation, do not create one. Structure your message concisely.'}"
                    message = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=200,
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
