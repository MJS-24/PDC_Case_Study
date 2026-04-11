"""Data models for all entities"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class Product(BaseModel):
    """Product catalog"""
    product_id: str
    product_name: str
    category: str
    unit_price: float
    weight_kg: float


class Branch(BaseModel):
    """Distribution centers"""
    branch_id: str
    branch_name: str
    city: str
    region: str
    capacity_sqm: int


class InventoryItem(BaseModel):
    """Stock levels by branch"""
    branch_id: str
    product_id: str
    stock_level: int
    reorder_point: int
    status: Optional[str] = None


class Transaction(BaseModel):
    """Sales transactions"""
    transaction_id: str
    timestamp: datetime
    branch_id: str
    product_id: str
    quantity: int
    total_amount: float
    customer_id: str


class Truck(BaseModel):
    """Fleet vehicles"""
    truck_id: str
    type: str
    capacity_kg: int
    fuel_efficiency_kpl: float
    last_maintenance: datetime


class Delivery(BaseModel):
    """Delivery logs"""
    delivery_id: str
    truck_id: str
    timestamp: datetime
    origin_branch: str
    destination_branch: str
    distance_km: float
    fuel_consumed_liters: float
    status: str


class InventoryWithProduct(BaseModel):
    """Inventory with product details"""
    branch_id: str
    branch_name: str
    product_id: str
    product_name: str
    category: str
    stock_level: int
    reorder_point: int
    unit_price: float
    stock_value: float
    status: str
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
