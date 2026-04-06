import type { Product } from '../types/api'

interface ProductListProps {
  products: Product[]
}

export function ProductList({ products }: ProductListProps) {
  return (
    <section aria-label="Product catalog">
      <h2>Aarambha Store Products</h2>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            <strong>{product.name}</strong> — NPR {product.price} — Stock: {product.stock_quantity}
          </li>
        ))}
      </ul>
    </section>
  )
}
