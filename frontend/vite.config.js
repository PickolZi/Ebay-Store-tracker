import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        // target: "http://127.0.0.1:5000",  // Running w/o Docker
        target: "http://flask_backend:5000",     // Running w/ Docker
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
