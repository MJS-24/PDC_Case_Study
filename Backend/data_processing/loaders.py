"""Stock data loading with validation"""

import pandas as pd
from pathlib import Path
from utils.path_utils import DataPathResolver
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class StockDataLoader:
    """Load stock market data with validation"""

    # CSV file registry
    DATASETS = {
        'stock_data': 'stock_details_5_years.csv',
    }

    def __init__(self):
        """Initialize loader"""
        self.stock_data: Dict[str, pd.DataFrame] = {}
        self.stocks_list: List[Dict] = []

    def load_stock_data(self) -> Dict[str, pd.DataFrame]:
        """Load stock data grouped by symbol"""
        if not self.stock_data:
            try:
                df = pd.read_csv(DataPathResolver.get_csv_path(self.DATASETS['stock_data']))

                # Validate schema
                required = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Company']
                missing = [col for col in required if col not in df.columns]
                if missing:
                    raise ValueError(f"Missing columns in stock_details_5_years.csv: {missing}")

                # Convert types
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
                df['High'] = pd.to_numeric(df['High'], errors='coerce')
                df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
                df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
                df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
                df['Dividends'] = pd.to_numeric(df['Dividends'], errors='coerce')
                df['Stock Splits'] = pd.to_numeric(df['Stock Splits'], errors='coerce')

                # Drop rows with invalid data
                df = df.dropna(subset=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

                # Group by company and sort by date
                for symbol in df['Company'].unique():
                    symbol_df = df[df['Company'] == symbol].copy()
                    symbol_df = symbol_df.sort_values('Date').reset_index(drop=True)
                    self.stock_data[symbol] = symbol_df

                # Create stocks list
                self.stocks_list = []
                for company, data in self.stock_data.items():
                    latest = data.iloc[-1]
                    if latest is not None:
                        close = float(latest['Close'])
                        open_price = float(latest['Open'])
                        volume = int(latest['Volume'])
                        change = float(((close - open_price) / open_price * 100) if open_price != 0 else 0)
                        self.stocks_list.append({
                            'company': company,
                            'name': company,  # Could map to full names if available
                            'current_price': close,
                            'change': change,
                            'volume': volume
                        })

                logger.info(f"✓ Loaded data for {len(self.stock_data)} stocks")
                print(f"✓ Loaded data for {len(self.stock_data)} stocks")

            except Exception as e:
                logger.error(f"✗ Error loading stock data: {e}")
                raise

        return self.stock_data

    def get_stocks_list(self) -> List[Dict]:
        """Get list of available stocks"""
        if not self.stocks_list:
            self.load_stock_data()
        return self.stocks_list

    def get_stock_data(self, company: str) -> pd.DataFrame:
        """Get historical data for a specific stock"""
        if not self.stock_data:
            self.load_stock_data()
        return self.stock_data.get(company, pd.DataFrame())

    def get_latest_price(self, company: str) -> float:
        """Get latest closing price for a stock"""
        data = self.get_stock_data(company)
        if not data.empty:
            return data.iloc[-1]['Close']
        return 0.0
    
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
