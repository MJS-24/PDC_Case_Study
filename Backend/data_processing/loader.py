import pandas as pd
from typing import Tuple


def load_csv_data(csv_path: str) -> pd.DataFrame:
    """
    Load stock data from CSV file
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        DataFrame with stock data
    """
    try:
        df = pd.read_csv(csv_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()


def get_latest_price(df: pd.DataFrame, symbol: str) -> Tuple[float, str]:
    """
    Get the latest price for a stock
    
    Args:
        df: DataFrame with stock data
        symbol: Stock symbol
        
    Returns:
        Tuple of (price, date)
    """
    stock_data = df[df['symbol'] == symbol].sort_values('timestamp')
    
    if stock_data.empty:
        return 0, ""
    
    latest = stock_data.iloc[-1]
    return latest['close'], str(latest['timestamp'].date())
