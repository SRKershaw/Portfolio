// src/hooks/useApi.js - Reusable API hook with axios for backend calls

import { useState, useCallback } from 'react';
import axios from 'axios';

export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const api = axios.create({
    baseURL: '/api',  // Proxy to backend (dev) or same domain (prod)
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const sendRequest = useCallback(async (method, url, data = null) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api({
        method,
        url,
        data,
      });
      return res.data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { sendRequest, loading, error };
}