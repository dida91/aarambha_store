import { useState } from 'react'

import { fetchAdminMetrics } from '../services/api'
import type { AdminMetrics } from '../types/api'

export function AdminSummary() {
  const [metrics, setMetrics] = useState<AdminMetrics | null>(null)
  const [error, setError] = useState('')

  const handleLoad = async () => {
    setError('')
    try {
      const token = localStorage.getItem('aarambha_admin_token') ?? ''
      const result = await fetchAdminMetrics(token)
      setMetrics(result.data)
    } catch {
      setError('Unable to load admin metrics.')
    }
  }

  return (
    <section aria-label="Admin metrics">
      <h2>Admin Dashboard Metrics</h2>
      <button type="button" onClick={handleLoad}>
        Load Metrics
      </button>
      {metrics ? (
        <ul>
          <li>Total Orders: {metrics.total_orders}</li>
          <li>Pending Orders: {metrics.pending_orders}</li>
          <li>Rejected Orders: {metrics.rejected_orders}</li>
          <li>Today Sales: NPR {metrics.today_sales}</li>
          <li>Month Sales: NPR {metrics.month_sales}</li>
        </ul>
      ) : null}
      {error ? <p role="alert">{error}</p> : null}
    </section>
  )
}
