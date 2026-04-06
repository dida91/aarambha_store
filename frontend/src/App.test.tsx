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
})
