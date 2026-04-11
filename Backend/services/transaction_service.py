"""Sales and transaction analytics"""

import pandas as pd
from datetime import datetime, timedelta


class TransactionService:
    """Sales and transaction analytics"""
    
    def __init__(self, loader):
        self.loader = loader
        self.transactions_df = loader.load_transactions()
        self.products_df = loader.load_products()
        self.branches_df = loader.load_branches()
    
    def get_recent_sales(self, days: int = 7) -> list:
        """Get sales from last N days"""
        
        cutoff = pd.Timestamp(datetime.now() - timedelta(days=days))
        recent = self.transactions_df[
            self.transactions_df['timestamp'] >= cutoff
        ].copy()
        
        # Join details
        recent = recent.merge(
            self.products_df[['product_id', 'product_name', 'category']], 
            on='product_id'
        )
        recent = recent.merge(
            self.branches_df[['branch_id', 'branch_name']], 
            on='branch_id'
        )
        
        result = []
        for _, row in recent.iterrows():
            result.append({
                'transaction_id': row['transaction_id'],
                'timestamp': row['timestamp'].isoformat(),
                'branch_name': row['branch_name'],
                'product_name': row['product_name'],
                'category': row['category'],
                'quantity': int(row['quantity']),
                'total_amount': float(row['total_amount']),
                'unit_price': float(row['total_amount'] / row['quantity'])
            })
        
        return sorted(result, key=lambda x: x['timestamp'], reverse=True)
