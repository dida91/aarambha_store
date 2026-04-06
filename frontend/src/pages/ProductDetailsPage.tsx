import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '../components/common/ErrorState'
import { Loader } from '../components/common/Loader'
import { QuantitySelector } from '../components/common/QuantitySelector'
import { getProductById } from '../features/products/service'
import { useCart } from '../hooks/useCart'
import { useToast } from '../hooks/useToast'
import { currency, getImageUrl } from '../lib/utils'
import type { Product } from '../types/product'

export function ProductDetailsPage() {
  const { id = '' } = useParams()
  const navigate = useNavigate()
  const { addItem } = useCart()
  const { showToast } = useToast()
  const [product, setProduct] = useState<Product | null>(null)
  const [quantity, setQuantity] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const data = await getProductById(id)
        setProduct(data)
      } catch (err) {
        setError((err as { message?: string }).message ?? 'Unable to fetch product.')
      } finally {
        setLoading(false)
      }
    }

    void load()
  }, [id])

  const onAddToCart = async () => {
    if (!product) {
      return
    }
    try {
      await addItem(product.id, quantity)
      showToast('Item added to cart.', 'success')
      navigate('/cart')
    } catch (err) {
      showToast((err as { message?: string }).message ?? 'Failed to add item.', 'error')
    }
  }

  if (loading) {
    return <Loader label="Loading product..." />
  }

  if (error || !product) {
    return <ErrorState message={error || 'Product not found.'} />
  }

  const primary = product.images.find((item) => item.is_primary) ?? product.images[0]
  const image = getImageUrl(primary?.image)

  return (
    <section className="grid gap-6 rounded-xl border border-slate-200 bg-white p-6 shadow-soft md:grid-cols-2">
      <div>
        {image ? (
          <img src={image} alt={primary?.alt_text || product.name} className="h-full max-h-[420px] w-full rounded-xl object-cover" />
        ) : (
          <div className="flex h-80 items-center justify-center rounded-xl bg-slate-100 text-slate-500">No image</div>
        )}
      </div>
      <div className="space-y-4">
        <p className="text-sm text-slate-500">{product.category_name}</p>
        <h1 className="text-2xl font-bold">{product.name}</h1>
        <p className="text-xl font-semibold text-brand-700">{currency(product.price)}</p>
        <p className="text-sm text-slate-600">{product.description || 'No description available.'}</p>
        <p className="text-sm text-slate-500">Stock available: {product.stock_quantity}</p>
        <div className="space-y-3 pt-2">
          <QuantitySelector value={quantity} max={Math.max(1, product.stock_quantity)} onChange={setQuantity} />
          <button
            type="button"
            onClick={onAddToCart}
            className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
            disabled={product.stock_quantity === 0}
          >
            Add to Cart
          </button>
        </div>
      </div>
    </section>
  )
}
