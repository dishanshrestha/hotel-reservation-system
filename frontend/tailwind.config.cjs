const defaultTheme = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#0f766e',
          'primary-dark': '#115e59',
          accent: '#f59e0b',
          gold: '#eabe6c',
          ink: '#0f172a',
          muted: '#64748b',
          border: '#cbd5e1',
          surface: '#ffffff',
          bg: '#f8fafc',
          dark: '#1f1f1f',
          'dark-light': '#2a2a2a',
        },
      },
      fontFamily: {
        sans: ['Poppins', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
