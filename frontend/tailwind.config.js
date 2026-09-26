/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#070b12",
        panel: "#0d131f",
        panel2: "#121a29",
        border: "#1e2a3d",
        muted: "#8fa1b8",
        mint: "#6ee7a8",
        cyan: "#3ac6e0",
        amber: "#f5b76e",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "system-ui", "sans-serif"],
      },
      borderRadius: {
        card: "16px",
      },
    },
  },
  plugins: [],
};
