import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(true);
  const [highContrast, setHighContrast] = useState(false);
  const [largeText, setLargeText] = useState(false);

  // Axios interceptor for auth
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get(`${API}/auth/me`);
      setUser(response.data);
      setLanguage(response.data.preferred_language || 'en');
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch user', error);
      // Only logout if unauthorized (401), not on network errors
      if (error.response?.status === 401) {
        logout();
      }
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, { email, password });
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      setLanguage(userData.preferred_language || 'en');
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const signup = async (name, email, password, preferred_language = 'en') => {
    try {
      const response = await axios.post(`${API}/auth/signup`, {
        name,
        email,
        password,
        preferred_language
      });
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      setLanguage(userData.preferred_language || 'en');
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Signup failed' };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    user,
    token,
    language,
    setLanguage,
    login,
    signup,
    logout,
    loading,
    highContrast,
    setHighContrast,
    largeText,
    setLargeText,
    API
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
