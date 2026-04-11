"""Analytics API routes"""

from fastapi import APIRouter, HTTPException
from Backend.models import PortfolioResponse
from Backend.services.analytics_service import AnalyticsService
from Backend.services.inventory_service import InventoryService
from Backend.services.transaction_service import TransactionService
from Backend.services.delivery_service import DeliveryService
from Backend.data_processing.loaders import CSVDataLoader

router = APIRouter(prefix="/api", tags=["analytics"])

# Initialize loader and services (global, loaded once)
loader = None
analytics_svc = None
inventory_svc = None
transaction_svc = None
delivery_svc = None


def initialize_services_api():
    """Call this in server.py startup"""
    global loader, analytics_svc, inventory_svc, transaction_svc, delivery_svc
    loader = CSVDataLoader()
    loader.load_all()
    analytics_svc = AnalyticsService(loader)
    inventory_svc = InventoryService(loader)
    transaction_svc = TransactionService(loader)
    delivery_svc = DeliveryService(loader)


# ============ DASHBOARD ENDPOINTS ============

@router.get("/dashboard")
async def get_dashboard():
    """⭐ High-level business overview"""
    if not analytics_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return analytics_svc.get_dashboard_summary()


# ============ INVENTORY ENDPOINTS ============

@router.get("/inventory/low-stock")
async def get_low_stock_alerts():
    """⭐ Items below reorder point - CRITICAL for operations"""
    if not inventory_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return inventory_svc.get_low_stock_items()


@router.get("/inventory/branch/{branch_id}")
async def get_branch_inventory(branch_id: str):
    """Get all inventory for a branch"""
    if not inventory_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return inventory_svc.get_branch_inventory(branch_id)


@router.get("/inventory/valuation")
async def get_inventory_valuation():
    """⭐ Total inventory asset value by branch"""
    if not analytics_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return analytics_svc.get_inventory_valuation()


@router.get("/portfolio", response_model=PortfolioResponse)
async def get_portfolio(user_id: str = None):
    """Current portfolio snapshot derived from inventory and product pricing."""
    if not analytics_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return analytics_svc.get_portfolio_snapshot(user_id=user_id)


# ============ SALES/TRANSACTION ENDPOINTS ============

@router.get("/sales/by-category")
async def get_sales_by_category():
    """⭐ Revenue breakdown by product category"""
    if not analytics_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return analytics_svc.get_sales_by_category()


@router.get("/sales/by-branch")
async def get_branch_performance():
    """⭐ Sales metrics per branch"""
    if not analytics_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return analytics_svc.get_branch_performance()


@router.get("/sales/recent")
async def get_recent_sales(days: int = 7):
    """Recent transactions (last N days)"""
    if not transaction_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return transaction_svc.get_recent_sales(days=days)


# ============ LOGISTICS/DELIVERY ENDPOINTS ============

@router.get("/deliveries/summary")
async def get_delivery_summary():
    """⭐ Delivery performance metrics"""
    if not delivery_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return delivery_svc.get_delivery_summary()


@router.get("/deliveries/delayed")
async def get_delayed_deliveries():
    """⭐ All delayed deliveries (operational concern)"""
    if not delivery_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return delivery_svc.get_delayed_deliveries()


@router.get("/fleet/efficiency")
async def get_fleet_efficiency():
    """⭐ Truck utilization and fuel costs"""
    if not analytics_svc:
        raise HTTPException(status_code=500, detail="Services not initialized")
    return analytics_svc.get_fleet_efficiency()
