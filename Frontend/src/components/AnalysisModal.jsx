import React from 'react';
import StockChart from '../charts/StockChart';

export default function AnalysisModal({ stock, history, onClose }) {
  // Mock analysis data
  const analysis = {
    confidence: 0.75,
    recommendation: 'BUY',
    prediction: 'Price may increase in the next 2-3 weeks based on current trends.'
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-lg p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">
            📊 {stock.company} Analysis
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ✕
          </button>
        </div>

        <div className="space-y-6">
          {/* Chart */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-2">Price Chart</h3>
            {history && history.length > 0 ? (
              <StockChart data={history} symbol={stock.company} />
            ) : (
              <p className="text-gray-500">No chart data available</p>
            )}
          </div>

          {/* Analysis */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-green-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-green-800 mb-2">
                Confidence Level
              </h3>
              <div className="text-3xl font-bold text-green-600">
                {(analysis.confidence * 100).toFixed(0)}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${analysis.confidence * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-blue-800 mb-2">
                Recommendation
              </h3>
              <div className={`text-2xl font-bold ${
                analysis.recommendation === 'BUY' ? 'text-green-600' :
                analysis.recommendation === 'SELL' ? 'text-red-600' : 'text-yellow-600'
              }`}>
                {analysis.recommendation}
              </div>
            </div>
          </div>

          {/* Prediction */}
          <div className="bg-yellow-50 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-yellow-800 mb-2">
              📅 Price Prediction
            </h3>
            <p className="text-gray-700">
              {analysis.prediction}
            </p>
            <p className="text-sm text-gray-600 mt-2">
              Suggested timing: Buy now if confidence{" > "}70%, hold for 2-4 weeks.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}