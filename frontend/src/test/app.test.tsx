import { render, screen } from '@testing-library/react';

import App from '../App';

describe('Aarambha Store app', () => {
  it('renders store branding', () => {
    render(<App />);
    expect(screen.getByText('Aarambha Store')).toBeInTheDocument();
  });
});
