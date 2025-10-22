// vite.config.js - Enhanced config for dev server and Vitest integration

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],  // React support
  server: {
    port: 3000,  // Consistent port (avoids conflicts)
    open: true,  // Auto-open browser on npm run dev
  },
  test: {
    globals: true,  // Use global test funcs (describe, it) without imports
    environment: 'jsdom',  // Browser simulation for DOM tests
    setupFiles: './src/setupTests.js',  // Load test helpers (create this file next)
  },
});