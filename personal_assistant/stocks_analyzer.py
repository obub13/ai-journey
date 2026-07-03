import os
from dotenv import load_dotenv
import requests
import finnhub

load_dotenv()
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

r = requests.get(
    "https://api.finnhub.io/api/v1/quote",
    params={"symbol": "AAPL", "token": os.getenv("FINNHUB_API_KEY")},
)

print(r.status_code, r.json())

r = requests.get(
    "https://api.twelvedata.com/price",
    params={"symbol": "AAPL", "apikey": os.getenv("TWELVEDATA_API_KEY")},
)
print(r.status_code, r.json())

r = requests.get(
    "https://data.alpaca.markets/v2/stocks/AAPL/quotes/latest",
    headers={"APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
             "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY")},
)
print(r.status_code, r.json())