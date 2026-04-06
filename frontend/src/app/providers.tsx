import type { ReactNode } from 'react'

import { AuthProvider } from './contexts/auth-provider'
import { CartProvider } from './contexts/cart-provider'
import { ToastProvider } from './contexts/toast-provider'
import { Toast } from '../components/common/Toast'

export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <ToastProvider>
      <AuthProvider>
        <CartProvider>
          {children}
          <Toast />
        </CartProvider>
      </AuthProvider>
    </ToastProvider>
  )
}
