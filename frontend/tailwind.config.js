/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      boxShadow: {
        futuristic: '0 30px 80px rgba(14, 165, 233, 0.18)',
      },
      colors: {
        navy: {
          900: '#050816',
          950: '#02040d'
        }
      }
    }
  },
  plugins: [],
};