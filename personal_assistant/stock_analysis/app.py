import requests
from adapters.finnhub_adapter import get_quote
from adapters.twelve_data_adapter import get_time_series

if __name__ == "__main__":
    print(get_quote("AAPL"))
    # print(get_time_series("AAPL"))
    candles = get_time_series("AAPL")
    print(candles[0])
    print(candles[-1])