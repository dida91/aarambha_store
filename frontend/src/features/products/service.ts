import { apiClient, unwrapEnvelope } from '../../lib/api'
import { API_ENDPOINTS } from '../../lib/endpoints'
import type { ApiEnvelope, PaginatedResponse } from '../../types/api'
import type { Category, Product } from '../../types/product'

export interface ProductQuery {
  category?: string
  search?: string
  ordering?: string
  page?: string
}

export async function getCategories(): Promise<Category[]> {
  const response = await apiClient.get<ApiEnvelope<Category[]>>(API_ENDPOINTS.catalog.categories)
  return unwrapEnvelope(response.data)
}

export async function getProducts(query: ProductQuery): Promise<PaginatedResponse<Product>> {
  const response = await apiClient.get<ApiEnvelope<PaginatedResponse<Product>>>(
    API_ENDPOINTS.catalog.products,
    { params: query },
  )
  return unwrapEnvelope(response.data)
}

export async function getProductById(id: string): Promise<Product> {
  const response = await apiClient.get<ApiEnvelope<Product>>(API_ENDPOINTS.catalog.productDetail(id))
  return unwrapEnvelope(response.data)
}
