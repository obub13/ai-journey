import requests
from adapters.finnhub_adapter import get_quote

if __name__ == "__main__":
    print(get_quote("AAPL"))
