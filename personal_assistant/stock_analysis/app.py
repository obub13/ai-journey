import requests
from adapters.finnhub_adapter import get_quote
from adapters.twelve_data_adapter import get_time_series
from adapters.alpaca_adapter import get_stock_news

if __name__ == "__main__":
    # print("FINNHUB ADAPTER  ", get_quote("AALPL"))
    # print("TWELVE DATA ADAPTER   " ,get_time_series("AAPLL"))
    candles = get_time_series("AAPL")
    print(candles[0])
    print(candles[-1])
    # print("ALPACA ADAPTER   " , get_stock_news("AAPLL"))
