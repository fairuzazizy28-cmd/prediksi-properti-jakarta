/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary-container": "#1d3eb3",
        "primary": "#2E5BFF", // Royal Blue
        "secondary": "#39FF14", // Neon Green
        "tertiary": "#FF8C00", // Orange
        "surface-container-low": "#111833", // Slightly lighter than neutral
        "surface": "#0A0F24", // Neutral Background
        "outline": "#8e90a2",
        "on-surface": "#f8fafc",
        "on-surface-variant": "#94a3b8",
        "error": "#ef4444",
        "success": "#39FF14", // Neon Green
        "warning": "#FF8C00", // Using tertiary orange for warning too
      },
      fontFamily: {
        "display-lg": ["'Plus Jakarta Sans'", "sans-serif"],
        "headline-lg": ["'Plus Jakarta Sans'", "sans-serif"],
        "body-md": ["'Plus Jakarta Sans'", "sans-serif"],
        "data-mono": ["'JetBrains Mono'", "monospace"],
        "label-caps": ["'Plus Jakarta Sans'", "sans-serif"],
        "body-sm": ["'Plus Jakarta Sans'", "sans-serif"],
        "headline-xl": ["'Plus Jakarta Sans'", "sans-serif"],
        "headline-lg-mobile": ["'Plus Jakarta Sans'", "sans-serif"]
      },
      spacing: {
        "container-padding": "32px",
        "unit": "4px",
        "gutter": "24px",
        "section-margin": "64px",
        "card-gap": "16px"
      }
    },
  },
  plugins: [],
}
