import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:18789',
      '/socket.io': {
        target: 'http://localhost:18789',
        ws: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
});
