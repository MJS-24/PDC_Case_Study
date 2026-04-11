import React, { useEffect, useState } from 'react';
import { stockApi, portfolioApi } from '../services/api';

export default function DashboardPage() {
  const [portfolio, setPortfolio] = useState(null);
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    console.log('DashboardPage: Fetching data...');
    try {
      const [portfolioData, stocksData] = await Promise.all([
        portfolioApi.getPortfolio(),
        stockApi.getAllStocks()
      ]);
      console.log('DashboardPage: Data fetched successfully', { portfolioData, stocksData });
      setPortfolio(portfolioData);
      setStocks(stocksData);
      setError(null);
    } catch (err) {
      console.error('DashboardPage: Data fetch error:', err);
      setError('Failed to fetch data');
      setPortfolio(null);
      setStocks([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-white text-center py-10">Loading portfolio...</div>;
  }

  if (error) {
    return <div className="text-red-400 text-center py-10">{error}</div>;
  }

  const profitLossColor = portfolio?.total_pnl >= 0 ? 'text-green-400' : 'text-red-400';
  const profitLossBgColor = portfolio?.total_pnl >= 0 ? 'bg-green-900' : 'bg-red-900';

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-8">📊 Dashboard</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <p className="text-gray-400 text-sm">Total Invested</p>
          <p className="text-2xl font-bold text-white mt-2">
            ${portfolio?.total_cost?.toFixed(2) || '0.00'}
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <p className="text-gray-400 text-sm">Current Value</p>
          <p className="text-2xl font-bold text-white mt-2">
            ${portfolio?.total_value?.toFixed(2) || '0.00'}
          </p>
        </div>

        <div className={`rounded-lg p-6 shadow-lg ${profitLossBgColor}`}>
          <p className="text-gray-300 text-sm">Profit/Loss</p>
          <p className={`text-2xl font-bold mt-2 ${profitLossColor}`}>
            ${portfolio?.total_pnl?.toFixed(2) || '0.00'}
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <p className="text-gray-400 text-sm">Return %</p>
          <p className={`text-2xl font-bold mt-2 ${profitLossColor}`}>
            {portfolio?.total_pnl_percent?.toFixed(2) || '0.00'}%
          </p>
        </div>
      </div>

      {/* Holdings */}
      <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
        <h2 className="text-xl font-bold text-white mb-4">📈 Current Holdings</h2>

        {portfolio?.holdings?.length === 0 ? (
          <p className="text-gray-400">No active holdings. Start trading!</p>
        ) : (
          <div className="space-y-3">
            {portfolio.holdings.map((holding) => (
              <div
                key={holding.company}
                className="bg-gray-700 rounded-lg p-4 flex justify-between items-center"
              >
                <div>
                  <p className="text-white font-semibold">{holding.company}</p>
                  <p className="text-gray-400 text-sm">
                    {holding.shares} shares @ ${holding.avg_price?.toFixed(2) || '0.00'}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-white">${holding.value?.toFixed(2) || '0.00'}</p>
                  <p className={`text-sm ${holding.pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {holding.pnl >= 0 ? '+' : ''}${holding.pnl?.toFixed(2) || '0.00'} ({holding.pnl_percent?.toFixed(2) || '0.00'}%)
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
