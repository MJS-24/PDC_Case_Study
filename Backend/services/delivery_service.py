"""Logistics and delivery analytics"""

import pandas as pd


class DeliveryService:
    """Logistics and delivery analytics"""
    
    def __init__(self, loader):
        self.loader = loader
        self.deliveries_df = loader.load_deliveries()
        self.trucks_df = loader.load_trucks()
        self.branches_df = loader.load_branches()
    
    def get_delivery_summary(self) -> dict:
        """Overall delivery performance"""
        
        statuses = self.deliveries_df['status'].value_counts().to_dict()
        
        return {
            'completed': int(statuses.get('Completed', 0)),
            'delayed': int(statuses.get('Delayed', 0)),
            'cancelled': int(statuses.get('Cancelled', 0)),
            'on_time_rate': float(
                statuses.get('Completed', 0) / len(self.deliveries_df) * 100
                if len(self.deliveries_df) > 0 else 0
            ),
            'total_distance_km': float(self.deliveries_df['distance_km'].sum()),
            'total_fuel_liters': float(self.deliveries_df['fuel_consumed_liters'].sum())
        }
    
    def get_delayed_deliveries(self) -> list:
        """Get all delayed deliveries"""
        
        delayed = self.deliveries_df[
            self.deliveries_df['status'] == 'Delayed'
        ].copy()
        
        # Join truck info
        delayed = delayed.merge(
            self.trucks_df[['truck_id', 'type', 'capacity_kg']], 
            on='truck_id'
        )
        
        result = []
        for _, row in delayed.iterrows():
            result.append({
                'delivery_id': row['delivery_id'],
                'truck_id': row['truck_id'],
                'truck_type': row['type'],
                'timestamp': row['timestamp'].isoformat(),
                'origin_branch': row['origin_branch'],
                'destination_branch': row['destination_branch'],
                'distance_km': float(row['distance_km']),
                'fuel_consumed_liters': float(row['fuel_consumed_liters']),
                'status': row['status']
            })
        
        return result
