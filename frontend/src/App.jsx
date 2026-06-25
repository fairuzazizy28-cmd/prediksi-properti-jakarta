import React, { useState, useEffect } from 'react';
import Home from './pages/Home';
import Prediction from './pages/Prediction';
import Opportunities from './pages/Opportunities';
import Affordability from './pages/Affordability';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [isBackendWakingUp, setIsBackendWakingUp] = useState(true);

  useEffect(() => {
    const pingBackend = async () => {
      try {
        const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const res = await fetch(`${API_BASE_URL}/`);
        if (res.ok) {
          setIsBackendWakingUp(false);
        } else {
          // Fallback if not 200 OK but server is running
          setIsBackendWakingUp(false);
        }
      } catch (err) {
        // If it fails immediately (CORS or network error before boot), we can try again after a delay
        setTimeout(pingBackend, 5000);
      }
    };
    pingBackend();
  }, []);

  return (
    <div className="min-h-screen bg-[#0A0F24] flex flex-col text-white font-['Plus_Jakarta_Sans']">
      
      {/* Top Navbar */}
      <nav className="fixed top-0 w-full z-[1000] bg-[#0A0F24]/80 backdrop-blur-xl border-b border-white/5 shadow-md">
        <div className="flex justify-between items-center px-8 h-20 w-full max-w-[1440px] mx-auto">
          <div 
            className="font-extrabold text-2xl tracking-tight cursor-pointer flex items-center gap-3"
            onClick={() => setCurrentView('home')}
          >
            {/* J Logo */}
            <svg width="44" height="44" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="drop-shadow-lg">
              <path d="M25 25h50v15H55v30c0 8.284-6.716 15-15 15s-15-6.716-15-15v-5h15v5c0 2.761 2.239 5 5 5s5-2.239 5-5V40H25V25z" fill="#7C3AED"/>
              <circle cx="85" cy="32" r="12" fill="#00E5FF"/>
            </svg>
            <div className="flex flex-col justify-center">
              <span className="text-white leading-none mb-0.5">Taksirin<span className="text-primary">Jakarta</span></span>
              <span className="text-[9px] text-slate-400 font-bold tracking-[0.2em] uppercase leading-none">SMART PROPERTY PREDICTION</span>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <button 
              onClick={() => setCurrentView('home')} 
              className={`font-semibold transition-colors ${currentView === 'home' ? 'text-primary border-b-2 border-primary pb-1' : 'text-slate-400 hover:text-white'}`}
            >
              Home
            </button>
            <button 
              onClick={() => setCurrentView('prediction')} 
              className={`font-semibold transition-colors ${currentView === 'prediction' ? 'text-primary border-b-2 border-primary pb-1' : 'text-slate-400 hover:text-white'}`}
            >
              Prediction
            </button>
            <button 
              onClick={() => setCurrentView('opportunities')} 
              className={`font-semibold transition-colors ${currentView === 'opportunities' ? 'text-primary border-b-2 border-primary pb-1' : 'text-slate-400 hover:text-white'}`}
            >
              Opportunities
            </button>
            <button 
              onClick={() => setCurrentView('affordability')} 
              className={`font-semibold transition-colors ${currentView === 'affordability' ? 'text-primary border-b-2 border-primary pb-1' : 'text-slate-400 hover:text-white'}`}
            >
              Affordability
            </button>
            <button 
              onClick={() => setCurrentView('insight')} 
              className={`font-semibold transition-colors ${currentView === 'insight' ? 'text-primary border-b-2 border-primary pb-1' : 'text-slate-400 hover:text-white'}`}
            >
              Insight
            </button>
          </div>
          <div className="hidden md:block">
            <button 
              onClick={() => setCurrentView('prediction')}
              className="px-6 py-2.5 bg-white/10 hover:bg-white/20 border border-white/10 rounded-full font-semibold text-sm transition-colors"
            >
              Mulai Prediksi
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <div className="flex-grow pt-20">
        
        {isBackendWakingUp && (
          <div className="bg-[#B45309]/20 border-b border-[#F59E0B]/30 text-[#FCD34D] px-6 py-3 text-center text-sm font-semibold flex flex-wrap items-center justify-center gap-3 animate-pulse shadow-md">
            <svg className="animate-spin h-5 w-5 shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Sistem Sedang Membangunkan Server AI (Cold Start). Proses ini mungkin memakan waktu hingga 1 menit...</span>
          </div>
        )}

        {currentView === 'home' && <Home setCurrentView={setCurrentView} />}
        {currentView === 'prediction' && <Prediction />}
        {currentView === 'opportunities' && <Opportunities />}
        {currentView === 'affordability' && <Affordability />}
        {currentView === 'insight' && (
          <div className="flex-grow flex items-center justify-center flex-col">
            <h1 className="text-4xl font-bold text-white mb-4">Analytical Insight</h1>
            <p className="text-slate-400">Fitur ini masih dalam tahap pengembangan.</p>
            <button onClick={() => setCurrentView('home')} className="mt-8 px-6 py-2 bg-white/10 hover:bg-white/20 rounded-xl transition-colors">Kembali ke Home</button>
          </div>
        )}
      </div>

      {/* Footer applied globally */}
      <footer className="py-8 text-center text-slate-500 text-xs border-t border-white/5">
        <p>Data source: <span className="font-bold text-white">rumah123.com</span> | &copy; {new Date().getFullYear()} Fairuzazizy</p>
        <p className="mt-1">Email: <a href="mailto:fairuzazizy28@gmail.com" className="text-primary hover:text-cyan-400 transition-colors">fairuzazizy28@gmail.com</a></p>
        <div className="flex flex-wrap justify-center gap-3 mt-5 max-w-2xl mx-auto">
           <span className="px-3 py-1.5 rounded-full border border-white/10 bg-[#131A32] text-slate-300 font-mono tracking-widest text-[10px] shadow-sm hover:border-cyan-500/50 transition-colors">🐍 Python 3</span>
           <span className="px-3 py-1.5 rounded-full border border-white/10 bg-[#131A32] text-slate-300 font-mono tracking-widest text-[10px] shadow-sm hover:border-cyan-500/50 transition-colors">🧠 LightGBM </span>
           <span className="px-3 py-1.5 rounded-full border border-white/10 bg-[#131A32] text-slate-300 font-mono tracking-widest text-[10px] shadow-sm hover:border-cyan-500/50 transition-colors">⚡ FastAPI</span>
           <span className="px-3 py-1.5 rounded-full border border-white/10 bg-[#131A32] text-slate-300 font-mono tracking-widest text-[10px] shadow-sm hover:border-cyan-500/50 transition-colors">⚛️ React.js</span>
           <span className="px-3 py-1.5 rounded-full border border-white/10 bg-[#131A32] text-slate-300 font-mono tracking-widest text-[10px] shadow-sm hover:border-cyan-500/50 transition-colors">🎨 TailwindCSS</span>
           <span className="px-3 py-1.5 rounded-full border border-white/10 bg-[#131A32] text-slate-300 font-mono tracking-widest text-[10px] shadow-sm hover:border-cyan-500/50 transition-colors">📊 Scikit-Learn</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
