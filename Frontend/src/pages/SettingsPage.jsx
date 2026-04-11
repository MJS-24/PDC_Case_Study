import React, { useEffect, useState } from 'react';
import { balanceApi } from '../services/api';

export default function SettingsPage() {
  const [balance, setBalance] = useState(0);
  const [addAmount, setAddAmount] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBalance();
  }, []);

  const fetchBalance = async () => {
    try {
      const data = await balanceApi.getBalance();
      setBalance(data.balance);
      setError(null);
    } catch (err) {
      console.error('Error fetching balance:', err);
      setError('Failed to fetch balance');
    } finally {
      setLoading(false);
    }
  };

  const handleAddFunds = async () => {
    const amount = parseFloat(addAmount);
    if (isNaN(amount) || amount <= 0) {
      setError('Please enter a valid positive amount');
      return;
    }

    try {
      const result = await balanceApi.addBalance(amount);
      if (result.success) {
        setBalance(result.new_balance);
        setAddAmount('');
        setError(null);
      } else {
        setError(result.message);
      }
    } catch (err) {
      console.error('Error adding funds:', err);
      setError('Failed to add funds');
    }
  };

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Account Balance</h2>

        <div className="mb-4">
          <p className="text-lg">
            Current Balance: <span className="font-bold text-green-600">${balance.toFixed(2)}</span>
          </p>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Add Funds
          </label>
          <input
            type="number"
            value={addAmount}
            onChange={(e) => setAddAmount(e.target.value)}
            placeholder="Enter amount"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            min="0"
            step="0.01"
          />
        </div>

        <button
          onClick={handleAddFunds}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Add Funds
        </button>

        {error && (
          <div className="mt-4 text-red-600">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}