import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, res) => {
            if (err.code === 'ECONNREFUSED') {
              console.warn(
                '[Vite Proxy] Backend offline (http://127.0.0.1:8000). Start backend with: npm run dev:backend or uvicorn app.main:app --port 8000'
              );
            } else {
              console.error('[Vite Proxy Error]:', err.message);
            }
            if (res && !res.headersSent) {
              res.writeHead(503, { 'Content-Type': 'application/json' });
              res.end(
                JSON.stringify({
                  error: 'Backend Offline',
                  detail:
                    'CogniFlow backend server is not running on http://127.0.0.1:8000. Please start the backend service.',
                })
              );
            }
          });
        },
      },
    },
  },
});
