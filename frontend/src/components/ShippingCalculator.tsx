import { useState } from 'react'

import { fetchShippingFee } from '../services/api'

export function ShippingCalculator() {
  const [zone, setZone] = useState<'INSIDE_VALLEY' | 'OUTSIDE_VALLEY'>('INSIDE_VALLEY')
  const [fee, setFee] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleCalculate = async () => {
    setLoading(true)
    setError('')
    try {
      const result = await fetchShippingFee(zone)
      setFee(result.data.fee)
    } catch {
      setError('Unable to calculate shipping right now.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section aria-label="Shipping calculator">
      <h2>Shipping Fee Calculator</h2>
      <label htmlFor="zone">Delivery Zone</label>
      <select
        id="zone"
        value={zone}
        onChange={(event) => setZone(event.target.value as 'INSIDE_VALLEY' | 'OUTSIDE_VALLEY')}
      >
        <option value="INSIDE_VALLEY">Inside Valley</option>
        <option value="OUTSIDE_VALLEY">Outside Valley</option>
      </select>
      <button type="button" onClick={handleCalculate} disabled={loading}>
        {loading ? 'Calculating...' : 'Calculate'}
      </button>
      {fee ? <p>Estimated Shipping Fee: NPR {fee}</p> : null}
      {error ? <p role="alert">{error}</p> : null}
    </section>
  )
}
