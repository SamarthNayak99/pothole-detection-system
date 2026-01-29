import { defineConfig } from 'vite'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        'mobile-detect': resolve(__dirname, 'mobile-detect.html'),
        map: resolve(__dirname, 'map.html'),
        history: resolve(__dirname, 'history.html'),
        home: resolve(__dirname, 'home.html'),
      },
    },
  },
})
