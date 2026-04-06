import { createContext } from 'react'

import type { Cart } from '../../types/cart'

export interface CartContextValue {
  cart: Cart | null
  isLoading: boolean
  subtotal: number
  total: number
  refreshCart: () => Promise<void>
  addItem: (productId: number, quantity: number) => Promise<void>
  updateItem: (itemId: number, quantity: number) => Promise<void>
  removeItem: (itemId: number) => Promise<void>
}

export const CartContext = createContext<CartContextValue | null>(null)
