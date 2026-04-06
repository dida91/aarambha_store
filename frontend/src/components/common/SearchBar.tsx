import { FormEvent, useState } from 'react'

interface SearchBarProps {
  initialValue?: string
  onSearch: (term: string) => void
}

export function SearchBar({ initialValue = '', onSearch }: SearchBarProps) {
  const [value, setValue] = useState(initialValue)

  const submit = (event: FormEvent) => {
    event.preventDefault()
    onSearch(value.trim())
  }

  return (
    <form onSubmit={submit} className="flex gap-2">
      <input
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Search products"
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-200"
      />
      <button
        type="submit"
        className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-300 disabled:cursor-not-allowed disabled:opacity-60"
      >
        Search
      </button>
    </form>
  )
}
