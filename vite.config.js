import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/',
  server: {
    proxy: {
      '/shortener': 'http://localhost:5000',
      '/analytics': 'http://localhost:5000',
      '/all_urls': 'http://localhost:5000',
      '/start_scrape': 'http://localhost:5000',
      '/scrape_status': 'http://localhost:5000',
      '/channels': 'http://localhost:5001',
      '/generate_qr': 'http://localhost:5002'
    }

  }
});
