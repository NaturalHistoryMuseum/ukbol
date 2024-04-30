import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    proxy: {
      // for the dev env, proxy the requests to the API to the Flask server
      '/api': 'http://localhost:5000',
    },
  },
});
