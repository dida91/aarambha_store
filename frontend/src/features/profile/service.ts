import { apiClient, unwrapEnvelope } from '../../lib/api'
import { API_ENDPOINTS } from '../../lib/endpoints'
import type { ApiEnvelope, PaginatedResponse } from '../../types/api'
import type { Order } from '../../types/order'

export async function getMyOrders(): Promise<PaginatedResponse<Order>> {
  const response = await apiClient.get<ApiEnvelope<PaginatedResponse<Order>>>(API_ENDPOINTS.orders.myOrders)
  return unwrapEnvelope(response.data)
}
