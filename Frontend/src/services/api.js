import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

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

export const stockApi = {
  getAllStocks: async () => {
    try {
      const response = await apiClient.get('/stocks');
      return response.data;
    } catch (error) {
      console.error('Error fetching stocks:', error);
      throw error;
    }
  },

  getStockHistory: async (company) => {
    try {
      const response = await apiClient.get(`/stocks/${company}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching history for ${company}:`, error);
      throw error;
    }
  },
};

export const portfolioApi = {
  getPortfolio: async () => {
    try {
      const response = await apiClient.get('/portfolio');
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio:', error);
      throw error;
    }
  },

  getTransactions: async () => {
    try {
      const response = await apiClient.get('/transactions');
      return response.data;
    } catch (error) {
      console.error('Error fetching transactions:', error);
      throw error;
    }
  },

  buyStock: async (company, quantity) => {
    try {
      const response = await apiClient.post('/buy', {
        company,
        quantity,
      });
      return response.data;
    } catch (error) {
      console.error(`Error buying ${company}:`, error);
      throw error;
    }
  },

  sellStock: async (company, quantity) => {
    try {
      const response = await apiClient.post('/sell', {
        company,
        quantity,
      });
      return response.data;
    } catch (error) {
      console.error(`Error selling ${company}:`, error);
      throw error;
    }
  },
};

export const balanceApi = {
  getBalance: async () => {
    try {
      const response = await apiClient.get('/balance');
      return response.data;
    } catch (error) {
      console.error('Error fetching balance:', error);
      throw error;
    }
  },

  addBalance: async (amount) => {
    try {
      const response = await apiClient.post('/balance/add', {
        amount,
      });
      return response.data;
    } catch (error) {
      console.error('Error adding balance:', error);
      throw error;
    }
  },
};
