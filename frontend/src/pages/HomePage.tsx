import { Link } from 'react-router-dom'

export function HomePage() {
  return (
    <section className="space-y-10">
      <div className="rounded-2xl bg-gradient-to-r from-brand-700 to-brand-500 p-8 text-white shadow-soft">
        <h1 className="text-3xl font-bold sm:text-4xl">Shop trusted products from Aarambha Store</h1>
        <p className="mt-3 max-w-2xl text-sm text-brand-50 sm:text-base">
          Discover quality essentials with fast delivery across Nepal.
        </p>
        <Link
          to="/products"
          className="mt-6 inline-flex rounded-lg bg-white px-4 py-2 text-sm font-semibold text-brand-700 hover:bg-brand-50"
        >
          Browse Products
        </Link>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-soft">
        <h2 className="text-xl font-semibold">Why shop with us?</h2>
        <ul className="mt-3 grid gap-3 text-sm text-slate-600 sm:grid-cols-3">
          <li className="rounded-lg bg-slate-50 p-3">Verified catalog and transparent pricing</li>
          <li className="rounded-lg bg-slate-50 p-3">Simple secure checkout with order tracking</li>
          <li className="rounded-lg bg-slate-50 p-3">Optimized for mobile and desktop shopping</li>
        </ul>
      </div>
    </section>
  )
}
