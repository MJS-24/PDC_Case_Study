import pandas as pd
from typing import Dict, Tuple, List
import uuid
from ..data_processing import load_csv_data, get_latest_price


class PortfolioService:
    """Service for managing user portfolio"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = load_csv_data(csv_path)
        self.portfolios = {}  # In-memory storage (would use DB in production)
    
    def create_portfolio(self, user_id: str) -> Dict:
        """Create a new portfolio for a user"""
        if user_id not in self.portfolios:
            self.portfolios[user_id] = {
                'user_id': user_id,
                'holdings': {},  # {symbol: {'quantity': int, 'buy_price': float}}
                'transactions': [],
                'cash': 100000  # Starting cash
            }
        
        return self.portfolios[user_id]
    
    def get_portfolio(self, user_id: str) -> Dict:
        """Get user's portfolio with current values"""
        if user_id not in self.portfolios:
            self.create_portfolio(user_id)
        
        portfolio = self.portfolios[user_id]
        
        # Calculate current values
        total_invested = 0
        current_value = 0
        
        for symbol, holding in portfolio['holdings'].items():
            quantity = holding['quantity']
            buy_price = holding['buy_price']
            
            # Get current price
            current_price, _ = self._get_current_price(symbol)
            
            total_invested += quantity * buy_price
            current_value += quantity * current_price
        
        profit_loss = current_value - total_invested
        profit_loss_percent = (profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        return {
            'user_id': user_id,
            'total_invested': round(total_invested, 2),
            'current_value': round(current_value, 2),
            'profit_loss': round(profit_loss, 2),
            'profit_loss_percent': round(profit_loss_percent, 2),
            'cash': round(portfolio['cash'], 2),
            'holdings': {
                symbol: {
                    'quantity': holding['quantity'],
                    'buy_price': round(holding['buy_price'], 2),
                    'current_price': round(self._get_current_price(symbol)[0], 2),
                    'value': round(holding['quantity'] * self._get_current_price(symbol)[0], 2)
                }
                for symbol, holding in portfolio['holdings'].items()
            },
            'transaction_count': len(portfolio['transactions'])
        }
    
    def buy_stock(self, user_id: str, symbol: str, quantity: int) -> Dict:
        """
        Buy a stock for the user
        
        Args:
            user_id: User ID
            symbol: Stock symbol
            quantity: Number of shares to buy
            
        Returns:
            Dictionary with transaction details
        """
        if user_id not in self.portfolios:
            self.create_portfolio(user_id)
        
        portfolio = self.portfolios[user_id]
        current_price, date = self._get_current_price(symbol)
        
        if current_price == 0:
            return {
                'success': False,
                'message': f'Stock {symbol} not found',
                'transaction_id': None
            }
        
        total_cost = current_price * quantity
        
        if portfolio['cash'] < total_cost:
            return {
                'success': False,
                'message': f'Insufficient funds. Available: ${portfolio["cash"]:.2f}, Required: ${total_cost:.2f}',
                'transaction_id': None
            }
        
        # Process buy
        portfolio['cash'] -= total_cost
        
        if symbol in portfolio['holdings']:
            # Calculate new average buy price
            old_quantity = portfolio['holdings'][symbol]['quantity']
            old_buy_price = portfolio['holdings'][symbol]['buy_price']
            new_quantity = old_quantity + quantity
            new_buy_price = ((old_quantity * old_buy_price) + (quantity * current_price)) / new_quantity
            
            portfolio['holdings'][symbol] = {
                'quantity': new_quantity,
                'buy_price': new_buy_price
            }
        else:
            portfolio['holdings'][symbol] = {
                'quantity': quantity,
                'buy_price': current_price
            }
        
        # Record transaction
        transaction_id = str(uuid.uuid4())
        portfolio['transactions'].append({
            'id': transaction_id,
            'symbol': symbol,
            'type': 'BUY',
            'quantity': quantity,
            'price': current_price,
            'total': total_cost,
            'date': date
        })
        
        return {
            'success': True,
            'message': f'Successfully bought {quantity} shares of {symbol} at ${current_price:.2f}',
            'transaction_id': transaction_id,
            'price': current_price,
            'total_amount': total_cost
        }
    
    def sell_stock(self, user_id: str, symbol: str, quantity: int) -> Dict:
        """
        Sell a stock for the user
        
        Args:
            user_id: User ID
            symbol: Stock symbol
            quantity: Number of shares to sell
            
        Returns:
            Dictionary with transaction details
        """
        if user_id not in self.portfolios:
            return {
                'success': False,
                'message': 'Portfolio not found',
                'transaction_id': None
            }
        
        portfolio = self.portfolios[user_id]
        
        if symbol not in portfolio['holdings']:
            return {
                'success': False,
                'message': f'You do not own any shares of {symbol}',
                'transaction_id': None
            }
        
        holding = portfolio['holdings'][symbol]
        if holding['quantity'] < quantity:
            return {
                'success': False,
                'message': f'Insufficient shares. You have {holding["quantity"]} shares',
                'transaction_id': None
            }
        
        current_price, date = self._get_current_price(symbol)
        total_proceeds = current_price * quantity
        profit_loss = (current_price - holding['buy_price']) * quantity
        
        # Process sell
        portfolio['cash'] += total_proceeds
        holding['quantity'] -= quantity
        
        if holding['quantity'] == 0:
            del portfolio['holdings'][symbol]
        
        # Record transaction
        transaction_id = str(uuid.uuid4())
        portfolio['transactions'].append({
            'id': transaction_id,
            'symbol': symbol,
            'type': 'SELL',
            'quantity': quantity,
            'price': current_price,
            'total': total_proceeds,
            'profit_loss': profit_loss,
            'date': date
        })
        
        return {
            'success': True,
            'message': f'Successfully sold {quantity} shares of {symbol} at ${current_price:.2f}',
            'transaction_id': transaction_id,
            'price': current_price,
            'total_amount': total_proceeds,
            'profit_loss': profit_loss
        }
    
    def get_transactions(self, user_id: str, limit: int = 50) -> List[Dict]:
        """
        Get transaction history for a user
        
        Args:
            user_id: User ID
            limit: Number of transactions to return
            
        Returns:
            List of transactions
        """
        if user_id not in self.portfolios:
            return []
        
        transactions = self.portfolios[user_id]['transactions']
        return transactions[-limit:]
    
    def _get_current_price(self, symbol: str) -> Tuple[float, str]:
        """Get current price for a symbol"""
        return get_latest_price(self.df, symbol)
