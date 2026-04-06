import { useEffect, useState } from 'react'

import { EmptyState } from '../components/common/EmptyState'
import { ErrorState } from '../components/common/ErrorState'
import { Loader } from '../components/common/Loader'
import { getMyOrders } from '../features/profile/service'
import { useAuth } from '../hooks/useAuth'
import { currency } from '../lib/utils'
import type { Order } from '../types/order'

export function ProfilePage() {
  const { user } = useAuth()
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const data = await getMyOrders()
        setOrders(data.results)
      } catch (err) {
        setError((err as { message?: string }).message ?? 'Failed to load your orders.')
      } finally {
        setLoading(false)
      }
    }

    void load()
  }, [])

  return (
    <section className="space-y-6">
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-soft">
        <h1 className="text-xl font-semibold">My Profile</h1>
        <div className="mt-3 grid gap-2 text-sm text-slate-700 sm:grid-cols-2">
          <p><strong>Username:</strong> {user?.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Name:</strong> {user?.first_name} {user?.last_name}</p>
          <p><strong>Phone:</strong> {user?.phone || 'N/A'}</p>
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-soft">
        <h2 className="text-lg font-semibold">My Orders</h2>
        {loading ? <Loader label="Loading orders..." /> : null}
        {error ? <ErrorState message={error} /> : null}
        {!loading && !error && orders.length === 0 ? (
          <EmptyState title="No orders yet" description="Your completed checkouts will appear here." />
        ) : null}
        {!loading && !error && orders.length > 0 ? (
          <div className="mt-4 space-y-3">
            {orders.map((order) => (
              <article key={order.id} className="rounded-lg border border-slate-200 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h3 className="font-medium">Order #{order.id}</h3>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium">{order.status}</span>
                </div>
                <p className="mt-2 text-sm text-slate-600">Total: {currency(order.grand_total)}</p>
                <p className="text-sm text-slate-500">Placed: {new Date(order.created_at).toLocaleString()}</p>
              </article>
            ))}
          </div>
        ) : null}
      </div>
    </section>
  )
}
