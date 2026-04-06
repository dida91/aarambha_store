import { createContext } from 'react'

import type { ToastItem } from '../../types/common'

export interface ToastContextValue {
  toasts: ToastItem[]
  showToast: (message: string, type?: ToastItem['type']) => void
  removeToast: (id: number) => void
}

export const ToastContext = createContext<ToastContextValue | null>(null)
