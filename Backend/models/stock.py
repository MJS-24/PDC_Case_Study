from pydantic import BaseModel


class StockData(BaseModel):
    """Model for raw stock data from CSV"""
    timestamp: str
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class StockPrice(BaseModel):
    """Model for current stock price"""
    symbol: str
    current_price: float
    date: str
