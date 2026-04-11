import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============ HEALTH CHECK ============
export const healthCheck = async () => {
  try {
    // Check root endpoint for basic connectivity
    const response = await axios.get('http://localhost:8001/');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

// ============ DASHBOARD ============
export const dashboardApi = {
  getSummary: async () => {
    try {
      const response = await apiClient.get('/dashboard');
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      throw error;
    }
  },
};

// ============ INVENTORY ============
export const inventoryApi = {
  getLowStock: async () => {
    try {
      const response = await apiClient.get('/inventory/low-stock');
      return response.data;
    } catch (error) {
      console.error('Error fetching low stock:', error);
      throw error;
    }
  },

  getBranchInventory: async (branchId) => {
    try {
      const response = await apiClient.get(`/inventory/branch/${branchId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching inventory for ${branchId}:`, error);
      throw error;
    }
  },

  getValuation: async () => {
    try {
      const response = await apiClient.get('/inventory/valuation');
      return response.data;
    } catch (error) {
      console.error('Error fetching inventory valuation:', error);
      throw error;
    }
  },
};

// ============ SALES ============
export const salesApi = {
  getByCategory: async () => {
    try {
      const response = await apiClient.get('/sales/by-category');
      return response.data;
    } catch (error) {
      console.error('Error fetching sales by category:', error);
      throw error;
    }
  },

  getByBranch: async () => {
    try {
      const response = await apiClient.get('/sales/by-branch');
      return response.data;
    } catch (error) {
      console.error('Error fetching branch performance:', error);
      throw error;
    }
  },

  getRecent: async (days = 7) => {
    try {
      const response = await apiClient.get('/sales/recent', { params: { days } });
      return response.data;
    } catch (error) {
      console.error('Error fetching recent sales:', error);
      throw error;
    }
  },
};

// ============ LOGISTICS ============
export const logisticsApi = {
  getDeliverySummary: async () => {
    try {
      const response = await apiClient.get('/deliveries/summary');
      return response.data;
    } catch (error) {
      console.error('Error fetching delivery summary:', error);
      throw error;
    }
  },

  getDelayedDeliveries: async () => {
    try {
      const response = await apiClient.get('/deliveries/delayed');
      return response.data;
    } catch (error) {
      console.error('Error fetching delayed deliveries:', error);
      throw error;
    }
  },

  getFleetEfficiency: async () => {
    try {
      const response = await apiClient.get('/fleet/efficiency');
      return response.data;
    } catch (error) {
      console.error('Error fetching fleet efficiency:', error);
      throw error;
    }
  },
};

// ============ STOCK API (Mock for compatibility) ============
export const stockApi = {
  getAllStocks: async () => {
    try {
      // Mock stock data
      return [
        { symbol: 'AAPL', name: 'Apple Inc.', price: 150.25, change: 2.5 },
        { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 2800.00, change: -1.2 },
        { symbol: 'MSFT', name: 'Microsoft Corp.', price: 305.50, change: 0.8 },
        { symbol: 'TSLA', name: 'Tesla Inc.', price: 220.75, change: 5.3 },
        { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 3200.00, change: -0.5 }
      ];
    } catch (error) {
      console.error('Error fetching stocks:', error);
      throw error;
    }
  },

  getPortfolio: async (userId) => {
    try {
      const response = await apiClient.get('/portfolio', {
        params: { user_id: userId }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio:', error);
      throw error;
    }
  },

  getStockAnalysis: async (symbol) => {
    try {
      // Mock analysis data
      const analyses = {
        'AAPL': { current_price: 150.25, recommendation: 'BUY', confidence: 0.85 },
        'GOOGL': { current_price: 2800.00, recommendation: 'HOLD', confidence: 0.65 },
        'MSFT': { current_price: 305.50, recommendation: 'BUY', confidence: 0.78 },
        'TSLA': { current_price: 220.75, recommendation: 'SELL', confidence: 0.72 },
        'AMZN': { current_price: 3200.00, recommendation: 'BUY', confidence: 0.81 }
      };
      return analyses[symbol] || { current_price: 100.00, recommendation: 'HOLD', confidence: 0.5 };
    } catch (error) {
      console.error('Error fetching stock analysis:', error);
      throw error;
    }
  },

  getStockHistory: async (symbol) => {
    try {
      // Mock history data with close/open format for chart
      return {
        history: [
          { date: '2024-01-01', close: 145.00, open: 144.50 },
          { date: '2024-01-02', close: 147.50, open: 145.20 },
          { date: '2024-01-03', close: 150.25, open: 147.80 }
        ]
      };
    } catch (error) {
      console.error('Error fetching stock history:', error);
      throw error;
    }
  }
};

// ============ PORTFOLIO API (Mock for compatibility) ============
export const portfolioApi = {
  getPortfolio: async (userId) => {
    try {
      const response = await apiClient.get('/portfolio', {
        params: { user_id: userId }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio:', error);
      throw error;
    }
  },

  getTransactions: async (userId) => {
    try {
      // Mock transactions data
      return [
        { id: 1, symbol: 'AAPL', type: 'BUY', shares: 10, price: 145.00, date: '2024-01-01' },
        { id: 2, symbol: 'GOOGL', type: 'SELL', shares: 2, price: 2750.00, date: '2024-01-02' }
      ];
    } catch (error) {
      console.error('Error fetching transactions:', error);
      throw error;
    }
  },

  buyStock: async (userId, symbol, quantity) => {
    try {
      // Mock successful buy
      return { success: true, message: 'Stock purchased successfully' };
    } catch (error) {
      console.error('Error buying stock:', error);
      throw error;
    }
  },

  sellStock: async (userId, symbol, quantity) => {
    try {
      // Mock successful sell
      return { success: true, message: 'Stock sold successfully' };
    } catch (error) {
      console.error('Error selling stock:', error);
      throw error;
    }
  }
};
