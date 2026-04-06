import { Link } from 'react-router-dom'

import { currency, getImageUrl } from '../../lib/utils'
import type { Product } from '../../types/product'

export function ProductCard({ product }: { product: Product }) {
  const primary = product.images.find((item) => item.is_primary) ?? product.images[0]
  const image = getImageUrl(primary?.image)

  return (
    <article className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-soft">
      <Link to={`/products/${product.id}`} className="block">
        {image ? (
          <img src={image} alt={primary?.alt_text || product.name} className="h-52 w-full object-cover" />
        ) : (
          <div className="flex h-52 items-center justify-center bg-slate-100 text-sm text-slate-500">No image</div>
        )}
      </Link>
      <div className="space-y-2 p-4">
        <p className="text-xs uppercase text-slate-500">{product.category_name}</p>
        <Link to={`/products/${product.id}`} className="line-clamp-1 text-base font-semibold text-slate-900 hover:text-brand-700">
          {product.name}
        </Link>
        <p className="line-clamp-2 text-sm text-slate-600">{product.description || 'No description available.'}</p>
        <div className="flex items-center justify-between pt-1">
          <p className="font-semibold text-brand-700">{currency(product.price)}</p>
          <p className="text-xs text-slate-500">Stock {product.stock_quantity}</p>
        </div>
      </div>
    </article>
  )
}
