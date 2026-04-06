export interface CartItem {
  id: number
  product: number
  product_name: string
  product_price: string
  quantity: number
}

export interface Cart {
  id: number
  items: CartItem[]
  created_at: string
  updated_at: string
}

export interface AddToCartPayload {
  product_id: number
  quantity: number
}

export interface UpdateCartItemPayload {
  quantity: number
}
