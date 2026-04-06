import type { AdminMetrics, ApiEnvelope, Product, ShippingFee } from '../types/api'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

async function request<T>(path: string): Promise<ApiEnvelope<T>> {
  const response = await fetch(`${API_BASE}${path}`)
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }
  return (await response.json()) as ApiEnvelope<T>
}

export async function fetchProducts(): Promise<ApiEnvelope<Product[]>> {
  return request<Product[]>('/catalog/products/')
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
