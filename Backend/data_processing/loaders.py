"""CSV data loading with validation"""

import pandas as pd
from pathlib import Path
from ..utils.path_utils import DataPathResolver


class CSVDataLoader:
    """Load all project CSVs with validation"""
    
    # CSV file registry
    DATASETS = {
        'products': 'products.csv',
        'branches': 'branches.csv',
        'inventory': 'inventory.csv',
        'trucks': 'trucks.csv',
        'transactions': 'transactions.csv',
        'deliveries': 'delivery_logs.csv',
    }
    
    def __init__(self):
        """Initialize loader"""
        self.data = {}
    
    def load_products(self) -> pd.DataFrame:
        """Load product catalog"""
        if 'products' not in self.data:
            try:
                df = pd.read_csv(DataPathResolver.get_csv_path(self.DATASETS['products']))
                
                # Validate schema
                required = ['product_id', 'product_name', 'category', 'unit_price', 'weight_kg']
                missing = [col for col in required if col not in df.columns]
                if missing:
                    raise ValueError(f"Missing columns in products.csv: {missing}")
                
                # Convert types
                df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
                df['weight_kg'] = pd.to_numeric(df['weight_kg'], errors='coerce')
                
                self.data['products'] = df
                print(f"✓ Loaded {len(df)} products")
            except Exception as e:
                print(f"✗ Error loading products: {e}")
                raise
        
        return self.data['products']
    
    def load_branches(self) -> pd.DataFrame:
        """Load branch locations"""
        if 'branches' not in self.data:
            try:
                df = pd.read_csv(DataPathResolver.get_csv_path(self.DATASETS['branches']))
                df['capacity_sqm'] = pd.to_numeric(df['capacity_sqm'], errors='coerce')
                self.data['branches'] = df
                print(f"✓ Loaded {len(df)} branches")
            except Exception as e:
                print(f"✗ Error loading branches: {e}")
                raise
        
        return self.data['branches']
    
    def load_inventory(self) -> pd.DataFrame:
        """Load inventory levels"""
        if 'inventory' not in self.data:
            try:
                df = pd.read_csv(DataPathResolver.get_csv_path(self.DATASETS['inventory']))
                df['stock_level'] = pd.to_numeric(df['stock_level'], errors='coerce')
                df['reorder_point'] = pd.to_numeric(df['reorder_point'], errors='coerce')
                self.data['inventory'] = df
                print(f"✓ Loaded {len(df)} inventory records")
            except Exception as e:
                print(f"✗ Error loading inventory: {e}")
                raise
        
        return self.data['inventory']
    
    def load_transactions(self) -> pd.DataFrame:
        """Load sales transactions"""
        if 'transactions' not in self.data:
            try:
                df = pd.read_csv(DataPathResolver.get_csv_path(self.DATASETS['transactions']))
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
                df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
                self.data['transactions'] = df
                print(f"✓ Loaded {len(df)} transactions")
            except Exception as e:
                print(f"✗ Error loading transactions: {e}")
                raise
        
        return self.data['transactions']
    
    def load_trucks(self) -> pd.DataFrame:
        """Load truck fleet"""
        if 'trucks' not in self.data:
            try:
                df = pd.read_csv(DataPathResolver.get_csv_path(self.DATASETS['trucks']))
                df['capacity_kg'] = pd.to_numeric(df['capacity_kg'], errors='coerce')
                df['fuel_efficiency_kpl'] = pd.to_numeric(df['fuel_efficiency_kpl'], errors='coerce')
                df['last_maintenance'] = pd.to_datetime(df['last_maintenance'], errors='coerce')
                self.data['trucks'] = df
                print(f"✓ Loaded {len(df)} trucks")
            except Exception as e:
                print(f"✗ Error loading trucks: {e}")
                raise
        
        return self.data['trucks']
    
    def load_deliveries(self) -> pd.DataFrame:
        """Load delivery logs"""
        if 'deliveries' not in self.data:
            try:
                df = pd.read_csv(DataPathResolver.get_csv_path(self.DATASETS['deliveries']))
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                df['distance_km'] = pd.to_numeric(df['distance_km'], errors='coerce')
                df['fuel_consumed_liters'] = pd.to_numeric(df['fuel_consumed_liters'], errors='coerce')
                self.data['deliveries'] = df
                print(f"✓ Loaded {len(df)} deliveries")
            except Exception as e:
                print(f"✗ Error loading deliveries: {e}")
                raise
        
        return self.data['deliveries']
    
    def load_all(self):
        """Load all datasets"""
        print("\n[Loading all datasets...]")
        self.load_products()
        self.load_branches()
        self.load_inventory()
        self.load_transactions()
        self.load_trucks()
        self.load_deliveries()
        print("✓ All datasets loaded successfully\n")
