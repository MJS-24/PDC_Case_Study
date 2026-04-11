"""Portfolio service for computing holdings and balance"""

from typing import List, Dict, Any
import logging
import json
import os
from .transaction_service import TransactionService
from .stock_service import StockService

logger = logging.getLogger(__name__)

BALANCE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'balance.json')

class PortfolioService:
    """Service for managing portfolio and computing holdings"""

    def __init__(self, stock_service: StockService, transaction_service: TransactionService):
        self.stock_service = stock_service
        self.transaction_service = transaction_service
        self.balance = self._load_balance()

    def _load_balance(self) -> float:
        """Load balance from file"""
        try:
            if os.path.exists(BALANCE_FILE):
                with open(BALANCE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('balance', 10000.0)
        except Exception as e:
            logger.error(f"Error loading balance: {e}")
        return 10000.0

    def _save_balance(self):
        """Save balance to file"""
        try:
            os.makedirs(os.path.dirname(BALANCE_FILE), exist_ok=True)
            with open(BALANCE_FILE, 'w') as f:
                json.dump({'balance': self.balance}, f)
        except Exception as e:
            logger.error(f"Error saving balance: {e}")

    def get_balance(self) -> float:
        """Get current balance"""
        return self.balance

    def add_balance(self, amount: float) -> Dict[str, Any]:
        """Add funds to balance"""
        if amount <= 0:
            return {'success': False, 'message': 'Amount must be positive'}
        self.balance += amount
        self._save_balance()
        return {'success': True, 'message': f'Added ${amount:.2f} to balance', 'new_balance': self.balance}

    def buy_stock(self, company: str, quantity: int) -> Dict[str, Any]:
        """Execute buy transaction"""
        if quantity <= 0:
            return {'success': False, 'message': 'Quantity must be positive'}

        # Get current price (use latest close)
        stocks = self.stock_service.get_all_stocks()
        stock = next((s for s in stocks if s['company'] == company), None)
        if not stock:
            return {'success': False, 'message': 'Stock not found'}

        current_price = stock['current_price']
        total_cost = current_price * quantity

        if total_cost > self.balance:
            return {'success': False, 'message': 'Insufficient funds'}

        # Record transaction
        transaction = self.transaction_service.buy_stock(company, quantity, current_price)
        self.balance -= total_cost
        self._save_balance()

        return {
            'success': True,
            'message': f'Bought {quantity} shares of {company} at ${current_price:.2f}',
            'transaction': transaction
        }

    def sell_stock(self, company: str, quantity: int) -> Dict[str, Any]:
        """Execute sell transaction"""
        if quantity <= 0:
            return {'success': False, 'message': 'Quantity must be positive'}

        # Check if we have enough shares
        holdings = self._compute_holdings()
        holding = next((h for h in holdings if h['company'] == company), None)
        if not holding or holding['shares'] < quantity:
            return {'success': False, 'message': 'Insufficient shares'}

        # Get current price
        stocks = self.stock_service.get_all_stocks()
        stock = next((s for s in stocks if s['company'] == company), None)
        current_price = stock['current_price'] if stock else 0
        total_value = current_price * quantity

        # Record transaction
        transaction = self.transaction_service.sell_stock(company, quantity, current_price)
        self.balance += total_value
        self._save_balance()

        return {
            'success': True,
            'message': f'Sold {quantity} shares of {company} at ${current_price:.2f}',
            'transaction': transaction
        }

    def get_portfolio(self) -> Dict[str, Any]:
        """Get portfolio with holdings and summary"""
        holdings = self._compute_holdings()
        total_value = sum(h['value'] for h in holdings)
        total_cost = sum(h['cost'] for h in holdings)
        total_pnl = total_value - total_cost
        total_pnl_percent = (total_pnl / total_cost * 100) if total_cost > 0 else 0

        return {
            'holdings': holdings,
            'total_value': total_value,
            'total_cost': total_cost,
            'total_pnl': total_pnl,
            'total_pnl_percent': total_pnl_percent,
            'cash': self.balance,
            'portfolio_value': total_value + self.balance
        }

    def _compute_holdings(self) -> List[Dict[str, Any]]:
        """Compute current holdings from transactions"""
        transactions = self.transaction_service.get_transactions()
        holdings_dict = {}

        for tx in transactions:
            company = tx['company']
            if company not in holdings_dict:
                holdings_dict[company] = {'shares': 0, 'total_cost': 0}

            if tx['type'] == 'buy':
                holdings_dict[company]['shares'] += tx['quantity']
                holdings_dict[company]['total_cost'] += tx['price'] * tx['quantity']
            elif tx['type'] == 'sell':
                holdings_dict[company]['shares'] -= tx['quantity']
                # For simplicity, don't adjust cost on sell

        # Get current prices
        stocks = self.stock_service.get_all_stocks()
        stock_prices = {s['company']: s['current_price'] for s in stocks}

        holdings = []
        for company, data in holdings_dict.items():
            if data['shares'] > 0:
                current_price = stock_prices.get(company, 0)
                avg_price = data['total_cost'] / data['shares'] if data['shares'] > 0 else 0
                value = data['shares'] * current_price
                cost = data['total_cost']
                pnl = value - cost
                pnl_percent = (pnl / cost * 100) if cost > 0 else 0

                holdings.append({
                    'company': company,
                    'shares': data['shares'],
                    'avg_price': avg_price,
                    'current_price': current_price,
                    'value': value,
                    'cost': cost,
                    'pnl': pnl,
                    'pnl_percent': pnl_percent
                })

        return holdings