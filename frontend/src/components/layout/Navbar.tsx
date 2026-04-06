import { Link, NavLink } from 'react-router-dom'

import { useAuth } from '../../hooks/useAuth'
import { useCart } from '../../hooks/useCart'

const activeClass = 'text-brand-700'

export function Navbar() {
  const { isAuthenticated, logoutUser, user } = useAuth()
  const { cart } = useCart()
  const cartCount = (cart?.items ?? []).reduce((sum, item) => sum + item.quantity, 0)

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-3">
        <Link to="/" className="text-lg font-bold text-brand-700">
          Aarambha Store
        </Link>
        <nav className="flex items-center gap-4 text-sm">
          <NavLink to="/" className={({ isActive }) => (isActive ? activeClass : 'text-slate-600 hover:text-brand-700')}>
            Home
          </NavLink>
          <NavLink to="/products" className={({ isActive }) => (isActive ? activeClass : 'text-slate-600 hover:text-brand-700')}>
            Products
          </NavLink>
          <NavLink to="/cart" className={({ isActive }) => (isActive ? activeClass : 'text-slate-600 hover:text-brand-700')}>
            Cart ({cartCount})
          </NavLink>
          {isAuthenticated ? (
            <>
              <NavLink to="/profile" className={({ isActive }) => (isActive ? activeClass : 'text-slate-600 hover:text-brand-700')}>
                {user?.username}
              </NavLink>
              <button
                type="button"
                onClick={logoutUser}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-slate-700 hover:bg-slate-100"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={({ isActive }) => (isActive ? activeClass : 'text-slate-600 hover:text-brand-700')}>
                Login
              </NavLink>
              <NavLink to="/register" className={({ isActive }) => (isActive ? activeClass : 'text-slate-600 hover:text-brand-700')}>
                Register
              </NavLink>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
