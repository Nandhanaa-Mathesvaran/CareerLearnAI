/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Purple / Lavender (main brand)
        brand: '#7c3aed', // violet-700
        brandLight: '#a78bfa', // violet-400
        lavender: '#ede9fe', // violet-100
        lavenderMid: '#c4b5fd', // violet-300

        // Coral / Peach (CTAs, highlights)
        coral: '#f97316', // orange-500
        coralLight: '#fed7aa', // orange-200
        peach: '#fde68a', // amber-200  (warm soft)
        peachDark: '#f59e0b', // amber-500

        // Mint / Teal (success, completed)
        mint: '#10b981', // emerald-500
        mintLight: '#d1fae5', // emerald-100
        teal: '#0d9488', // teal-600

        // Soft Yellow (tips, insights)
        lemon: '#fef08a', // yellow-200
        lemonDark: '#ca8a04', // yellow-600

        // Pink / Violet (decorative, selected)
        pink: '#ec4899', // pink-500
        pinkLight: '#fce7f3', // pink-100
        violet: '#8b5cf6', // violet-500

        // Neutral backgrounds
        bgBase: '#fafafa',
        bgSection: '#f5f3ff', // lavender-tinted
        bgSectionAlt: '#fff7ed', // peach-tinted

        // Dark hero
        heroBase: '#1e0a3c',
        heroDark: '#0f0620',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(135deg, #1e0a3c 0%, #3b0764 45%, #1e1b4b 100%)',
        'brand-gradient': 'linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%)',
        'coral-gradient': 'linear-gradient(135deg, #f97316 0%, #fb923c 50%, #fbbf24 100%)',
        'mint-gradient': 'linear-gradient(135deg, #10b981 0%, #0d9488 100%)',
        'peach-gradient': 'linear-gradient(135deg, #f97316 0%, #fbbf24 100%)',
        'pink-gradient': 'linear-gradient(135deg, #a855f7 0%, #ec4899 100%)',
        'lavender-gradient': 'linear-gradient(135deg, #ede9fe 0%, #e0d8ff 100%)',
        'glow-purple': 'radial-gradient(circle at 50% 50%, rgba(124,58,237,0.35) 0%, transparent 70%)',
        'glow-pink': 'radial-gradient(circle at 50% 50%, rgba(236,72,153,0.3) 0%, transparent 70%)',
        'glow-coral': 'radial-gradient(circle at 50% 50%, rgba(249,115,22,0.3) 0%, transparent 70%)',
        'glow-mint': 'radial-gradient(circle at 50% 50%, rgba(16,185,129,0.25) 0%, transparent 70%)',
      },
      boxShadow: {
        'glow-purple': '0 0 36px rgba(124,58,237,0.4)',
        'glow-pink': '0 0 36px rgba(236,72,153,0.35)',
        'glow-coral': '0 0 36px rgba(249,115,22,0.35)',
        'glow-mint': '0 0 28px rgba(16,185,129,0.3)',
        'card': '0 4px 24px rgba(15,6,32,0.07)',
        'card-hover': '0 10px 40px rgba(124,58,237,0.18)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s ease-in-out infinite',
        'fade-up': 'fade-up 0.5s ease-out forwards',
        'spin-slow': 'spin 8s linear infinite',
        'gradient': 'gradient-shift 8s ease infinite',
      },
      keyframes: {
        float: {
          '0%,100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-14px)' },
        },
        'fade-up': {
          'from': { opacity: '0', transform: 'translateY(18px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        'gradient-shift': {
          '0%,100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
    },
  },
  plugins: [],
}
