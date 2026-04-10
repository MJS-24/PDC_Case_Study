import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
from typing import Dict, Tuple


def process_stock_chunk(chunk_data: Tuple[str, pd.DataFrame]) -> Dict:
    """
    Process a chunk of stock data for a single symbol
    Used for parallel processing via multiprocessing
    
    Args:
        chunk_data: Tuple of (symbol, dataframe chunk)
        
    Returns:
        Dictionary with analysis results
    """
    symbol, df = chunk_data
    
    if df.empty:
        return {
            'symbol': symbol,
            'records': 0,
            'avg_price': 0,
            'volatility': 0,
            'price_range': (0, 0)
        }
    
    # Calculate statistics
    avg_price = df['close'].mean()
    volatility = df['close'].std()
    price_min = df['close'].min()
    price_max = df['close'].max()
    
    return {
        'symbol': symbol,
        'records': len(df),
        'avg_price': avg_price,
        'volatility': volatility,
        'price_range': (price_min, price_max),
        'latest_price': df.iloc[-1]['close'] if len(df) > 0 else 0
    }


def analyze_stocks_parallel(df: pd.DataFrame) -> Dict[str, Dict]:
    """
    Analyze stock data using parallel processing (multiprocessing)
    Demonstrates distributed computing by processing each stock in parallel
    
    Args:
        df: DataFrame with stock data
        
    Returns:
        Dictionary with analysis results for all stocks
    """
    if df.empty:
        return {}
    
    # Group data by stock symbol
    grouped = [(symbol, group) for symbol, group in df.groupby('symbol')]
    
    # Use multiprocessing to process chunks in parallel
    num_processes = min(cpu_count(), len(grouped))
    
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_stock_chunk, grouped)
    
    # Convert list of results to dictionary
    analysis_dict = {result['symbol']: result for result in results}
    return analysis_dict
