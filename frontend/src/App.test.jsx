// src/App.test.jsx - Test that frontend fetches and displays backend message
// ########################################################################################

import { render, screen, waitFor } from '@testing-library/react';
import { expect, test, vi } from 'vitest';
import App from './App';

// Mock fetch globally (simulates backend response)
vi.stubGlobal('fetch', vi.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ message: 'Hello from backend!' }),
  })
));

test('displays message from backend', async () => {
  render(<App />);
  
  // Wait for fetch to resolve and message to appear
  await waitFor(() => {
    expect(screen.getByText('Hello from backend!')).toBeInTheDocument();
  });
});