export function currency(value: string | number): string {
  const num = Number(value)
  if (Number.isNaN(num)) {
    return 'Rs 0.00'
  }
  return `Rs ${num.toFixed(2)}`
}

export function getImageUrl(input: string | { url?: string } | null | undefined): string {
  if (!input) {
    return ''
  }
  if (typeof input === 'string') {
    return input
  }
  return input.url ?? ''
}
