from pydantic import BaseModel
from typing import Optional


class BuyRequest(BaseModel):
    """Request model for buying stocks"""
    symbol: str
    quantity: int


class SellRequest(BaseModel):
    """Request model for selling stocks"""
    symbol: str
    quantity: int


class BuyResponse(BaseModel):
    """Response model for buy transaction"""
    success: bool
    message: str
    transaction_id: Optional[str]
    price: Optional[float]
    total_amount: Optional[float]


class SellResponse(BaseModel):
    """Response model for sell transaction"""
    success: bool
    message: str
    transaction_id: Optional[str]
    price: Optional[float]
    total_amount: Optional[float]
    profit_loss: Optional[float]
