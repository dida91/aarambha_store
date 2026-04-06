export type ShippingZone = 'INSIDE_VALLEY' | 'OUTSIDE_VALLEY'

export interface CheckoutPayload {
  zone: ShippingZone
  promo_code?: string
  address: string
  city: string
  contact_phone: string
}

export interface OrderItem {
  id: number
  product: number | null
  product_name: string
  product_slug: string
  unit_price: string
  quantity: number
  line_total: string
}

export interface OrderTimeline {
  id: number
  status: 'PENDING' | 'CONFIRMED' | 'REJECTED'
  actor: number | null
  actor_username: string
  note: string
  created_at: string
}

export interface Order {
  id: number
  status: 'PENDING' | 'CONFIRMED' | 'REJECTED'
  subtotal: string
  discount_total: string
  shipping_fee: string
  grand_total: string
  rejection_reason: string | null
  shipping_snapshot: {
    zone?: ShippingZone
    address?: string
    city?: string
    contact_phone?: string
  }
  items: OrderItem[]
  timeline: OrderTimeline[]
  created_at: string
  updated_at: string
}
