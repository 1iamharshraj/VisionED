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
      'input-color': '7B7878',
      'input-stroke': 'E0DBDB',
      'gray-dark': '#273444',
      'gray': '#8492a6',
      'gray-light': '#d3dce6',
    },
    extend: {
      fontSize: {
        'h80': '80px',
        'h1': '40px',
        'h2': '36px',
        'h3': '30px',
        'subheading': '22px', // For sub-sections
        'h4': '24px',
        'h5': '20px',
        'small': '12px', // For captions
      }
    }
  },
  plugins: [],
}

