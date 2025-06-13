/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",   // <== adjust this path to match your project
    "./app/**/*.{js,ts,jsx,tsx}",   // <== include if you're using the /app directory (Next.js 13+)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
