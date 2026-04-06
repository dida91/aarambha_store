import type { AdminMetrics, ApiEnvelope, Product, ShippingFee } from '../types/api'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

function unwrapListData<T>(data: unknown): T[] {
  if (Array.isArray(data)) {
    return data as T[]
  }
  if (
    data &&
    typeof data === 'object' &&
    'results' in data &&
    Array.isArray((data as { results?: unknown }).results)
  ) {
    return (data as { results: T[] }).results
  }
  return []
}

async function request<T>(path: string): Promise<ApiEnvelope<T>> {
  const response = await fetch(`${API_BASE}${path}`)
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }
  return (await response.json()) as ApiEnvelope<T>
}

export async function fetchProducts(): Promise<ApiEnvelope<Product[]>> {
  const response = await request<unknown>('/catalog/products/')
  return {
    ...response,
    data: unwrapListData<Product>(response.data),
  }
}

export async function fetchShippingFee(
  zone: 'INSIDE_VALLEY' | 'OUTSIDE_VALLEY',
): Promise<ApiEnvelope<ShippingFee>> {
  return request<ShippingFee>(`/shipping/configs/calculate/?zone=${zone}`)
}

export async function fetchAdminMetrics(token: string): Promise<ApiEnvelope<AdminMetrics>> {
  const response = await fetch(`${API_BASE}/common/admin-metrics/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }
  return (await response.json()) as ApiEnvelope<AdminMetrics>
}
