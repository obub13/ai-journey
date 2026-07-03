from dataclasses import dataclass

"""
StockQuote — Standard data contract for stock quote responses.

Defines the normalized shape that all three API adapters (Finnhub, Twelve Data, Alpaca)
must conform to. Any code consuming stock quote data in this app works with
StockQuote objects exclusively — never raw API responses.
"""


@dataclass
class StockQuote:
    symbol: str
    current_price: float
    change: float
    change_percent: float
    high: float
    low: float
    open: float
    previous_close: float
    timestamp: str
    source: str
