/** @type {import('tailwindcss').Config} */


module.exports = {
  content: [
    './templates/**/*.html'
  ],
  theme: {
    colors: {
      'background': '#191919',
      'primary-ascent': '#8878f5',
      'secondary-background': '#212021',
      'text-color': '#D9D9D9',
      'secondtext-color': '#444444',
      'secondary-ascent': '#9A8DF6',
      'gray-dark': '#273444',
      'gray': '#8492a6',
      'gray-light': '#d3dce6',
    },
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      serif: ['Merriweather', 'serif']
    },
    extend: {},
  },
  plugins: [],
}

