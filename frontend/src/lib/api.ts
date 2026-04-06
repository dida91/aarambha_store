import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'

import { API_ENDPOINTS } from './endpoints'
import type { ApiEnvelope, ApiErrorShape } from '../types/api'
import type { TokenPair } from '../types/auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'
const WITH_CREDENTIALS = (import.meta.env.VITE_API_WITH_CREDENTIALS ?? 'false') === 'true'

const ACCESS_KEY = 'aarambha_access_token'
const REFRESH_KEY = 'aarambha_refresh_token'

let refreshPromise: Promise<string | null> | null = null

function toErrorMap(value: unknown): Record<string, string[]> {
  if (value === null || value === undefined) {
    return {}
  }
  if (typeof value === 'string') {
    return { detail: [value] }
  }
  if (Array.isArray(value)) {
    return { detail: value.map(String) }
  }
  if (typeof value !== 'object') {
    return { detail: ['Unexpected error'] }
  }

  const result: Record<string, string[]> = {}
  for (const [key, raw] of Object.entries(value as Record<string, unknown>)) {
    if (Array.isArray(raw)) {
      result[key] = raw.map(String)
    } else if (typeof raw === 'string') {
      result[key] = [raw]
    } else {
      result[key] = [String(raw)]
    }
  }
  return result
}

export function normalizeApiError(error: unknown): ApiErrorShape {
  const fallback: ApiErrorShape = {
    message: 'Something went wrong. Please try again.',
    status: 500,
    errors: {},
  }

  if (!axios.isAxiosError(error)) {
    return fallback
  }

  const status = error.response?.status ?? 500
  const payload = error.response?.data as ApiEnvelope<unknown> | undefined
  const errors = toErrorMap(payload?.errors)
  const detail = errors.detail?.[0]

  return {
    status,
    message: payload?.message || detail || error.message || fallback.message,
    errors,
  }
}

export function getStoredTokens(): TokenPair | null {
  const access = localStorage.getItem(ACCESS_KEY)
  const refresh = localStorage.getItem(REFRESH_KEY)
  if (!access || !refresh) {
    return null
  }
  return { access, refresh }
}

export function setStoredTokens(tokens: TokenPair): void {
  localStorage.setItem(ACCESS_KEY, tokens.access)
  localStorage.setItem(REFRESH_KEY, tokens.refresh)
}

export function clearStoredTokens(): void {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
}

async function refreshAccessToken(): Promise<string | null> {
  if (refreshPromise) {
    return refreshPromise
  }

  const tokens = getStoredTokens()
  if (!tokens?.refresh) {
    return null
  }

  refreshPromise = axios
    .post<ApiEnvelope<{ access: string }>>(
      `${API_BASE_URL}${API_ENDPOINTS.accounts.refresh}`,
      { refresh: tokens.refresh },
      { withCredentials: WITH_CREDENTIALS },
    )
    .then((res) => {
      const newAccess = res.data.data.access
      setStoredTokens({ access: newAccess, refresh: tokens.refresh })
      return newAccess
    })
    .catch(() => {
      clearStoredTokens()
      return null
    })
    .finally(() => {
      refreshPromise = null
    })

  return refreshPromise
}

function attachAuthHeader(config: InternalAxiosRequestConfig): InternalAxiosRequestConfig {
  const access = localStorage.getItem(ACCESS_KEY)
  if (access) {
    config.headers.Authorization = `Bearer ${access}`
  }
  return config
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: WITH_CREDENTIALS,
})

apiClient.interceptors.request.use(attachAuthHeader)

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiEnvelope<unknown>>) => {
    const original = error.config as (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined

    if (error.response?.status === 401 && original && !original._retry) {
      original._retry = true
      const nextAccess = await refreshAccessToken()
      if (nextAccess) {
        original.headers.Authorization = `Bearer ${nextAccess}`
        return apiClient(original)
      }
    }

    return Promise.reject(normalizeApiError(error))
  },
)

export function unwrapEnvelope<T>(envelope: ApiEnvelope<T>): T {
  return envelope.data
}
