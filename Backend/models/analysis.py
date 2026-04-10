from pydantic import BaseModel


class StockAnalysis(BaseModel):
    """Model for stock analysis results"""
    symbol: str
    current_price: float
    moving_average_10: float
    moving_average_20: float
    volatility: float
    recommendation: str  # BUY, SELL, HOLD
    confidence: float
    date: str
