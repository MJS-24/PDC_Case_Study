import pandas as pd
from typing import Dict, Tuple, List
from ..data_processing import load_csv_data


class StockAnalysisService:
    """Service for analyzing stocks and generating recommendations"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = load_csv_data(csv_path)
        self.analysis_cache = {}
    
    def get_stock_recommendation(self, symbol: str) -> Dict:
        """
        Generate a buy/sell/hold recommendation for a stock
        Based on:
        - Moving average crossover
        - Volatility
        - Price trends
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with recommendation and analysis
        """
        if self.df.empty or symbol not in self.df['symbol'].values:
            return {
                'symbol': symbol,
                'recommendation': 'HOLD',
                'confidence': 0,
                'signal': 'No data available'
            }
        
        stock_data = self.df[self.df['symbol'] == symbol].sort_values('timestamp')
        
        if len(stock_data) < 20:
            return {
                'symbol': symbol,
                'recommendation': 'HOLD',
                'confidence': 0,
                'signal': 'Insufficient data'
            }
        
        # Calculate technical indicators
        current_price = stock_data.iloc[-1]['close']
        prev_price = stock_data.iloc[-2]['close'] if len(stock_data) > 1 else current_price
        
        # Moving averages
        ma_10 = stock_data['close'].tail(10).mean()
        ma_20 = stock_data['close'].tail(20).mean()
        
        # Volatility
        volatility = stock_data['close'].std()
        
        # Price momentum
        price_change = ((current_price - stock_data.iloc[0]['close']) / 
                       stock_data.iloc[0]['close'] * 100)
        
        # Generate recommendation
        recommendation, confidence, signal = self._generate_signal(
            current_price, ma_10, ma_20, volatility, price_change
        )
        
        return {
            'symbol': symbol,
            'current_price': round(current_price, 2),
            'moving_avg_10': round(ma_10, 2),
            'moving_avg_20': round(ma_20, 2),
            'volatility': round(volatility, 2),
            'price_change_percent': round(price_change, 2),
            'recommendation': recommendation,
            'confidence': confidence,
            'signal': signal
        }
    
    def _generate_signal(self, price: float, ma_10: float, ma_20: float, 
                        volatility: float, momentum: float) -> Tuple[str, float, str]:
        """
        Generate trading signal based on indicators
        
        Args:
            price: Current price
            ma_10: 10-day moving average
            ma_20: 20-day moving average
            volatility: Price volatility
            momentum: Price momentum percentage
            
        Returns:
            Tuple of (recommendation, confidence, signal)
        """
        signals = 0
        confidence = 0
        signal_reasons = []
        
        # Signal 1: Moving average crossover
        if ma_10 > ma_20:
            signals += 1
            signal_reasons.append("MA10 > MA20 (Bullish)")
        else:
            signals -= 1
            signal_reasons.append("MA10 < MA20 (Bearish)")
        
        # Signal 2: Price vs moving averages
        if price > ma_10:
            signals += 1
            signal_reasons.append("Price above MA10")
        else:
            signals -= 1
            signal_reasons.append("Price below MA10")
        
        # Signal 3: Momentum
        if momentum > 2:
            signals += 1
            signal_reasons.append(f"Positive momentum ({momentum:.2f}%)")
        elif momentum < -2:
            signals -= 1
            signal_reasons.append(f"Negative momentum ({momentum:.2f}%)")
        
        # Volatility consideration (increase confidence)
        volatility_factor = min(volatility / 10, 1)  # Normalize volatility
        
        # Determine recommendation
        if signals >= 2:
            recommendation = "BUY"
            confidence = min(0.8 + volatility_factor * 0.2, 1.0)
        elif signals <= -2:
            recommendation = "SELL"
            confidence = min(0.8 + volatility_factor * 0.2, 1.0)
        else:
            recommendation = "HOLD"
            confidence = 0.5
        
        signal_text = " | ".join(signal_reasons)
        
        return recommendation, round(confidence, 2), signal_text
    
    def get_all_stocks_analysis(self) -> List[Dict]:
        """
        Get analysis for all stocks in the dataset
        
        Returns:
            List of dictionaries with analysis for each stock
        """
        if self.df.empty:
            return []
        
        symbols = self.df['symbol'].unique()
        analysis = []
        
        for symbol in symbols:
            analysis.append(self.get_stock_recommendation(symbol))
        
        return analysis
    
    def get_stock_price_history(self, symbol: str, limit: int = 20) -> List[Dict]:
        """
        Get price history for a stock
        
        Args:
            symbol: Stock symbol
            limit: Number of records to return
            
        Returns:
            List of price data points
        """
        if symbol not in self.df['symbol'].values:
            return []
        
        stock_data = self.df[self.df['symbol'] == symbol].sort_values('timestamp').tail(limit)
        
        return [
            {
                'date': str(row['timestamp'].date()),
                'open': round(row['open'], 2),
                'high': round(row['high'], 2),
                'low': round(row['low'], 2),
                'close': round(row['close'], 2),
                'volume': int(row['volume'])
            }
            for _, row in stock_data.iterrows()
        ]
