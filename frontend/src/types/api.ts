export interface ApiEnvelope<T> {
  success: boolean
  message: string
  data: T
  errors: Record<string, string[]> | null
}

export interface Product {
  id: number
  name: string
  slug: string
  price: string
  stock_quantity: number
  category_name?: string
}

export interface ShippingFee {
  zone: 'INSIDE_VALLEY' | 'OUTSIDE_VALLEY'
  fee: string
}

export interface AdminMetrics {
  total_orders: number
  pending_orders: number
  rejected_orders: number
  today_sales: string
  month_sales: string
}
