import { render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import App from './App'

const mockFetch = vi.fn()

vi.stubGlobal('fetch', mockFetch)

describe('Aarambha Store app', () => {
  beforeEach(() => {
    mockFetch.mockReset()
  })

  it('renders brand and product data from API', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'Products fetched',
        data: [
          {
            id: 1,
            name: 'Ilam Tea',
            slug: 'ilam-tea',
            price: '500.00',
            stock_quantity: 5,
          },
        ],
        errors: null,
      }),
    })

    render(<App />)

    expect(screen.getByRole('heading', { name: 'Aarambha Store' })).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText(/Ilam Tea/)).toBeInTheDocument()
    })
  })

  it('shows error when products fail to load', async () => {
    mockFetch.mockResolvedValueOnce({ ok: false, status: 500 })

    render(<App />)

    await waitFor(() => {
      expect(
        screen.getByText('Unable to load products from Aarambha Store API.'),
      ).toBeInTheDocument()
    })
  })

  it('renders products from paginated API envelope data', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'Products fetched',
        data: {
          count: 1,
          next: null,
          previous: null,
          results: [
            {
              id: 2,
              name: 'Mustang Apples',
              slug: 'mustang-apples',
              price: '350.00',
              stock_quantity: 14,
            },
          ],
        },
        errors: null,
      }),
    })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/Mustang Apples/)).toBeInTheDocument()
    })
  })

  it('does not crash when API returns malformed product list data', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'Products fetched',
        data: { unexpected: 'shape' },
        errors: null,
      }),
    })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Aarambha Store Products' })).toBeInTheDocument()
    })
  })
})
