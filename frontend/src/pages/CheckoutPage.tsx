import { FormEvent, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { ErrorState } from '../components/common/ErrorState'
import { useCart } from '../hooks/useCart'
import { useToast } from '../hooks/useToast'
import { checkout, validatePromo } from '../features/checkout/service'
import { currency } from '../lib/utils'
import type { ShippingZone } from '../types/order'

interface CheckoutForm {
  zone: ShippingZone
  address: string
  city: string
  contact_phone: string
  promo_code: string
}

export function CheckoutPage() {
  const navigate = useNavigate()
  const { cart, subtotal, refreshCart } = useCart()
  const { showToast } = useToast()

  const [form, setForm] = useState<CheckoutForm>({
    zone: 'INSIDE_VALLEY',
    address: '',
    city: '',
    contact_phone: '',
    promo_code: '',
  })
  const [promoDiscount, setPromoDiscount] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const total = useMemo(() => Math.max(0, subtotal - promoDiscount), [subtotal, promoDiscount])

  const validateForm = (): string | null => {
    if (!form.address.trim()) {
      return 'Address is required.'
    }
    if (!form.city.trim()) {
      return 'City is required.'
    }
    if (!form.contact_phone.trim()) {
      return 'Contact phone is required.'
    }
    if (form.contact_phone.trim().length < 7) {
      return 'Contact phone looks invalid.'
    }
    return null
  }

  const applyPromo = async () => {
    if (!form.promo_code.trim()) {
      setPromoDiscount(0)
      return
    }
    try {
      const result = await validatePromo(form.promo_code.trim(), subtotal.toFixed(2))
      setPromoDiscount(Number(result.discount))
      showToast('Promo applied.', 'success')
    } catch (err) {
      setPromoDiscount(0)
      showToast((err as { message?: string }).message ?? 'Promo validation failed.', 'error')
    }
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    const validationError = validateForm()
    if (validationError) {
      setError(validationError)
      return
    }

    setLoading(true)
    setError('')
    try {
      const order = await checkout({
        zone: form.zone,
        address: form.address.trim(),
        city: form.city.trim(),
        contact_phone: form.contact_phone.trim(),
        promo_code: form.promo_code.trim() || undefined,
      })
      await refreshCart()
      showToast(`Order #${order.id} created successfully.`, 'success')
      navigate('/profile')
    } catch (err) {
      setError((err as { message?: string }).message ?? 'Checkout failed.')
    } finally {
      setLoading(false)
    }
  }

  if (!cart || cart.items.length === 0) {
    return <ErrorState message="Your cart is empty. Add products before checkout." />
  }

  return (
    <section className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <form onSubmit={submit} className="space-y-4 rounded-xl border border-slate-200 bg-white p-6 shadow-soft">
        <h1 className="text-xl font-semibold">Checkout</h1>
        {error ? <ErrorState message={error} /> : null}

        <label className="block space-y-1 text-sm">
          <span>Shipping zone</span>
          <select
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
            value={form.zone}
            onChange={(event) => setForm((prev) => ({ ...prev, zone: event.target.value as ShippingZone }))}
          >
            <option value="INSIDE_VALLEY">Inside Valley</option>
            <option value="OUTSIDE_VALLEY">Outside Valley</option>
          </select>
        </label>

        <label className="block space-y-1 text-sm">
          <span>Address</span>
          <input
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
            value={form.address}
            onChange={(event) => setForm((prev) => ({ ...prev, address: event.target.value }))}
          />
        </label>

        <label className="block space-y-1 text-sm">
          <span>City</span>
          <input
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
            value={form.city}
            onChange={(event) => setForm((prev) => ({ ...prev, city: event.target.value }))}
          />
        </label>

        <label className="block space-y-1 text-sm">
          <span>Contact phone</span>
          <input
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
            value={form.contact_phone}
            onChange={(event) => setForm((prev) => ({ ...prev, contact_phone: event.target.value }))}
          />
        </label>

        <div className="grid gap-2 sm:grid-cols-[1fr_auto]">
          <input
            placeholder="Promo code"
            className="rounded-lg border border-slate-300 px-3 py-2"
            value={form.promo_code}
            onChange={(event) => setForm((prev) => ({ ...prev, promo_code: event.target.value }))}
          />
          <button
            type="button"
            onClick={() => void applyPromo()}
            className="rounded-lg border border-slate-300 px-4 py-2 text-sm hover:bg-slate-100"
          >
            Apply
          </button>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Processing...' : 'Place Order'}
        </button>
      </form>

      <aside className="h-fit rounded-xl border border-slate-200 bg-white p-4 shadow-soft">
        <h2 className="text-lg font-semibold">Summary</h2>
        <div className="mt-3 space-y-2 text-sm text-slate-600">
          <div className="flex justify-between">
            <span>Subtotal</span>
            <span>{currency(subtotal)}</span>
          </div>
          <div className="flex justify-between">
            <span>Discount</span>
            <span>- {currency(promoDiscount)}</span>
          </div>
          <div className="flex justify-between border-t border-slate-200 pt-2 font-semibold text-slate-900">
            <span>Total</span>
            <span>{currency(total)}</span>
          </div>
        </div>
      </aside>
    </section>
  )
}
