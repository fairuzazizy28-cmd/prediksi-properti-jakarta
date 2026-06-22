import React from 'react';

function Home({ setCurrentView }) {
  return (
    <div className="flex flex-col max-w-[1440px] mx-auto w-full px-container-padding py-10 space-y-12">
      
      {/* Hero Section */}
      <div className="bg-[#131A32] rounded-[32px] overflow-hidden shadow-2xl border border-white/5 relative flex flex-col lg:flex-row items-center min-h-[460px]">
        
        {/* Abstract Glow in background */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/20 blur-[120px] rounded-full translate-x-1/2 -translate-y-1/4 pointer-events-none"></div>

        {/* Text Content */}
        <div className="lg:w-1/2 p-12 lg:p-16 z-10">
          <h1 className="text-4xl lg:text-[52px] font-extrabold text-white leading-[1.1] tracking-tight mb-6">
            Prediksi Harga<br />
            Properti Cerdas<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">dengan AI</span>
          </h1>
          <p className="text-slate-400 text-lg mb-10 max-w-md leading-relaxed">
            Platform intelijen properti premium. Analisis jutaan titik data untuk memberikan estimasi harga yang akurat dan wawasan mendalam bagi investor dan pemilik rumah.
          </p>
          <button 
            onClick={() => setCurrentView('prediction')}
            className="inline-flex items-center justify-center gap-3 px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-400 to-purple-500 text-white font-bold text-lg hover:opacity-90 hover:shadow-[0_0_30px_rgba(0,229,255,0.4)] transition-all duration-300 group"
          >
            Mulai Prediksi Sekarang 
            <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
          </button>
        </div>

        {/* Abstract Image / Illustration */}
        <div className="lg:w-1/2 p-12 flex justify-center lg:justify-end z-10">
          <div className="relative w-full max-w-[400px] aspect-square rounded-[24px] overflow-hidden shadow-[0_20px_50px_rgba(0,0,0,0.5)] border border-white/10 bg-[#0A0F24]">
             <img src="https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2070&auto=format&fit=crop" alt="AI Abstract" className="w-full h-full object-cover opacity-80 mix-blend-luminosity" />
             <div className="absolute inset-0 bg-gradient-to-tr from-cyan-500/20 to-purple-500/20"></div>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard 
          icon={
            <svg width="200" height="200" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 9.5L12 3L21 9.5V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V9.5Z" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M9 21V12H15V21" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          } 
          title="TOTAL DATA PROPERTI" 
          value="36,373" 
        />
        <MetricCard 
          icon={
            <svg width="150" height="150" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="6" width="18" height="12" rx="2" stroke="#A855F7" stroke-width="2"/>
              <circle cx="12" cy="12" r="3" stroke="#A855F7" stroke-width="2"/>
              <path d="M18 12H18.01" stroke="#A855F7" stroke-width="2" stroke-linecap="round"/>
              <path d="M6 12H6.01" stroke="#A855F7" stroke-width="2" stroke-linecap="round"/>
            </svg>
          } 
          title="MEDIAN HARGA PROPERTI" 
          value="Rp 4.5M" />
        <MetricCard 
          icon={
            <svg width="200" height="200" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="9" stroke="#A855F7" stroke-width="2"/>
              <circle cx="12" cy="12" r="5" stroke="#A855F7" stroke-width="2"/>
              <circle cx="12" cy="12" r="1.5" fill="#A855F7"/>
              <path d="M12 3V5" stroke="#A855F7" stroke-width="2" stroke-linecap="round"/>
              <path d="M12 19V21" stroke="#A855F7" stroke-width="2" stroke-linecap="round"/>
              <path d="M3 12H5" stroke="#A855F7" stroke-width="2" stroke-linecap="round"/>
              <path d="M19 12H21" stroke="#A855F7" stroke-width="2" stroke-linecap="round"/>
            </svg>
            } 
            title="AKURASI MODEL" 
            value={<span className="text-success">0.86 <span className="text-[10px] bg-success/20 px-2 py-0.5 rounded ml-1">R²</span></span>} />
        <MetricCard 
          icon={
            <svg width="200" height="200" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 6L9 3L15 6L20 3V18L15 21L9 18L4 21V6Z" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M9 3V18" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M15 6V21" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            } 
            title="KAWASAN/KECATAMAN TERCAKUP" 
            value="302" />
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Feature 1 */}
        <div className="bg-[#131A32] p-8 rounded-[32px] border border-white/5 flex flex-col transition-transform hover:-translate-y-2">
           <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center text-xl mb-6 border border-white/10">🤖</div>
           <h3 className="text-2xl font-bold text-white mb-4">Prediksi Harga</h3>
           <p className="text-slate-400 mb-8 flex-grow">
             Masukkan detail properti seperti lokasi, luas tanah, dan fasilitas untuk mendapatkan estimasi harga pasar terkini yang didukung oleh model AI canggih kami.
           </p>
           <button onClick={() => setCurrentView('prediction')} className="w-full flex justify-between items-center px-5 py-3.5 bg-white/5 hover:bg-white/10 rounded-xl text-white font-semibold transition-colors border border-white/5">
             Buka Fitur <span className="text-slate-400">→</span>
           </button>
        </div>

        {/* Feature 2 */}
        <div className="bg-[#131A32] p-8 rounded-[32px] border border-white/5 flex flex-col transition-transform hover:-translate-y-2">
           <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center text-xl mb-6 border border-white/10">📈</div>
           <h3 className="text-2xl font-bold text-white mb-4">Analytical Insight</h3>
           <p className="text-slate-400 mb-8 flex-grow">
             Jelajahi tren pasar, perbandingan area, dan analisis mendalam untuk mengambil keputusan investasi yang lebih cerdas dan berdasarkan data real-time.
           </p>
           <button onClick={() => setCurrentView('insight')} className="w-full flex justify-between items-center px-5 py-3.5 bg-white/5 hover:bg-white/10 rounded-xl text-white font-semibold transition-colors border border-white/5">
             Buka Fitur <span className="text-slate-400">→</span>
           </button>
        </div>

        {/* Feature 3: Insight Snapshot */}
        <div className="bg-transparent p-8 rounded-[32px] border border-white/20 flex flex-col relative overflow-hidden">
           <div className="flex justify-between items-start mb-6">
              <h3 className="text-2xl font-bold text-white">Insight<br/>Snapshot</h3>
              <span className="text-slate-500">•••</span>
           </div>

           <div className="space-y-5 mb-8">
             <div>
               <p className="text-[12px] font-bold text-slate-400 tracking-widest uppercase mb-4">Top 5 Median Harga Kawasan Termahal</p>
               <div className="space-y-3">
                 <ProgressBar label="Patal Senayan" value="Rp 36M" percent="100%" />
                 <ProgressBar label="Mega Kuningan" value="Rp 35M" percent="97%" />
                 <ProgressBar label="Menteng" value="Rp 32M" percent="88%" />
                 <ProgressBar label="Patra Kuningan" value="Rp 30.05M" percent="83%" />
                 <ProgressBar label="Kuningan" value="Rp 27.75M" percent="77%" />
               </div>
             </div>
             
             <div className="pt-4 border-t border-white/10">
                <p className="text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-6">Distribusi Harga</p>
                <div className="flex items-end gap-2 h-20 w-full justify-between px-2">
                   {/* Murah (500 Jt - 3.66 M) */}
                   <div className="w-full bg-white/10 rounded-t-sm h-[67%] hover:bg-white/20 transition-all relative group">
                     <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] text-white/0 group-hover:text-white/100 transition-opacity">6,049</span>
                   </div>
                   <div className="w-full bg-purple-400 rounded-t-sm h-[100%] shadow-[0_0_15px_rgba(192,132,252,0.5)] relative group cursor-pointer hover:bg-purple-300 transition-colors">
                     <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] font-bold text-white/0 group-hover:text-purple-300 transition-opacity">9,011</span>
                   </div>
                   
                   {/* Menengah (3.66 M - 6.83 M) */}
                   <div className="w-full bg-white/20 rounded-t-sm h-[56%] hover:bg-white/30 transition-all relative group">
                     <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] text-white/0 group-hover:text-white/100 transition-opacity">5,042</span>
                   </div>
                   <div className="w-full bg-white/10 rounded-t-sm h-[40%] hover:bg-white/20 transition-all relative group">
                     <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] text-white/0 group-hover:text-white/100 transition-opacity">3,593</span>
                   </div>
                   
                   {/* Premium (6.83 M - 10 M+) */}
                   <div className="w-full bg-white/10 rounded-t-sm h-[51%] hover:bg-white/20 transition-all relative group">
                     <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] text-white/0 group-hover:text-white/100 transition-opacity">4,618</span>
                   </div>
                   <div className="w-full bg-white/30 rounded-t-sm h-[89%] hover:bg-white/40 transition-all relative group cursor-pointer">
                     <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] text-white/0 group-hover:text-white/100 transition-opacity">8,060</span>
                   </div>
                </div>
                <div className="flex justify-between text-[8px] font-bold text-slate-500 uppercase mt-3 px-2">
                  <div className="flex flex-col">
                     <span className="text-white mb-0.5">Murah</span>
                     <span className="text-[7px]">500Jt - 3.66M</span>
                  </div>
                  <div className="flex flex-col items-center">
                     <span className="text-white mb-0.5">Menengah</span>
                     <span className="text-[7px]">3.66M - 6.83M</span>
                  </div>
                  <div className="flex flex-col items-end">
                     <span className="text-white mb-0.5">Premium</span>
                     <span className="text-[7px]">6.83M - 10M+</span>
                  </div>
                </div>
             </div>
           </div>
        </div>

      </div>
    </div>
  );
}

// Utility Components
const MetricCard = ({ icon, title, value }) => (
  <div className="bg-[#131A32] p-6 rounded-[24px] border border-white/5 flex flex-col justify-between hover:bg-[#1A2242] transition-colors">
    <div className="w-10 h-10 bg-white/5 rounded-lg flex items-center justify-center text-lg mb-6 border border-white/10">
      {icon}
    </div>
    <div>
      <p className="text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-2">{title}</p>
      <h4 className="text-3xl font-extrabold text-white">{value}</h4>
    </div>
  </div>
);

const ProgressBar = ({ label, value, percent }) => (
  <div className="w-full">
    <div className="flex justify-between text-xs font-semibold text-white mb-1.5">
      <span>{label}</span>
      <span className="text-slate-300">{value}</span>
    </div>
    <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
      <div className="h-full bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full" style={{ width: percent }}></div>
    </div>
  </div>
);

export default Home;
