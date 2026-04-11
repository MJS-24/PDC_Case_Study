"""Stock service for loading and providing stock data"""

import pandas as pd
from typing import List, Dict, Any
from data_processing.loaders import StockDataLoader
import logging

logger = logging.getLogger(__name__)

class StockService:
    """Service for stock data operations"""

    def __init__(self, loader: StockDataLoader):
        self.loader = loader
        self.loader.load_stock_data()

    def get_all_stocks(self) -> List[Dict[str, Any]]:
        """Get list of all available stocks"""
        return self.loader.get_stocks_list()

    def get_stock_history(self, company: str) -> List[Dict[str, Any]]:
        """Get historical price data for a stock"""
        df = self.loader.get_stock_data(company)
        if df.empty:
            return []

        # Convert to list of dicts for API
        history = []
        for _, row in df.iterrows():
            history.append({
                'date': row['Date'].isoformat(),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            })

        return history