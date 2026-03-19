import { defineConfig } from 'vite';

export default defineConfig({
    root: 'public',
    build: {
        outDir: '../dist',
        emptyOutDir: true,
    },
    server: {
        host: true,
        port: 5173,
        hmr: {
            protocol: 'ws',
            host: 'localhost',
            port: 5173,
            overlay: false,
        },
    },
});
