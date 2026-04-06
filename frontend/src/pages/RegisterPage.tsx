import { FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '../components/common/ErrorState'
import { useAuth } from '../hooks/useAuth'
import { useToast } from '../hooks/useToast'

interface RegisterForm {
  username: string
  email: string
  password: string
  first_name: string
  last_name: string
  phone: string
}

export function RegisterPage() {
  const { registerUser } = useAuth()
  const { showToast } = useToast()
  const navigate = useNavigate()

  const [form, setForm] = useState<RegisterForm>({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    phone: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const validate = (): string | null => {
    if (!form.username.trim()) return 'Username is required.'
    if (!form.email.trim() || !form.email.includes('@')) return 'Valid email is required.'
    if (form.password.length < 8) return 'Password must be at least 8 characters.'
    return null
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    const validationError = validate()
    if (validationError) {
      setError(validationError)
      return
    }

    setLoading(true)
    setError('')
    try {
      await registerUser({
        ...form,
        username: form.username.trim(),
        email: form.email.trim(),
        first_name: form.first_name.trim(),
        last_name: form.last_name.trim(),
        phone: form.phone.trim(),
      })
      showToast('Registration successful.', 'success')
      navigate('/')
    } catch (err) {
      setError((err as { message?: string }).message ?? 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="mx-auto max-w-md rounded-xl border border-slate-200 bg-white p-6 shadow-soft">
      <h1 className="text-xl font-semibold">Register</h1>
      <p className="mt-1 text-sm text-slate-600">Create your Aarambha Store account.</p>

      <form onSubmit={submit} className="mt-4 space-y-3">
        {error ? <ErrorState message={error} /> : null}
        {(
          [
            ['username', 'Username'],
            ['email', 'Email'],
            ['first_name', 'First name'],
            ['last_name', 'Last name'],
            ['phone', 'Phone'],
          ] as const
        ).map(([key, label]) => (
          <label key={key} className="block space-y-1 text-sm">
            <span>{label}</span>
            <input
              type={key === 'email' ? 'email' : 'text'}
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
              value={form[key]}
              onChange={(event) => setForm((prev) => ({ ...prev, [key]: event.target.value }))}
            />
          </label>
        ))}

        <label className="block space-y-1 text-sm">
          <span>Password</span>
          <input
            type="password"
            className="w-full rounded-lg border border-slate-300 px-3 py-2"
            value={form.password}
            onChange={(event) => setForm((prev) => ({ ...prev, password: event.target.value }))}
          />
        </label>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Creating account...' : 'Register'}
        </button>
      </form>

      <p className="mt-3 text-sm text-slate-600">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-brand-700 hover:underline">
          Login
        </Link>
      </p>
    </section>
  )
}
