import { FormEvent, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import { ErrorState } from '../components/common/ErrorState'
import { useAuth } from '../hooks/useAuth'
import { useToast } from '../hooks/useToast'

export function LoginPage() {
  const { loginUser } = useAuth()
  const { showToast } = useToast()
  const navigate = useNavigate()
  const location = useLocation()
  const redirectTo = (location.state as { from?: string } | null)?.from ?? '/'

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    if (!username.trim() || !password.trim()) {
      setError('Username and password are required.')
      return
    }

    setLoading(true)
    setError('')
    try {
      await loginUser({ username: username.trim(), password })
      showToast('Logged in successfully.', 'success')
      navigate(redirectTo, { replace: true })
    } catch (err) {
      setError((err as { message?: string }).message ?? 'Login failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="mx-auto max-w-md rounded-xl border border-slate-200 bg-white p-6 shadow-soft">
      <h1 className="text-xl font-semibold">Login</h1>
      <p className="mt-1 text-sm text-slate-600">Access your Aarambha Store account.</p>
      <form onSubmit={submit} className="mt-4 space-y-3">
        {error ? <ErrorState message={error} /> : null}
        <label className="block space-y-1 text-sm">
          <span>Username</span>
          <input
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </label>
        <label className="block space-y-1 text-sm">
          <span>Password</span>
          <input
            type="password"
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p className="mt-3 text-sm text-slate-600">
        Don&apos;t have an account?{' '}
        <Link to="/register" className="font-medium text-brand-700 hover:underline">
          Register
        </Link>
      </p>
    </section>
  )
}
