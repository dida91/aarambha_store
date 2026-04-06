import axios from 'axios';

import type { ApiEnvelope } from './types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
});

export const setAccessToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
};

export async function getEnveloped<T>(url: string): Promise<T> {
  const { data } = await api.get<ApiEnvelope<T>>(url);
  return data.data;
}

export async function postEnveloped<T, P>(url: string, payload: P): Promise<T> {
  const { data } = await api.post<ApiEnvelope<T>>(url, payload);
  return data.data;
}

export default api;
