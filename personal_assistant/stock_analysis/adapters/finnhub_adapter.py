import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timezone
from models.stock_model import StockQuote



load_dotenv()
# finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))  # Not using finnhub SDK directly, using requests instead

def get_quote(symbol: str):
    """Fetches the quote data for a given stock symbol from the Finnhub API.

    Args:
        symbol (str): The stock symbol to fetch data for.

    Returns:
        StockQuote: An instance of StockQuote containing the fetched data.
    """
    r = requests.get(
        "https://api.finnhub.io/api/v1/quote",
        params={"symbol": symbol, "token": os.getenv("FINNHUB_API_KEY")},
    )
    if r.status_code == 200:
        dt_object = datetime.fromtimestamp(r.json().get("t"), tz=timezone.utc)
        human_timestamp = dt_object.strftime("%b %d, %Y %I:%M %p")
        return StockQuote(
            symbol=symbol,
            current_price=r.json().get("c"),
            change=r.json().get("d"),
            change_percent=r.json().get("dp"),
            high=r.json().get("h"),
            low=r.json().get("l"),
            open=r.json().get("o"),
            previous_close=r.json().get("pc"),
            timestamp=f"Last traded: {human_timestamp}",
            source="Finnhub"
        )
    else:
        raise Exception(f"finnhub: Error fetching quote for {symbol}: {r.status_code} - {r.text}")
    



