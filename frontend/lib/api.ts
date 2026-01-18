import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          });
          
          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: (data: { email: string; password: string }) =>
    api.post('/auth/register', data),
  login: (data: { username: string; password: string }) => {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// User API
export const userApi = {
  getMe: () => api.get('/users/me'),
  updateMe: (data: any) => api.put('/users/me', data),
  updateProfile: (data: any) => api.put('/users/me/profile', data),
};

// Products API
export const productsApi = {
  getAll: () => api.get('/products'),
  getOne: (id: number) => api.get(`/products/${id}`),
  create: (data: any) => api.post('/products', data),
  update: (id: number, data: any) => api.put(`/products/${id}`, data),
  delete: (id: number) => api.delete(`/products/${id}`),
};

// Routines API
export const routinesApi = {
  getAll: () => api.get('/routines'),
  getOne: (id: number) => api.get(`/routines/${id}`),
  create: (data: any) => api.post('/routines', data),
  update: (id: number, data: any) => api.put(`/routines/${id}`, data),
  delete: (id: number) => api.delete(`/routines/${id}`),
};

// Routine Logs API
export const routineLogsApi = {
  getAll: (params?: any) => api.get('/routine-logs', { params }),
  getOne: (id: number) => api.get(`/routine-logs/${id}`),
  create: (data: any) => api.post('/routine-logs', data),
  update: (id: number, data: any) => api.put(`/routine-logs/${id}`, data),
  delete: (id: number) => api.delete(`/routine-logs/${id}`),
};

// Outcomes API
export const outcomesApi = {
  getAll: () => api.get('/outcomes'),
  getOne: (id: number) => api.get(`/outcomes/${id}`),
  create: (data: any) => api.post('/outcomes', data),
  update: (id: number, data: any) => api.put(`/outcomes/${id}`, data),
  delete: (id: number) => api.delete(`/outcomes/${id}`),
};

// Weather API
export const weatherApi = {
  getAll: (params?: any) => api.get('/weather', { params }),
  fetchAndSave: (date: string, location?: string) =>
    api.post('/weather/fetch', null, {
      params: { target_date: date, location },
    }),
};

// Dashboard API
export const dashboardApi = {
  getStats: () => api.get('/dashboard/stats'),
  getTrends: (days: number = 30) => api.get('/dashboard/trends', { params: { days } }),
  getInsights: () => api.get('/dashboard/insights'),
};
