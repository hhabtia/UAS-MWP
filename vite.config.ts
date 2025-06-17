import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // ✅ Tambahan agar bisa pakai alias `@`

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // ✅ Alias untuk path absolute ke folder src
    },
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
