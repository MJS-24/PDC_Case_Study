from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Transaction(BaseModel):
    """Model for buy/sell transactions"""
    transaction_id: str
    symbol: str
    transaction_type: str  # BUY or SELL
    quantity: int
    price: float
    total_amount: float
    timestamp: datetime


class Portfolio(BaseModel):
    """Model for user portfolio"""
    user_id: str
    holdings: dict  # {symbol: quantity}
    transaction_history: List[Transaction]
    total_invested: float
    current_value: float
    profit_loss: float


class PortfolioResponse(BaseModel):
    """Response model for portfolio data"""
    total_invested: float
    current_value: float
    profit_loss: float
    profit_loss_percent: float
    holdings: dict
