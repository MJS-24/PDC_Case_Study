import pandas as pd
from typing import List, Dict


def calculate_moving_average(df: pd.DataFrame, symbol: str, window: int = 10) -> List[float]:
    """
    Calculate moving average for a stock symbol
    
    Args:
        df: DataFrame with stock data
        symbol: Stock symbol
        window: Window size for moving average
        
    Returns:
        List of moving average values
    """
    stock_data = df[df['symbol'] == symbol].sort_values('timestamp')
    
    if len(stock_data) < window:
        return []
    
    return stock_data['close'].rolling(window=window).mean().tolist()


def calculate_volatility(df: pd.DataFrame, symbol: str, window: int = 20) -> float:
    """
    Calculate volatility (standard deviation) for a stock
    
    Args:
        df: DataFrame with stock data
        symbol: Stock symbol
        window: Window size for volatility calculation
        
    Returns:
        Volatility value
    """
    stock_data = df[df['symbol'] == symbol].sort_values('timestamp')
    
    if len(stock_data) < window:
        return stock_data['close'].std()
    
    return stock_data['close'].rolling(window=window).std().mean()
