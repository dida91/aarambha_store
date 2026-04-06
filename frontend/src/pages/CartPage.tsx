import { Link } from 'react-router-dom'

import { EmptyState } from '../components/common/EmptyState'
import { Loader } from '../components/common/Loader'
import { QuantitySelector } from '../components/common/QuantitySelector'
import { useCart } from '../hooks/useCart'
import { useToast } from '../hooks/useToast'
import { currency } from '../lib/utils'

export function CartPage() {
  const { cart, isLoading, subtotal, updateItem, removeItem } = useCart()
  const { showToast } = useToast()

  const onUpdate = async (itemId: number, quantity: number) => {
    try {
      await updateItem(itemId, quantity)
    } catch (err) {
      showToast((err as { message?: string }).message ?? 'Failed to update quantity.', 'error')
    }
  }

  const onRemove = async (itemId: number) => {
    try {
      await removeItem(itemId)
      showToast('Item removed from cart.', 'info')
    } catch (err) {
      showToast((err as { message?: string }).message ?? 'Failed to remove item.', 'error')
    }
  }

  if (isLoading) {
    return <Loader label="Loading cart..." />
  }

  if (!cart || cart.items.length === 0) {
    return <EmptyState title="Your cart is empty" description="Add products to proceed with checkout." />
  }

  return (
    <section className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <div className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-soft">
        {cart.items.map((item) => (
          <div key={item.id} className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 py-3 last:border-b-0">
            <div>
              <p className="font-medium text-slate-900">{item.product_name}</p>
              <p className="text-sm text-slate-500">{currency(item.product_price)}</p>
            </div>
            <div className="flex items-center gap-2">
              <QuantitySelector value={item.quantity} onChange={(value) => void onUpdate(item.id, value)} />
              <button
                type="button"
                onClick={() => void onRemove(item.id)}
                className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-100"
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      <aside className="h-fit rounded-xl border border-slate-200 bg-white p-4 shadow-soft">
        <h2 className="text-lg font-semibold">Order summary</h2>
        <div className="mt-3 flex justify-between text-sm text-slate-600">
          <span>Subtotal</span>
          <span>{currency(subtotal)}</span>
        </div>
        <div className="mt-4 border-t border-slate-200 pt-3">
          <Link
            to="/checkout"
            className="inline-flex w-full justify-center rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Proceed to Checkout
          </Link>
        </div>
      </aside>
    </section>
  )
}
