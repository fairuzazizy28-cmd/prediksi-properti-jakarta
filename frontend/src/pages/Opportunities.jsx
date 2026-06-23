import React, { useState, useEffect } from 'react';
import Pagination from '../components/Pagination';

export default function Opportunities() {
  const [discountVal, setDiscountVal] = useState(25);
  const [locationFilter, setLocationFilter] = useState('Seluruh Jakarta');
  const [sortOption, setSortOption] = useState('roi_desc');
  
  const [appliedDiscount, setAppliedDiscount] = useState(25);
  const [appliedLocation, setAppliedLocation] = useState('Seluruh Jakarta');

  const [opportunities, setOpportunities] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Compare Feature State
  const [compareList, setCompareList] = useState([]);

  useEffect(() => {
    const fetchOpps = async () => {
      try {
        setIsLoading(true);
        const queryParams = new URLSearchParams({
          min_discount: appliedDiscount,
          location: appliedLocation,
          sort: sortOption
        });
        const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const res = await fetch(`${API_BASE_URL}/api/opportunities?${queryParams}`);
        if (!res.ok) throw new Error('Gagal mengambil data dari server');
        const data = await res.json();
        if (data.status === 'success') {
          setOpportunities(data.data);
          setCurrentPage(1);
        } else {
          throw new Error(data.error || 'Terjadi kesalahan tidak dikenal');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchOpps();
  }, [appliedDiscount, appliedLocation, sortOption]);

  const handleApplyFilters = () => {
    setAppliedDiscount(discountVal);
    setAppliedLocation(locationFilter);
  };
  
  const handleToggleCompare = (opp) => {
    setCompareList(prev => {
      const exists = prev.find(item => item.id === opp.id);
      if (exists) {
        return prev.filter(item => item.id !== opp.id);
      } else {
        if (prev.length >= 4) {
          alert("Maksimal 4 properti untuk dibandingkan.");
          return prev;
        }
        return [...prev, opp];
      }
    });
  };
  
  const scrollToCompare = () => {
    const el = document.getElementById('compare-section');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  const filteredOpps = opportunities;

  return (
    <div className="flex w-full max-w-[1440px] mx-auto px-8 gap-8 pb-32 pt-8 min-h-screen relative">
      
      {/* LEFT SIDEBAR FILTER */}
      <aside className="w-72 shrink-0 flex flex-col gap-6 relative z-10">
        <div className="bg-[#131A32] rounded-[32px] border border-white/5 p-6 sticky top-28 shadow-xl">
          <h2 className="text-2xl font-bold text-white mb-8">Good Deal Finder</h2>
          
          <div className="space-y-8">
            {/* Location Radius */}
            <div>
              <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Radius Lokasi</label>
              <div className="relative">
                <select 
                  value={locationFilter}
                  onChange={(e) => setLocationFilter(e.target.value)}
                  className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white focus:outline-none focus:border-primary appearance-none cursor-pointer"
                >
                  <option>Seluruh Jakarta</option>
                  <option>Jakarta Selatan</option>
                  <option>Jakarta Pusat</option>
                  <option>Jakarta Barat</option>
                  <option>Jakarta Timur</option>
                  <option>Jakarta Utara</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
                  <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" /></svg>
                </div>
              </div>
            </div>

            {/* Minimum Discount */}
            <div>
              <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Diskon Minimum</label>
              <input 
                type="range" 
                min="5" 
                max="40" 
                value={discountVal}
                onChange={(e) => setDiscountVal(e.target.value)}
                className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-success"
              />
              <div className="flex justify-between mt-3 text-xs font-semibold">
                <span className="text-slate-400">5%</span>
                <span className="text-success bg-success/10 px-2 py-0.5 rounded-md">{discountVal}% (Ideal)</span>
                <span className="text-slate-400">40%</span>
              </div>
            </div>

            <button 
              onClick={handleApplyFilters}
              className="w-full mt-4 py-3.5 bg-primary hover:bg-primary/90 text-white rounded-xl text-sm font-bold shadow-[0_0_15px_rgba(45,104,255,0.3)] transition-all active:scale-95"
            >
              Terapkan Filter
            </button>
          </div>
        </div>
      </aside>

      {/* RIGHT MAIN CONTENT */}
      <main className="flex-grow flex flex-col relative z-0">
        
        {/* Header Bar */}
        <div className="flex justify-between items-center mb-6 bg-[#131A32] p-4 rounded-2xl border border-white/5">
          <div className="flex items-center gap-4">
            <div className="relative">
              <select 
                value={sortOption}
                onChange={(e) => setSortOption(e.target.value)}
                className="pl-10 pr-8 py-2 bg-[#0A0F24] border border-white/10 rounded-lg text-sm font-semibold text-white focus:outline-none focus:border-primary appearance-none cursor-pointer"
              >
                <option value="roi_desc">ROI Tertinggi</option>
                <option value="roi_asc">ROI Terendah</option>
                <option value="price_asc">Harga Termurah</option>
                <option value="price_desc">Harga Tertinggi</option>
              </select>
              <svg className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" /></svg>
              <svg className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" /></svg>
            </div>
          </div>
          <span className="text-sm font-medium text-slate-400">Menampilkan <strong className="text-white text-base">{filteredOpps.length} properti</strong> di bawah harga pasar</span>
        </div>

        {/* Loading / Error States */}
        {isLoading && (
          <div className="flex-grow flex items-center justify-center min-h-[400px]">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-slate-400 text-sm font-medium">Menyelaraskan taksiran AI dan memuat gambar properti...</p>
            </div>
          </div>
        )}
        
        {error && (
          <div className="flex-grow flex items-center justify-center min-h-[400px]">
            <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-8 text-center max-w-md">
              <svg className="w-12 h-12 text-red-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
              <p className="text-red-400 font-bold text-lg mb-2">Gagal Memuat Peluang</p>
              <p className="text-slate-400 text-sm leading-relaxed">{error}</p>
            </div>
          </div>
        )}

        {/* Property Grid */}
        {!isLoading && !error && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 relative z-10">
            {(() => {
              const itemsPerPage = 20;
              const totalPages = Math.ceil(filteredOpps.length / itemsPerPage);
              const paginatedOpps = filteredOpps.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
              
              return (
                <>
                  {paginatedOpps.map((opp, idx) => {
                    const isSelected = compareList.some(item => item.id === opp.id);
                    return (
                      <div key={idx} className={`bg-[#131A32] rounded-[24px] overflow-hidden flex flex-col group hover:-translate-y-1.5 transition-all duration-300 ${isSelected ? 'border-2 border-primary shadow-[0_0_20px_rgba(45,104,255,0.3)]' : 'border border-white/5 shadow-xl hover:shadow-2xl'}`}>
                        {/* Image Section */}
                        <div className="h-52 relative overflow-hidden bg-slate-800">
                          <img 
                            src={opp.image} 
                            alt={opp.title} 
                            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-in-out" 
                            onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=2075&auto=format&fit=crop'; }}
                          />
                  <div className="absolute inset-0 bg-gradient-to-t from-[#131A32] via-transparent to-transparent opacity-80"></div>
                  <div className="absolute top-4 left-4 bg-success text-[#0A0F24] text-[10px] font-extrabold px-3 py-1.5 rounded-full flex items-center gap-1.5 shadow-lg tracking-wide">
                    <span className="text-sm leading-none">✨</span> {opp.discountPercent} DI BAWAH PASAR
                  </div>
                </div>

                {/* Card Body */}
                <div className="p-6 flex flex-col flex-grow relative">
                  <div className="mb-6">
                    <h3 className="text-lg font-bold text-white mb-2 leading-tight line-clamp-2" title={opp.title}>{opp.title}</h3>
                    <p className="text-sm text-slate-400 flex items-center gap-1.5 font-medium">
                       <svg className="text-primary shrink-0" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                       <span className="truncate">{opp.location}</span>
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-6 bg-[#0A0F24] rounded-xl p-4 border border-white/5">
                     <div>
                       <p className="text-[10px] text-slate-500 font-bold tracking-widest uppercase mb-1">Harga Asli</p>
                       <p className="text-lg font-bold text-white truncate">{opp.actualPrice}</p>
                     </div>
                     <div className="text-right border-l border-white/5 pl-4">
                       <p className="text-[10px] text-success/80 font-bold tracking-widest uppercase mb-1">Taksiran AI</p>
                       <p className="text-lg font-bold text-success truncate">{opp.aiEstValue}</p>
                     </div>
                  </div>

                  <div className="flex justify-between items-center mt-auto pt-2">
                     <div className="flex flex-col">
                       <span className="text-[10px] text-slate-500 font-bold tracking-widest uppercase mb-0.5">Potensi ROI</span>
                       <div className="text-base font-extrabold text-white flex items-center gap-1.5">
                         {opp.roi} 
                         <svg className="text-success w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>
                       </div>
                     </div>
                     <div className="flex gap-2">
                       <button 
                         onClick={() => handleToggleCompare(opp)}
                         className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all ${isSelected ? 'bg-primary/20 text-primary border border-primary/50' : 'border border-white/10 text-white hover:bg-white/5 hover:border-white/20'}`}
                       >
                         {isSelected ? 'Terpilih' : 'Bandingkan'}
                       </button>
                       <a href={opp.url} target="_blank" rel="noreferrer" className="px-5 py-2.5 bg-primary hover:bg-primary/90 text-white rounded-xl text-sm font-bold shadow-[0_0_15px_rgba(45,104,255,0.3)] transition-all flex items-center gap-2">
                         Detail
                       </a>
                     </div>
                  </div>
                </div>
              </div>
            )})}
            
            {filteredOpps.length > 0 && Math.ceil(filteredOpps.length / 20) > 1 && (
              <div className="col-span-full">
                <Pagination 
                  currentPage={currentPage}
                  totalPages={Math.ceil(filteredOpps.length / 20)}
                  onPageChange={setCurrentPage}
                />
              </div>
            )}
            </>
            );
            })()}
            
            {filteredOpps.length === 0 && (
              <div className="col-span-2 py-16 text-center bg-[#131A32] rounded-[24px] border border-white/5">
                <p className="text-slate-400 font-medium">Tidak ada properti yang sesuai dengan filter Anda.</p>
              </div>
            )}
          </div>
        )}

        {/* COMPARISON SECTION */}
        <div id="compare-section" className={`transition-all duration-700 overflow-hidden ${compareList.length > 0 ? 'opacity-100 mb-10' : 'opacity-0 h-0 pointer-events-none'}`}>
          <div className="bg-[#131A32] border border-white/10 rounded-[32px] p-8 shadow-2xl relative">
            <h3 className="text-2xl font-bold text-white mb-2">Komparasi Aset</h3>
            <p className="text-slate-400 text-sm mb-8">Membandingkan {compareList.length} properti pilihan Anda</p>
            
            <div className="flex gap-6 overflow-x-auto pb-4 custom-scrollbar">
              {compareList.map(item => (
                <div key={`compare-${item.id}`} className="min-w-[280px] w-[280px] bg-[#0A0F24] rounded-2xl border border-white/5 overflow-hidden flex flex-col relative group">
                  <button onClick={() => handleToggleCompare(item)} className="absolute top-2 right-2 w-8 h-8 bg-black/50 hover:bg-red-500/80 rounded-full flex items-center justify-center text-white z-10 transition-colors backdrop-blur-sm">
                    <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
                  <img src={item.image} alt="" className="w-full h-32 object-cover opacity-80 group-hover:opacity-100 transition-opacity" />
                  <div className="p-5 flex flex-col gap-4">
                    <div>
                      <p className="font-bold text-white line-clamp-2 text-sm leading-tight mb-1">{item.title}</p>
                      <p className="text-xs text-slate-400 truncate">{item.location}</p>
                    </div>
                    
                    <div className="space-y-3 border-t border-white/5 pt-3">
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-slate-500">Taksiran AI</span>
                        <span className="text-sm font-bold text-success">{item.aiEstValue}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-slate-500">Harga Asli</span>
                        <span className="text-sm font-bold text-white">{item.actualPrice}</span>
                      </div>
                      <div className="flex justify-between items-center bg-success/10 p-2 rounded-lg">
                        <span className="text-xs text-success font-semibold">Potensi ROI</span>
                        <span className="text-sm font-extrabold text-success">{item.roi}</span>
                      </div>
                    </div>
                    
                    <div className="space-y-2 border-t border-white/5 pt-3">
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-slate-500">Luas Tanah</span>
                        <span className="text-xs text-white font-medium">{item.lt} m²</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-slate-500">Luas Bangunan</span>
                        <span className="text-xs text-white font-medium">{item.lb} m²</span>
                      </div>
                    </div>
                    
                    <a href={item.url} target="_blank" rel="noreferrer" className="mt-2 w-full py-2 bg-white/5 hover:bg-white/10 rounded-lg text-center text-xs font-semibold text-white transition-colors">Kunjungi Iklan</a>
                  </div>
                </div>
              ))}
              
              {compareList.length < 4 && (
                <div className="min-w-[280px] w-[280px] bg-[#0A0F24]/50 border border-white/5 border-dashed rounded-2xl flex flex-col items-center justify-center text-slate-500 p-6 opacity-50">
                   <svg className="w-12 h-12 mb-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
                   <p className="text-sm font-medium text-center">Pilih properti lain untuk dibandingkan</p>
                </div>
              )}
            </div>
          </div>
        </div>

      </main>

      {/* Floating Action Bar */}
      {!isLoading && !error && compareList.length > 0 && (
        <div className="fixed bottom-8 right-8 bg-[#1A2242] border border-white/10 rounded-2xl px-5 py-4 flex items-center gap-6 shadow-[0_10px_40px_rgba(0,0,0,0.8)] z-[100] animate-bounce-slow">
           <div className="flex items-center gap-4">
              <div className="flex -space-x-2">
                {compareList.slice(0,3).map((item, i) => (
                  <div key={i} className="w-10 h-10 rounded-full bg-slate-800 border-2 border-[#1A2242] z-20 overflow-hidden flex-shrink-0">
                    <img src={item.image} alt="" className="w-full h-full object-cover" />
                  </div>
                ))}
              </div>
              <div className="pr-2">
                <p className="text-sm font-bold text-white leading-tight">{compareList.length} Aset Dipilih</p>
                <p className="text-[10px] text-slate-400">Bandingkan ROI & Risiko</p>
              </div>
           </div>
           <button onClick={scrollToCompare} className="w-10 h-10 bg-primary hover:bg-primary/90 rounded-xl flex items-center justify-center text-white transition-all shadow-lg hover:shadow-primary/50 flex-shrink-0">
             <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" /></svg>
           </button>
        </div>
      )}

      <style jsx="true">{`
        @keyframes bounce-slow {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-8px); }
        }
        .animate-bounce-slow {
          animation: bounce-slow 3s infinite ease-in-out;
        }
        .custom-scrollbar::-webkit-scrollbar {
          height: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255,255,255,0.02);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255,255,255,0.1);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(255,255,255,0.2);
        }
      `}</style>
    </div>
  );
}
