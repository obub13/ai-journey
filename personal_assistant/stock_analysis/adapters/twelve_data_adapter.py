import os
from dotenv import load_dotenv
import requests
from models.stock_model import PriceCandle

load_dotenv()

from datetime import datetime, timedelta


def get_time_series(symbol: str):
    """
    Fetches the time series data for a given stock symbol from the Twelve Data API.

    Args:
        symbol (str): The stock symbol to fetch data for.

    Returns:
        dict: A dictionary containing the time series data.
    """

    end_date_var = datetime.today()
    start_date_var = end_date_var - timedelta(days=5 * 365)
    r = requests.get(
        "https://api.twelvedata.com/time_series",
        params={
            "symbol": symbol,
            "interval": "1day",
            "outputsize": 1260,
            "start_date": start_date_var,
            "end_date": end_date_var,
            "apikey": os.getenv("TWELVEDATA_API_KEY"),
        },
    )
    if r.status_code == 200:
        candles_list = []
        for item in r.json().get("values"):
            candles_list.append(PriceCandle(
                timestamp=item.get("datetime"),
                open=float(item.get("open")),
                high=float(item.get("high")),
                low=float(item.get("low")),
                close=float(item.get("close")),
                volume=int(item.get("volume")),
            ))
        return candles_list
    else:
        raise Exception(
            f"twelve_data: Error fetching time series for {symbol}: {r.status_code} - {r.text}"
        )
