#!/usr/bin/env python3
"""Test script to validate all data loading and services"""

import sys
import os

# Add parent directory to path so Backend can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from Backend.utils.path_utils import DataPathResolver
from Backend.data_processing.loaders import CSVDataLoader
from Backend.services.analytics_service import AnalyticsService

def test_paths():
    """✓ Test path resolution"""
    print("\n[PATH TEST]")
    try:
        root = DataPathResolver.get_project_root()
        print(f"✓ Project root: {root}")
        
        data = DataPathResolver.get_data_folder()
        print(f"✓ Data folder: {data}")
        
        for filename in CSVDataLoader.DATASETS.values():
            path = DataPathResolver.get_csv_path(filename)
            exists = path.exists()
            status = "✓" if exists else "✗"
            print(f"{status} {filename}: {path}")
        
        return True
    except Exception as e:
        print(f"✗ Path test failed: {e}")
        return False

def test_loading():
    """✓ Test CSV loading"""
    print("\n[LOADING TEST]")
    try:
        loader = CSVDataLoader()
        loader.load_all()
        print(f"✓ All datasets loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_services():
    """✓ Test service initialization"""
    print("\n[SERVICE TESTS]")
    try:
        loader = CSVDataLoader()
        loader.load_all()
        
        analytics = AnalyticsService(loader)
        
        # Test dashboard
        dashboard = analytics.get_dashboard_summary()
        print(f"✓ Dashboard: {dashboard['total_transactions']} transactions")
        
        # Test low stock
        low_stock = analytics.inv_svc.get_low_stock_items()
        print(f"✓ Low Stock: {len(low_stock)} items need reordering")
        
        # Test sales analytics
        sales = analytics.get_sales_by_category()
        print(f"✓ Sales by Category: {len(sales)} categories")
        
        # Test branch performance
        branches = analytics.get_branch_performance()
        top_branch = branches[0] if branches else {}
        print(f"✓ Branch Performance: Top branch {top_branch.get('branch_name')} - ₱{top_branch.get('revenue', 0):,.2f}")
        
        # Test fleet
        fleet = analytics.get_fleet_efficiency()
        print(f"✓ Fleet: {fleet['total_completed_deliveries']} completed deliveries")
        
        # Test inventory valuation
        inv_val = analytics.get_inventory_valuation()
        print(f"✓ Inventory Value: ₱{inv_val['total_inventory_value']:,.2f} total assets")
        
        return True
    except Exception as e:
        print(f"✗ Service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    all_pass = all([
        test_paths(),
        test_loading(),
        test_services(),
    ])
    
    if all_pass:
        print("\n✅ All tests passed! Ready for production.")
    else:
        print("\n❌ Some tests failed. Check output above.")
    
    sys.exit(0 if all_pass else 1)
