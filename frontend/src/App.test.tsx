import { describe, expect, it } from 'vitest'

import { currency } from './lib/utils'

describe('currency utility', () => {
  it('formats numbers in rupees', () => {
    expect(currency('125.5')).toBe('Rs 125.50')
  })

  it('returns fallback for invalid values', () => {
    expect(currency('bad')).toBe('Rs 0.00')
  })
})
