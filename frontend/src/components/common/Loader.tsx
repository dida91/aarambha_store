export function Loader({ label = 'Loading...' }: { label?: string }) {
  return (
    <div className="flex items-center justify-center py-10" role="status" aria-live="polite">
      <div className="h-6 w-6 animate-spin rounded-full border-2 border-brand-200 border-t-brand-600" />
      <span className="ml-3 text-sm text-slate-600">{label}</span>
    </div>
  )
}
