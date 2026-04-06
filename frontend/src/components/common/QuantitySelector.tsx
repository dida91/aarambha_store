interface QuantitySelectorProps {
  value: number
  min?: number
  max?: number
  onChange: (value: number) => void
}

export function QuantitySelector({ value, min = 1, max = 99, onChange }: QuantitySelectorProps) {
  const set = (next: number) => {
    if (next < min || next > max) {
      return
    }
    onChange(next)
  }

  return (
    <div className="inline-flex items-center rounded-lg border border-slate-300">
      <button
        type="button"
        className="px-3 py-1 text-slate-700 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
        onClick={() => set(value - 1)}
        disabled={value <= min}
      >
        -
      </button>
      <span className="min-w-10 px-2 text-center text-sm">{value}</span>
      <button
        type="button"
        className="px-3 py-1 text-slate-700 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
        onClick={() => set(value + 1)}
        disabled={value >= max}
      >
        +
      </button>
    </div>
  )
}
