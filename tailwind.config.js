/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './core/templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'nepal-red': '#DC143C', // Crimson red standard in Nepal gov
        'nepal-blue': '#003893', // Deep blue
        'gov-bg': '#f3f4f6',
      },
      fontFamily: {
        'sans': ['Mukta', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
