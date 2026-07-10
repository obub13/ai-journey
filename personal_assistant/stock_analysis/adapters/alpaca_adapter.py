import html
import re
import requests
import os
from dotenv import load_dotenv

from models.stock_model import NewsItem
from datetime import datetime, timedelta, timezone

load_dotenv()


def _clean_text(text):
    if not text:
        return text
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def get_stock_news(symbol: str):
    """
    Fetches the latest news for a given stock symbol from the Alpaca API.

    Args:
        symbol (str): The stock symbol to fetch news for.

    Returns:
        list: A list of news articles for the given stock symbol.
    """
    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY"),
    }
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=14)
    r = requests.get(
        "https://data.alpaca.markets/v1beta1/news",
        headers=headers,
        params={
            "symbols": symbol,
            "limit": 5,
            "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    )
    if r.status_code == 200:
        news_list = []
        for item in r.json().get("news", []):
            news_list.append(
                NewsItem(
                    headline=_clean_text(item.get("headline")),
                    summary=_clean_text(item.get("summary")) or None,
                    source=item.get("source"),
                    url=item.get("url"),
                    published_at=item.get("created_at"),
                )
            )
        return news_list
    else:
        raise Exception(
            f"alpaca: Error fetching news for {symbol}: {r.status_code} - {r.text}"
        )
