import { apiClient, unwrapEnvelope } from '../../lib/api'
import { API_ENDPOINTS } from '../../lib/endpoints'
import type { ApiEnvelope } from '../../types/api'
import type { AddToCartPayload, Cart, UpdateCartItemPayload } from '../../types/cart'

export async function getMyCart(): Promise<Cart> {
  const response = await apiClient.get<ApiEnvelope<Cart>>(API_ENDPOINTS.cart.me)
  return unwrapEnvelope(response.data)
}

export async function addCartItem(payload: AddToCartPayload): Promise<Cart> {
  const response = await apiClient.post<ApiEnvelope<Cart>>(API_ENDPOINTS.cart.items, payload)
  return unwrapEnvelope(response.data)
}

export async function updateCartItem(itemId: number, payload: UpdateCartItemPayload): Promise<Cart> {
  const response = await apiClient.patch<ApiEnvelope<Cart>>(API_ENDPOINTS.cart.itemById(itemId), payload)
  return unwrapEnvelope(response.data)
}

export async function removeCartItem(itemId: number): Promise<Cart> {
  const response = await apiClient.delete<ApiEnvelope<Cart>>(API_ENDPOINTS.cart.itemById(itemId))
  return unwrapEnvelope(response.data)
}
