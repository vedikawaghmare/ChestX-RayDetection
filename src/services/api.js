import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Fix CORS issues by ensuring proper origin
if (window.location.port === '5001') {
  window.location.href = 'http://localhost:3000';
}

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    
    if (error.response?.status === 413) {
      throw new Error('File too large. Please upload a smaller image.');
    } else if (error.response?.status === 415) {
      throw new Error('Unsupported file type. Please upload a valid image.');
    } else if (error.response?.status >= 500) {
      throw new Error('Server error. Please try again later.');
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. Please try again.');
    }
    
    throw error;
  }
);

/**
 * Analyze chest X-ray image using Gemini AI
 * @param {File} imageFile - The image file to analyze
 * @returns {Promise<Object>} Analysis results
 */
export const analyzeImage = async (imageFile) => {
  try {
    // Validate file
    if (!imageFile) {
      throw new Error('No image file provided');
    }

    // Check file size (max 10MB)
    const maxSize = 10 * 1024 * 1024;
    if (imageFile.size > maxSize) {
      throw new Error('File size too large. Maximum size is 10MB.');
    }

    // Check file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(imageFile.type)) {
      throw new Error('Invalid file type. Please upload JPG, PNG, or WEBP images only.');
    }

    // Create form data
    const formData = new FormData();
    formData.append('image', imageFile);

    // Make API request
    const response = await api.post('/api/analyze', formData);

    // Validate response
    if (!response.data) {
      throw new Error('Invalid response from server');
    }

    return response.data;
  } catch (error) {
    console.error('Image analysis error:', error);
    
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    
    throw error;
  }
};

/**
 * Check server health
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Health check error:', error);
    throw new Error('Unable to connect to server');
  }
};

/**
 * Get supported file types
 * @returns {Promise<Object>} Supported file types
 */
export const getSupportedTypes = async () => {
  try {
    const response = await api.get('/api/supported-types');
    return response.data;
  } catch (error) {
    console.error('Get supported types error:', error);
    return {
      types: ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
      extensions: ['.jpg', '.jpeg', '.png', '.webp'],
      maxSize: 10 * 1024 * 1024
    };
  }
};

export default api;