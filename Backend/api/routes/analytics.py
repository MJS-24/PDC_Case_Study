"""Stock trading API routes"""

from fastapi import APIRouter, HTTPException
from services.stock_service import StockService
from services.portfolio_service import PortfolioService
from services.transaction_service import TransactionService
from data_processing.loaders import StockDataLoader
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["stock-trading"])

# Initialize services (global, loaded once)
loader = None
stock_svc = None
portfolio_svc = None
transaction_svc = None

def initialize_services_api():
    """Call this in server.py startup"""
    global loader, stock_svc, portfolio_svc, transaction_svc
    loader = StockDataLoader()
    stock_svc = StockService(loader)
    transaction_svc = TransactionService()
    portfolio_svc = PortfolioService(stock_svc, transaction_svc)

# ============ HEALTH CHECK ============

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Stock Trading API is running"}

# ============ STOCK ENDPOINTS ============

@router.get("/stocks")
async def get_stocks():
    """Get all available stocks"""
    if not stock_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return stock_svc.get_all_stocks()

@router.get("/stocks/{company}")
async def get_stock_history(company: str):
    """Get historical data for a stock"""
    if not stock_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    history = stock_svc.get_stock_history(company)
    if not history:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"company": company, "history": history}

@router.post("/buy")
async def buy_stock(request: dict):
    """Buy stock"""
    if not portfolio_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")

    company = request.get("company")
    quantity = request.get("quantity", 1)

    if not company:
        raise HTTPException(status_code=400, detail="Company required")

    result = portfolio_svc.buy_stock(company, quantity)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])

    return result

@router.post("/sell")
async def sell_stock(request: dict):
    """Sell stock"""
    if not portfolio_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")

    company = request.get("company")
    quantity = request.get("quantity", 1)

    if not company:
        raise HTTPException(status_code=400, detail="Company required")

    result = portfolio_svc.sell_stock(company, quantity)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])

    return result

@router.get("/portfolio")
async def get_portfolio():
    """Get user portfolio"""
    if not portfolio_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return portfolio_svc.get_portfolio()

@router.get("/balance")
async def get_balance():
    """Get current balance"""
    if not portfolio_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return {"balance": portfolio_svc.get_balance()}

@router.post("/balance/add")
async def add_balance(request: dict):
    """Add funds to balance"""
    if not portfolio_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")

    amount = request.get("amount", 0)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    result = portfolio_svc.add_balance(amount)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])

    return result
@router.get("/transactions")
async def get_transactions():
    """Get transaction history"""
    if not transaction_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return {"transactions": transaction_svc.get_transactions()}
