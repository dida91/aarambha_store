import { useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'

import { addCartItem, getMyCart, removeCartItem, updateCartItem } from '../../features/cart/service'
import { AuthContext } from './auth-context'
import { CartContext, type CartContextValue } from './cart-context'

export function CartProvider({ children }: { children: ReactNode }) {
  const auth = useContext(AuthContext)
  const [cart, setCart] = useState<CartContextValue['cart']>(null)
  const [isLoading, setIsLoading] = useState(false)

  const refreshCart = useCallback(async () => {
    if (!auth?.isAuthenticated) {
      setCart(null)
      return
    }
    setIsLoading(true)
    try {
      const data = await getMyCart()
      setCart(data)
    } finally {
      setIsLoading(false)
    }
  }, [auth?.isAuthenticated])

  useEffect(() => {
    void refreshCart()
  }, [refreshCart])

  const addItem = useCallback(async (productId: number, quantity: number) => {
    const updated = await addCartItem({ product_id: productId, quantity })
    setCart(updated)
  }, [])

  const updateItemQuantity = useCallback(async (itemId: number, quantity: number) => {
    const updated = await updateCartItem(itemId, { quantity })
    setCart(updated)
  }, [])

  const removeItemById = useCallback(async (itemId: number) => {
    const updated = await removeCartItem(itemId)
    setCart(updated)
  }, [])

  const subtotal = useMemo(
    () => (cart?.items ?? []).reduce((sum, item) => sum + Number(item.product_price) * item.quantity, 0),
    [cart],
  )

  const value = useMemo<CartContextValue>(
    () => ({
      cart,
      isLoading,
      subtotal,
      total: subtotal,
      refreshCart,
      addItem,
      updateItem: updateItemQuantity,
      removeItem: removeItemById,
    }),
    [cart, isLoading, subtotal, refreshCart, addItem, updateItemQuantity, removeItemById],
  )

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}
