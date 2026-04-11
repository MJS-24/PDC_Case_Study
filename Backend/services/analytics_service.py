"""Cross-dataset analytics and computed insights"""

import pandas as pd
from datetime import datetime, timedelta
from .inventory_service import InventoryService
from .transaction_service import TransactionService
from .delivery_service import DeliveryService


class AnalyticsService:
    """Cross-dataset insights and computed analytics"""
    
    def __init__(self, loader):
        self.loader = loader
        self.products_df = loader.load_products()
        self.branches_df = loader.load_branches()
        self.inventory_df = loader.load_inventory()
        self.transactions_df = loader.load_transactions()
        self.trucks_df = loader.load_trucks()
        self.deliveries_df = loader.load_deliveries()
        
        self.inv_svc = InventoryService(loader)
        self.tx_svc = TransactionService(loader)
        self.del_svc = DeliveryService(loader)
    
    def get_dashboard_summary(self) -> dict:
        """⭐ High-level business metrics for dashboard"""
        
        # Total revenue (all time)
        total_revenue = self.transactions_df['total_amount'].sum()
        
        # Recent transactions (last 7 days)
        now = pd.Timestamp(datetime.now())
        recent = self.transactions_df[
            (now - self.transactions_df['timestamp']).dt.days <= 7
        ]
        recent_revenue = recent['total_amount'].sum()
        
        # Low stock alerts
        low_stock = self.inv_svc.get_low_stock_items()
        
        # Delivery performance
        completed = len(self.deliveries_df[self.deliveries_df['status'] == 'Completed'])
        delayed = len(self.deliveries_df[self.deliveries_df['status'] == 'Delayed'])
        cancelled = len(self.deliveries_df[self.deliveries_df['status'] == 'Cancelled'])
        
        return {
            'total_revenue': float(total_revenue),
            'recent_revenue_7d': float(recent_revenue),
            'total_transactions': len(self.transactions_df),
            'low_stock_items': len(low_stock),
            'deliveries': {
                'completed': completed,
                'delayed': delayed,
                'cancelled': cancelled,
                'total': len(self.deliveries_df)
            },
            'branches_active': len(self.branches_df),
            'products_catalog': len(self.products_df),
            'fleet_size': len(self.trucks_df)
        }
    
    def get_sales_by_category(self) -> list:
        """⭐ Revenue breakdown by product category"""
        
        # Join transactions with products
        merged = self.transactions_df.merge(
            self.products_df[['product_id', 'category']], 
            on='product_id'
        )
        
        # Group by category
        by_category = merged.groupby('category').agg({
            'total_amount': ['sum', 'count', 'mean'],
            'quantity': 'sum'
        }).reset_index()
        
        result = []
        for _, row in by_category.iterrows():
            result.append({
                'category': row['category'],
                'total_sales': float(row[('total_amount', 'sum')]),
                'transaction_count': int(row[('total_amount', 'count')]),
                'avg_transaction': float(row[('total_amount', 'mean')]),
                'total_units_sold': int(row[('quantity', 'sum')])
            })
        
        return sorted(result, key=lambda x: x['total_sales'], reverse=True)
    
    def get_branch_performance(self) -> list:
        """⭐ Sales and metrics by branch"""
        
        # Sales by branch
        branch_sales = self.transactions_df.groupby('branch_id').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        
        branch_sales.columns = ['branch_id', 'revenue', 'units_sold', 'transaction_count']
        
        # Join branch details
        branch_performance = branch_sales.merge(
            self.branches_df, on='branch_id'
        )
        
        # Add inventory count per branch
        inv_counts = self.inventory_df.groupby('branch_id')['product_id'].count().reset_index()
        inv_counts.columns = ['branch_id', 'products_stocked']
        branch_performance = branch_performance.merge(inv_counts, on='branch_id', how='left')
        branch_performance['products_stocked'] = branch_performance['products_stocked'].fillna(0).astype(int)
        
        result = []
        for _, row in branch_performance.iterrows():
            result.append({
                'branch_id': row['branch_id'],
                'branch_name': row['branch_name'],
                'city': row['city'],
                'region': row['region'],
                'revenue': float(row['revenue']),
                'units_sold': int(row['units_sold']),
                'transaction_count': int(row['transaction_count']),
                'products_stocked': int(row['products_stocked']),
                'capacity_sqm': int(row['capacity_sqm'])
            })
        
        return sorted(result, key=lambda x: x['revenue'], reverse=True)
    
    def get_fleet_efficiency(self) -> dict:
        """⭐ Truck utilization and fuel costs"""
        
        # Merge deliveries with trucks
        merged = self.deliveries_df.merge(self.trucks_df, on='truck_id')
        
        # Calculate metrics
        completed_deliveries = merged[merged['status'] == 'Completed']
        
        total_distance = completed_deliveries['distance_km'].sum()
        total_fuel = completed_deliveries['fuel_consumed_liters'].sum()
        total_deliveries = len(completed_deliveries)
        
        avg_fuel_per_km = (total_fuel / total_distance) if total_distance > 0 else 0
        
        # Cost calculation (assume fuel cost ₱50/liter, typical Philippines)
        fuel_cost_per_liter = 50
        total_fuel_cost = total_fuel * fuel_cost_per_liter
        
        # By truck type
        by_type = merged.groupby('type').agg({
            'distance_km': 'sum',
            'fuel_consumed_liters': 'sum',
            'truck_id': 'count'
        }).reset_index()
        
        fleet_by_type = []
        for _, row in by_type.iterrows():
            fleet_by_type.append({
                'truck_type': row['type'],
                'trucks_count': int(row['truck_id']),
                'total_km': float(row['distance_km']),
                'total_fuel_liters': float(row['fuel_consumed_liters']),
                'fuel_cost_estimate': float(row['fuel_consumed_liters'] * fuel_cost_per_liter)
            })
        
        return {
            'total_completed_deliveries': total_deliveries,
            'total_distance_km': float(total_distance),
            'total_fuel_liters': float(total_fuel),
            'fuel_cost_estimate': float(total_fuel_cost),
            'avg_fuel_per_km': float(avg_fuel_per_km),
            'by_truck_type': fleet_by_type
        }
    
    def get_inventory_valuation(self) -> dict:
        """⭐ Total inventory value by branch"""
        
        # Join inventory with product prices
        merged = self.inventory_df.merge(
            self.products_df[['product_id', 'unit_price']], 
            on='product_id'
        )
        
        # Calculate stock value
        merged['stock_value'] = merged['stock_level'] * merged['unit_price']
        
        # Summary
        total_value = merged['stock_value'].sum()
        total_units = merged['stock_level'].sum()
        
        # By branch
        by_branch = merged.groupby('branch_id').agg({
            'stock_value': 'sum',
            'stock_level': 'sum',
            'product_id': 'count'
        }).reset_index()
        
        by_branch.columns = ['branch_id', 'inventory_value', 'total_units', 'unique_products']
        
        # Join branch names
        by_branch = by_branch.merge(
            self.branches_df[['branch_id', 'branch_name', 'city']], 
            on='branch_id'
        )
        
        branch_valuations = []
        for _, row in by_branch.iterrows():
            branch_valuations.append({
                'branch_id': row['branch_id'],
                'branch_name': row['branch_name'],
                'city': row['city'],
                'inventory_value': float(row['inventory_value']),
                'total_units': int(row['total_units']),
                'unique_products': int(row['unique_products'])
            })
        
        return {
            'total_inventory_value': float(total_value),
            'total_units_in_stock': int(total_units),
            'by_branch': sorted(branch_valuations, key=lambda x: x['inventory_value'], reverse=True)
        }

    def get_portfolio_snapshot(self, user_id: str = None) -> dict:
        """Generate a portfolio snapshot from current inventory and product pricing."""
        # Aggregate current holdings by product across all branches
        grouped = self.inventory_df.groupby('product_id', as_index=False).agg({'stock_level': 'sum'})
        merged = grouped.merge(
            self.products_df[['product_id', 'product_name', 'category', 'unit_price']],
            on='product_id',
            how='left'
        )

        holdings = {}
        total_value = 0.0

        for _, row in merged.iterrows():
            quantity = int(row['stock_level'])
            if quantity <= 0:
                continue

            unit_price = float(row['unit_price']) if not pd.isna(row['unit_price']) else 0.0
            current_value = quantity * unit_price
            holdings[row['product_id']] = {
                'product_id': row['product_id'],
                'product_name': row['product_name'],
                'category': row['category'],
                'quantity': quantity,
                'buy_price': unit_price,
                'current_price': unit_price,
                'total_value': float(current_value)
            }
            total_value += current_value

        return {
            'total_invested': float(total_value),
            'current_value': float(total_value),
            'profit_loss': 0.0,
            'profit_loss_percent': 0.0,
            'holdings': holdings
        }
