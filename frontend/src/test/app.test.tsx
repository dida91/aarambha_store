import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';

vi.mock('../api', async () => {
  const actual = await vi.importActual<typeof import('../api')>('../api');
  return {
    ...actual,
    getEnveloped: vi.fn().mockResolvedValue([]),
    postEnveloped: vi.fn(),
  };
});

import App from '../App';

describe('Aarambha Store app', () => {
  it('renders store branding', () => {
    render(<App />);
    expect(screen.getByText('Aarambha Store')).toBeInTheDocument();
  });
});
