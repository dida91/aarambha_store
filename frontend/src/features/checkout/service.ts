import { apiClient, unwrapEnvelope } from '../../lib/api'
import { API_ENDPOINTS } from '../../lib/endpoints'
import type { ApiEnvelope } from '../../types/api'
import type { CheckoutPayload, Order, ShippingZone } from '../../types/order'

interface ShippingFeeResponse {
  zone: ShippingZone
  fee: string
}

export async function checkout(payload: CheckoutPayload): Promise<Order> {
  const response = await apiClient.post<ApiEnvelope<Order>>(API_ENDPOINTS.orders.checkout, payload)
  return unwrapEnvelope(response.data)
}

export async function calculateShipping(zone: ShippingZone): Promise<ShippingFeeResponse> {
  const response = await apiClient.get<ApiEnvelope<ShippingFeeResponse>>(API_ENDPOINTS.shipping.calculate, {
    params: { zone },
  })
  return unwrapEnvelope(response.data)
}

export async function validatePromo(code: string, subtotal: string): Promise<{
  code: string | null
  discount: string
  subtotal: string
  total_after_discount: string
}> {
  const response = await apiClient.post<
    ApiEnvelope<{ code: string | null; discount: string; subtotal: string; total_after_discount: string }>
  >(API_ENDPOINTS.promotions.validateCode, {
    code,
    subtotal,
  })
  return unwrapEnvelope(response.data)
}
