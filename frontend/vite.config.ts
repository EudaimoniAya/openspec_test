import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts', 'allure-vitest/setup'],
    globals: true,
    reporters: [
      'default',
      [
        'allure-vitest/reporter',
        {
          resultsDir: '../reports/allure-results/frontend',
        },
      ],
    ],
  },
})
