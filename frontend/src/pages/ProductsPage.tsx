import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'

import { CategoryFilter } from '../components/common/CategoryFilter'
import { EmptyState } from '../components/common/EmptyState'
import { ErrorState } from '../components/common/ErrorState'
import { Loader } from '../components/common/Loader'
import { ProductGrid } from '../components/common/ProductGrid'
import { SearchBar } from '../components/common/SearchBar'
import { getCategories, getProducts } from '../features/products/service'
import type { Category, Product } from '../types/product'

export function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [categories, setCategories] = useState<Category[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const query = useMemo(
    () => ({
      search: searchParams.get('search') ?? '',
      category: searchParams.get('category') ?? '',
      ordering: searchParams.get('ordering') ?? '-created_at',
      page: searchParams.get('page') ?? '1',
    }),
    [searchParams],
  )

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const [categoryData, productData] = await Promise.all([
          getCategories(),
          getProducts({
            search: query.search || undefined,
            category: query.category || undefined,
            ordering: query.ordering || undefined,
            page: query.page,
          }),
        ])
        setCategories(categoryData)
        setProducts(productData.results)
      } catch (err) {
        setError((err as { message?: string }).message ?? 'Failed to fetch products.')
      } finally {
        setLoading(false)
      }
    }

    void load()
  }, [query])

  const updateQuery = (next: Partial<typeof query>) => {
    const params = new URLSearchParams(searchParams)
    for (const [key, value] of Object.entries(next)) {
      if (!value) {
        params.delete(key)
      } else {
        params.set(key, value)
      }
    }
    if (next.search !== undefined || next.category !== undefined || next.ordering !== undefined) {
      params.set('page', '1')
    }
    setSearchParams(params)
  }

  return (
    <section className="space-y-5">
      <div className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-soft md:flex-row md:items-center md:justify-between">
        <div className="w-full md:max-w-md">
          <SearchBar initialValue={query.search} onSearch={(value) => updateQuery({ search: value })} />
        </div>
        <div className="flex flex-wrap gap-2">
          <CategoryFilter categories={categories} selected={query.category} onChange={(value) => updateQuery({ category: value })} />
          <select
            value={query.ordering}
            onChange={(event) => updateQuery({ ordering: event.target.value })}
            className="rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-200"
            aria-label="Sort products"
          >
            <option value="-created_at">Newest</option>
            <option value="price">Price: Low to high</option>
            <option value="-price">Price: High to low</option>
            <option value="name">Name: A to Z</option>
          </select>
        </div>
      </div>

      {loading ? <Loader label="Loading products..." /> : null}
      {error ? <ErrorState message={error} /> : null}
      {!loading && !error && products.length === 0 ? (
        <EmptyState title="No products found" description="Try updating your search or category filters." />
      ) : null}
      {!loading && !error && products.length > 0 ? <ProductGrid products={products} /> : null}
    </section>
  )
}
