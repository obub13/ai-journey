import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timezone
from models.stock_model import StockQuote
from adapters.errors import AdapterError



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
        timeout=5
    )
    if r.status_code == 200:
        data = r.json()
        if data.get("c") == 0 and data.get("t") == 0:
            raise AdapterError(f"finnhub: No quote data found for {symbol}.")
        dt_object = datetime.fromtimestamp(data.get("t"), tz=timezone.utc)
        human_timestamp = "Last traded:  " + dt_object.strftime("%b %d, %Y %I:%M %p")
        
        return StockQuote(
            symbol=symbol,
            current_price=data.get("c"),
            change=data.get("d"),
            change_percent=data.get("dp"),
            high=data.get("h"),
            low=data.get("l"),
            open=data.get("o"),
            previous_close=data.get("pc"),
            timestamp=dt_object.isoformat(),
            # timestamp=f"Last traded: {human_timestamp}",
            source="Finnhub"
        )
    else:
        raise AdapterError(f"finnhub: Error fetching quote for {symbol}: {r.status_code} - {r.text}")
    



