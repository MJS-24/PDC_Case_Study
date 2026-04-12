"""ML-OPTIMIZED stock service (FAST + simulation-aware + scalable)"""

from typing import List, Dict, Any
from data_processing.loaders import StockDataLoader
from models.ml_model import StockMLModel
import logging

logger = logging.getLogger(__name__)


class StockService:
    """Ultra-fast stock service with ML (optimized)"""

    def __init__(self, loader: StockDataLoader):
        self.loader = loader

        # Cached data
        self.stocks = self.loader.get_stocks_list()
        self.data = self.loader.stock_data

        # 🔥 ML MODEL
        self.model = StockMLModel()
        self._train_model()

    # ========================
    # ML TRAINING (ONCE)
    # ========================

    def _train_model(self):
        try:
            self.model.train(self.data)
            logger.info("✅ ML model trained (optimized)")
        except Exception as e:
            logger.error(f"ML training failed: {e}")

    # ========================
    # INTERNAL UTIL (FAST)
    # ========================

    def _get_index(self, index, length):
        if index is not None:
            return min(max(index, 0), length - 1)
        return length - 1

    def _get_analysis(self, prices, idx):
        start = max(0, idx - 10)
        relevant_prices = prices[start:idx + 1]
        return self.model.predict(relevant_prices)

    # ========================
    # CORE API METHODS
    # ========================

    def get_all_stocks(self, index: int = None) -> List[Dict[str, Any]]:
        """
        🔥 Optimized stock list (still ML-powered)
        """

        result = []

        for stock in self.stocks:
            company = stock["company"]
            data = self.data.get(company)

            if not data:
                continue

            prices = data["prices"]
            length = data["length"]

            idx = self._get_index(index, length)
            current_price = prices[idx]

            analysis = self._get_analysis(prices, idx)

            result.append({
                "company": company,
                "name": stock["name"],
                "price": round(current_price, 2),
                "confidence": analysis["confidence"],
                "action": analysis["action"]
            })

        return result

    # ========================
    # 🔥 NEW: FAST SINGLE STOCK (CRITICAL FIX)
    # ========================

    def get_single_stock(self, company: str, index: int = None):
        """
        🚀 MUCH faster than filtering get_all_stocks
        """

        data = self.data.get(company)
        if not data:
            return None

        prices = data["prices"]
        length = data["length"]

        idx = self._get_index(index, length)
        current_price = prices[idx]

        analysis = self._get_analysis(prices, idx)

        return {
            "company": company,
            "price": round(current_price, 2),
            "confidence": analysis["confidence"],
            "action": analysis["action"]
        }

    # ========================
    # HISTORY
    # ========================

    def get_stock_history(self, company: str, limit: int = 100, index: int = None) -> List[Dict[str, Any]]:
        data = self.data.get(company)
        if not data:
            return []

        prices = data["prices"]
        length = data["length"]

        end = self._get_index(index, length)
        start = max(0, end - limit)

        return [
            {
                "index": i,
                "close": prices[i]
            }
            for i in range(start, end + 1)
        ]

    # ========================
    # PRICE
    # ========================

    def get_price_at_index(self, company: str, index: int) -> float:
        return self.loader.get_price_at_index(company, index)