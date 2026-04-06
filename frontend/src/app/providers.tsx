import type { ReactNode } from 'react'

import { AuthProvider } from './contexts/AuthContext'
import { CartProvider } from './contexts/CartContext'
import { ToastProvider } from './contexts/ToastContext'
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
