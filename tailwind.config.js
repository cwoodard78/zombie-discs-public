/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // All HTML templates in project folder
    './**/templates/**/*.html', // Nested templates across apps
    './**/*.html', // Any stray HTML files
    './**/*.js', // Stray JavaScript files in the project
    './static/css/styles.css', // Styles file with Tailwind directives
    './static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  safelist: [
    'hidden',
    'block',
    'md:flex',
    'md:hidden',
  ],
  plugins: [],
}

