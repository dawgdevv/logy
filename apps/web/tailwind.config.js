/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        deep: '#0c0a09',
        surface: '#1c1917',
        elevated: '#292524',
        border: {
          subtle: '#44403c',
          muted: '#292524',
        },
        accent: {
          DEFAULT: '#f59e0b',
          dim: '#92400e',
          glow: 'rgba(245, 158, 11, 0.12)',
        },
      },
      fontFamily: {
        mono: ['"DM Mono"', 'monospace'],
        serif: ['"Instrument Serif"', 'serif'],
      },
    },
  },
  plugins: [],
}
