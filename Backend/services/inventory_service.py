"""Inventory management and low-stock alerts"""

import pandas as pd


class InventoryService:
    """Inventory management and low-stock alerts"""
    
    def __init__(self, loader):
        self.loader = loader
        self.inventory_df = loader.load_inventory()
        self.products_df = loader.load_products()
        self.branches_df = loader.load_branches()
    
    def get_low_stock_items(self) -> list:
        """⭐ Items below reorder point (alerts)"""
        
        low_stock = self.inventory_df[
            self.inventory_df['stock_level'] <= self.inventory_df['reorder_point']
        ].copy()
        
        # Join with product and branch details
        low_stock = low_stock.merge(
            self.products_df[['product_id', 'product_name', 'category', 'unit_price']], 
            on='product_id'
        )
        low_stock = low_stock.merge(
            self.branches_df[['branch_id', 'branch_name', 'city']], 
            on='branch_id'
        )
        
        result = []
        for _, row in low_stock.iterrows():
            shortage = row['reorder_point'] - row['stock_level']
            result.append({
                'branch_id': row['branch_id'],
                'branch_name': row['branch_name'],
                'city': row['city'],
                'product_id': row['product_id'],
                'product_name': row['product_name'],
                'category': row['category'],
                'current_stock': int(row['stock_level']),
                'reorder_point': int(row['reorder_point']),
                'shortage': int(shortage),
                'unit_price': float(row['unit_price']),
                'restock_cost': float(shortage * row['unit_price'])
            })
        
        return sorted(result, key=lambda x: x['shortage'], reverse=True)
    
    def get_branch_inventory(self, branch_id: str) -> list:
        """Get all inventory for a branch with product details"""
        
        branch_inv = self.inventory_df[self.inventory_df['branch_id'] == branch_id].copy()
        
        # Join with products
        branch_inv = branch_inv.merge(
            self.products_df[['product_id', 'product_name', 'category', 'unit_price']], 
            on='product_id'
        )
        
        result = []
        for _, row in branch_inv.iterrows():
            status = "Low Stock" if row['stock_level'] <= row['reorder_point'] else \
                     "Adequate" if row['stock_level'] <= (row['reorder_point'] * 2) else \
                     "Excess"
            
            result.append({
                'product_id': row['product_id'],
                'product_name': row['product_name'],
                'category': row['category'],
                'stock_level': int(row['stock_level']),
                'reorder_point': int(row['reorder_point']),
                'unit_price': float(row['unit_price']),
                'stock_value': float(row['stock_level'] * row['unit_price']),
                'status': status
            })
        
        return result
