import { useEffect, useState } from 'react'

import './App.css'
import { AdminSummary } from './components/AdminSummary'
import { ProductList } from './components/ProductList'
import { ShippingCalculator } from './components/ShippingCalculator'
import { fetchProducts } from './services/api'
import type { Product } from './types/api'

function App() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const result = await fetchProducts()
        setProducts(result.data)
      } catch {
        setError('Unable to load products from Aarambha Store API.')
      } finally {
        setLoading(false)
      }
    }
    void loadProducts()
  }, [])

  return (
    <main className="app-shell">
      <header>
        <h1>Aarambha Store</h1>
        <p>Single-seller eCommerce platform for Nepal</p>
      </header>

      {loading ? <p>Loading products...</p> : null}
      {error ? <p role="alert">{error}</p> : null}
      {!loading && !error ? <ProductList products={products} /> : null}

      <ShippingCalculator />
      <AdminSummary />
    </main>
  )
}

export default App
