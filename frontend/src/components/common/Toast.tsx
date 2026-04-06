import { useToast } from '../../hooks/useToast'

const tones = {
  success: 'border-green-200 bg-green-50 text-green-700',
  error: 'border-red-200 bg-red-50 text-red-700',
  info: 'border-slate-200 bg-white text-slate-700',
}

export function Toast() {
  const { toasts, removeToast } = useToast()

  return (
    <div className="pointer-events-none fixed right-4 top-4 z-50 flex w-full max-w-sm flex-col gap-2">
      {toasts.map((toast) => (
        <button
          key={toast.id}
          type="button"
          className={`pointer-events-auto rounded-xl border p-3 text-left text-sm shadow-soft ${tones[toast.type]}`}
          onClick={() => removeToast(toast.id)}
        >
          {toast.message}
        </button>
      ))}
    </div>
  )
}
