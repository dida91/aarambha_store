import type { Category } from '../../types/product'

interface CategoryFilterProps {
  categories: Category[]
  selected: string
  onChange: (value: string) => void
}

export function CategoryFilter({ categories, selected, onChange }: CategoryFilterProps) {
  return (
    <select
      value={selected}
      onChange={(event) => onChange(event.target.value)}
      className="rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-200"
      aria-label="Filter by category"
    >
      <option value="">All categories</option>
      {categories.map((category) => (
        <option key={category.id} value={String(category.id)}>
          {category.name}
        </option>
      ))}
    </select>
  )
}
