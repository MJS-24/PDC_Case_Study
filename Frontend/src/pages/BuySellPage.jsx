import React, { useEffect, useState } from 'react';
import { stockApi, portfolioApi } from '../services/api';
import StockChart from '../charts/StockChart';

export default function BuySellPage({ selectedCompany, onCompanyChange }) {
  const [company, setCompany] = useState(selectedCompany || 'AAPL');
  const [quantity, setQuantity] = useState(1);
  const [history, setHistory] = useState([]);
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [transactionType, setTransactionType] = useState('buy');
  const [availableStocks, setAvailableStocks] = useState([]);

  useEffect(() => {
    setCompany(selectedCompany || 'AAPL');
  }, [selectedCompany]);

  useEffect(() => {
    fetchStocks();
  }, []);

  useEffect(() => {
    fetchData();
  }, [company]);

  const fetchStocks = async () => {
    try {
      const stocks = await stockApi.getAllStocks();
      setAvailableStocks(stocks);
    } catch (error) {
      console.error('Error fetching stocks:', error);
    }
  };

  const fetchData = async () => {
    console.log('BuySellPage: Fetching data for', company);
    setLoading(true);
    try {
      const [historyData, portfolioData] = await Promise.all([
        stockApi.getStockHistory(company),
        portfolioApi.getPortfolio(),
      ]);
      console.log('BuySellPage: Data fetched', { historyData, portfolioData });
      setHistory(historyData.history || []);
      setPortfolio(portfolioData);
    } catch (error) {
      console.error('BuySellPage: Error fetching data:', error);
      setMessage({ type: 'error', text: 'Failed to load data' });
    } finally {
      setLoading(false);
    }
  };

  const handleBuy = async () => {
    if (quantity <= 0) {
      setMessage({ type: 'error', text: 'Quantity must be greater than 0' });
      return;
    }

    try {
      const result = await portfolioApi.buyStock(company, parseInt(quantity));
      if (result.success) {
        setMessage({
          type: 'success',
          text: `✓ Bought ${quantity} shares of ${company}`,
        });
        setQuantity(1);
        fetchData();
        if (onCompanyChange) onCompanyChange(company);
      } else {
        setMessage({ type: 'error', text: result.message });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Transaction failed' });
      console.error(error);
    }
  };

  const handleSell = async () => {
    if (quantity <= 0) {
      setMessage({ type: 'error', text: 'Quantity must be greater than 0' });
      return;
    }

    try {
      const result = await portfolioApi.sellStock(company, parseInt(quantity));
      if (result.success) {
        setMessage({
          type: 'success',
          text: `✓ Sold ${quantity} shares of ${company}`,
        });
        setQuantity(1);
        fetchData();
        if (onCompanyChange) onCompanyChange(company);
      } else {
        setMessage({ type: 'error', text: result.message });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Transaction failed' });
      console.error(error);
    }
  };

  const holding = portfolio?.holdings?.find(h => h.company === company);
  const currentPrice = history.length > 0 ? history[history.length - 1].close : 0;
  const currentValue = currentPrice * quantity;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-white mb-8 text-center">💰 Buy / Sell Stocks</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart */}
        <div className="lg:col-span-2">
          {loading ? (
            <div className="bg-gray-800 rounded-lg p-6 text-center text-gray-400">
              Loading chart data...
            </div>
          ) : history.length > 0 ? (
            <StockChart data={history} symbol={company} />
          ) : (
            <div className="bg-gray-800 rounded-lg p-6 text-center text-gray-400">
              No chart data available for {company}
            </div>
          )}
        </div>

        {/* Trade Panel */}
        <div>
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            {/* Stock Selector */}
            <div className="mb-6">
              <label className="block text-gray-300 text-sm mb-2">
                Select Company
              </label>
              <select
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:border-green-500"
              >
                {availableStocks.map((stock) => (
                  <option key={stock.company} value={stock.company}>
                    {stock.company} - {stock.name}
                  </option>
                ))}
              </select>
            </div>

            <h2 className="text-2xl font-bold text-white mb-6">
              {company}
            </h2>

            <div className="space-y-3 mb-6">
              <div className="bg-gray-700 rounded-lg p-3">
                <p className="text-gray-400 text-sm">Current Price</p>
                <p className="text-2xl font-bold text-green-400">
                  ${currentPrice.toFixed(2)}
                </p>
              </div>

              {holding && (
                <div className="bg-gray-700 rounded-lg p-3">
                  <p className="text-gray-400 text-sm">You Own</p>
                  <p className="text-lg font-bold text-white">
                    {holding.shares} shares
                  </p>
                  <p className="text-xs text-gray-400">
                    @ ${holding.avg_price.toFixed(2)}
                  </p>
                </div>
              )}
            </div>

            {/* Trade Section */}
            <div className="border-t border-gray-700 pt-6">
              <div className="mb-4">
                <label className="block text-gray-300 text-sm mb-2">
                  Quantity
                </label>
                <input
                  type="number"
                  min="1"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:border-green-500"
                />
              </div>

              <div className="mb-4 text-sm">
                <p className="text-gray-400">Total Value</p>
                <p className="text-xl font-bold text-white">
                  ${currentValue.toFixed(2)}
                </p>
              </div>

              <div className="space-y-2">
                <button
                  onClick={handleBuy}
                  disabled={loading}
                  className="w-full bg-green-500 hover:bg-green-600 text-white py-3 rounded-lg font-semibold transition-colors disabled:bg-gray-600"
                >
                  🟢 Buy Now
                </button>

                {holding && (
                  <button
                    onClick={handleSell}
                    disabled={loading}
                    className="w-full bg-red-500 hover:bg-red-600 text-white py-3 rounded-lg font-semibold transition-colors disabled:bg-gray-600"
                  >
                    🔴 Sell Now
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Message */}
      {message && (
        <div
          className={`mt-6 p-4 rounded-lg ${
            message.type === 'success'
              ? 'bg-green-900 text-green-300'
              : 'bg-red-900 text-red-300'
          }`}
        >
          {message.text}
        </div>
      )}
    </div>
  );
}
