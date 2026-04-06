import type { AdminMetrics, ApiEnvelope, Product, ShippingFee } from '../types/api'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

function isProduct(item: unknown): item is Product {
  return (
    !!item &&
    typeof item === 'object' &&
    typeof (item as { id?: unknown }).id === 'number' &&
    typeof (item as { name?: unknown }).name === 'string' &&
    typeof (item as { slug?: unknown }).slug === 'string' &&
    typeof (item as { price?: unknown }).price === 'string' &&
    typeof (item as { stock_quantity?: unknown }).stock_quantity === 'number'
  )
}

function unwrapProductsData(data: unknown): Product[] {
  if (Array.isArray(data)) {
    return data.filter(isProduct)
  }
  if (
    data &&
    typeof data === 'object' &&
    'results' in data &&
    Array.isArray((data as { results?: unknown }).results)
  ) {
    return (data as { results: unknown[] }).results.filter(isProduct)
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
    data: unwrapProductsData(response.data),
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
