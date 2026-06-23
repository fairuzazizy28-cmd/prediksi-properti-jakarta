import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker } from 'react-leaflet';
import L from 'leaflet';
import PropertyCard from '../components/PropertyCard';
import Pagination from '../components/Pagination';

export default function Affordability() {
  const [formData, setFormData] = useState({
    penghasilan: 25000000,
    dti: 30,
    dp: 150000000,
    bunga: 5.5,
    tenor: 20
  });

  const [kotaCounts, setKotaCounts] = useState({});
  const [kecamatanToKota, setKecamatanToKota] = useState({});
  const [recommendations, setRecommendations] = useState({});
  const [selectedKota, setSelectedKota] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  
  const [totalAffordable, setTotalAffordable] = useState(0);
  const [loading, setLoading] = useState(false);
  const [geoData, setGeoData] = useState(null);

  // Kalkulasi Finansial
  const cicilanMaks = formData.penghasilan * (formData.dti / 100);
  const r = (formData.bunga / 12) / 100;
  const n = formData.tenor * 12;
  const maxLoan = cicilanMaks > 0 && r > 0 ? (cicilanMaks * (Math.pow(1 + r, n) - 1)) / (r * Math.pow(1 + r, n)) : 0;
  const maxPrice = maxLoan + formData.dp;

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: Number(value) }));
  };

  const fetchHeatmap = async () => {
    setLoading(true);
    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE_URL}/api/affordability`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ max_harga: maxPrice })
      });
      if (response.ok) {
        const data = await response.json();
        const counts = data.kota_counts || {};
        setKotaCounts(counts);
        setKecamatanToKota(data.kecamatan_to_kota || {});
        setTotalAffordable(data.total_affordable);
        setRecommendations(data.recommendations || {});
        setCurrentPage(1);
        
        // Auto-select the city with highest count if nothing selected or current is 0
        if (Object.keys(counts).length > 0) {
          const highestKota = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
          if (!selectedKota || counts[selectedKota] === 0) {
            setSelectedKota(highestKota);
          }
        } else {
            setSelectedKota('All');
        }
      }
    } catch (err) {
      console.error("Gagal mengambil data heatmap:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Load NEW GeoJSON for 5 Jakarta Cities directly
    fetch('/jakarta-5-kota.geojson')
      .then(res => res.json())
      .then(data => setGeoData(data))
      .catch(err => console.error("Gagal memuat batas wilayah Jakarta:", err));
  }, []);

  // Debounce the API call so it doesn't spam while sliding
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchHeatmap();
    }, 500);
    return () => clearTimeout(timeoutId);
    // eslint-disable-next-line
  }, [formData]);

  const formatRupiah = (number) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(number);

  const getColor = (count) => {
    if (!count || count === 0) return 'transparent';
    if (count > 2000) return '#4ade80'; // Bright Green 400
    if (count > 1000) return '#22c55e'; // Green 500
    if (count > 500)  return '#16a34a'; // Green 600
    if (count > 200)  return '#15803d'; // Green 700
    if (count > 50)   return '#166534'; // Green 800
    return '#14532d'; // Dark Green 900
  };

  const geoJsonStyle = (feature) => {
    const kota = feature.properties.Kota;
    const count = kota ? kotaCounts[kota] : 0;
    const fillColor = getColor(count);
    const isSelected = selectedKota === kota || selectedKota === 'All';

    return {
      fillColor: fillColor,
      weight: isSelected ? 3 : 1.5,
      opacity: isSelected ? 1 : 0.4,
      color: isSelected ? '#ffffff' : '#1E293B', // Highlight border white if selected
      fillOpacity: isSelected ? (count > 0 ? 0.8 : 0.05) : (count > 0 ? 0.4 : 0.02)
    };
  };

  const onEachFeature = (feature, layer) => {
    layer.on({
      click: () => {
        // Toggle selection (if already selected, maybe unselect? Or just select)
        setSelectedKota(feature.properties.Kota);
        setCurrentPage(1);
      }
    });
  };

  const activeRecommendations = selectedKota && recommendations[selectedKota] ? recommendations[selectedKota] : recommendations['All'] || [];

  return (
    <div className="max-w-[1440px] mx-auto w-full px-container-padding py-6">
      
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold text-white mb-2">Peta Keterjangkauan Harga</h1>
        <p className="text-slate-400">Hitung batas maksimal properti yang dapat Anda beli, dan lihat zona persebarannya di Jakarta.</p>
      </div>

      <div className="grid grid-cols-12 gap-6 min-h-[600px] lg:min-h-[700px]">
        
        {/* Panel Kiri - Kalkulator */}
        <div className="col-span-12 lg:col-span-4 flex flex-col gap-6">
          
          <div className="bg-[#131A32] border border-white/5 p-6 rounded-[32px] shadow-lg">
            <h2 className="text-xl font-bold mb-6 text-white flex items-center gap-3">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="url(#financeGradient)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="drop-shadow-[0_0_8px_rgba(168,85,247,0.5)] shrink-0">
                <defs>
                  <linearGradient id="financeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#E9D5FF" />
                    <stop offset="100%" stopColor="#A855F7" />
                  </linearGradient>
                </defs>
                <path d="M10 6V3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v13" />
                <rect x="2" y="6" width="11" height="16" rx="2" fill="#131A32" />
                <rect x="4" y="8" width="7" height="3" rx="0.5" />
                <path d="M4.5 14h1.5 M7.5 14h1.5 M10.5 14h1.5" />
                <path d="M4.5 17h1.5 M7.5 17h1.5 M10.5 17h1.5" />
                <path d="M4.5 20h1.5 M7.5 20h1.5 M10.5 20h1.5" />
                <circle cx="17" cy="17" r="6" fill="#131A32" />
                <path d="M17 13v8" />
                <path d="M19 14.5h-3.75a1.75 1.75 0 0 0 0 3.5h2.5a1.75 1.75 0 0 1 0 3.5H15" />
              </svg>
              Simulasi Keuangan
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3 flex justify-between">
                  <span>Penghasilan Bulanan</span>
                  <span className="text-white">{formatRupiah(formData.penghasilan)}</span>
                </label>
                <input type="range" name="penghasilan" min="5000000" max="100000000" step="1000000" value={formData.penghasilan} onChange={handleInputChange} />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3 flex justify-between">
                  <span>Batas Cicilan (DTI)</span>
                  <span className="text-white">{formData.dti}%</span>
                </label>
                <input type="range" name="dti" min="10" max="80" step="5" value={formData.dti} onChange={handleInputChange} />
                <p className="text-[10px] text-slate-500 mt-2 text-right">Maks cicilan: {formatRupiah(cicilanMaks)}</p>
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3 flex justify-between">
                  <span>Dana Tunai (DP)</span>
                  <span className="text-white">{formatRupiah(formData.dp)}</span>
                </label>
                <input type="range" name="dp" min="0" max="2000000000" step="50000000" value={formData.dp} onChange={handleInputChange} />
              </div>

              <div className="grid grid-cols-2 gap-4 pt-2">
                <div>
                  <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Suku Bunga (%)</label>
                  <input type="number" name="bunga" value={formData.bunga} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white focus:border-primary focus:outline-none" />
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Tenor (Tahun)</label>
                  <input type="number" name="tenor" value={formData.tenor} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white focus:border-primary focus:outline-none" />
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-[#2E5BFF]/20 to-[#8B5CF6]/20 border border-primary/30 p-8 rounded-[32px] text-center flex-grow flex flex-col justify-center relative overflow-hidden shadow-[0_0_30px_rgba(46,91,255,0.1)]">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-40 h-40 bg-primary/40 rounded-full blur-[60px] pointer-events-none"></div>
            
            <p className="text-[10px] font-bold text-primary tracking-widest uppercase mb-2 relative z-10">Batas Harga Maksimal</p>
            <h3 className="text-4xl lg:text-[40px] font-extrabold text-white mb-6 drop-shadow-[0_0_15px_rgba(139,92,246,0.3)] relative z-10 leading-tight">
              {formatRupiah(maxPrice)}
            </h3>
            
            <div className="bg-[#0A0F24]/50 backdrop-blur-sm border border-white/10 rounded-2xl p-4 mt-auto relative z-10">
              <p className="text-xs text-slate-300 font-medium mb-1">Ditemukan</p>
              <p className="text-2xl font-bold text-success">{totalAffordable} <span className="text-sm font-medium text-slate-400">Properti</span></p>
            </div>
          </div>

        </div>

        {/* Panel Kanan - Map Heatmap */}
        <div className="col-span-12 lg:col-span-8 relative rounded-[32px] overflow-hidden border border-white/10 shadow-2xl min-h-[400px]">
          {loading && (
            <div className="absolute inset-0 z-[1000] bg-[#0A0F24]/60 backdrop-blur-sm flex items-center justify-center">
              <div className="flex flex-col items-center">
                <svg className="animate-spin h-10 w-10 text-primary mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span className="text-sm font-semibold text-white tracking-widest uppercase">Menganalisa Titik Panas...</span>
              </div>
            </div>
          )}
          
          <MapContainer 
            center={[-6.200000, 106.816666]} // Center Jakarta
            zoom={11} 
            minZoom={10}
            maxBounds={[
              [-6.5, 106.5], // Koordinat Barat Daya (Tangerang/Depok border)
              [-5.9, 107.1]  // Koordinat Timur Laut (Bekasi border)
            ]}
            scrollWheelZoom={true}
            style={{ height: '100%', width: '100%', background: '#0A0F24' }}
            zoomControl={false}
          >
            {/* Dark theme Map Tiles (CartoDB Dark Matter) */}
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />
            
            {/* GeoJSON Borders for Jakarta Administratif (Choropleth Mode) */}
            {geoData && (
              <>
                <GeoJSON 
                  data={geoData} 
                  style={geoJsonStyle}
                  onEachFeature={onEachFeature}
                />
                
                {/* Text Labels for each Kota using Centroids */}
                {geoData.features.map(f => (
                  <Marker 
                    key={f.properties.Kota}
                    position={[f.properties.centroid_lat, f.properties.centroid_lng]}
                    icon={L.divIcon({
                      className: 'bg-transparent border-none',
                      html: `<div style="color: white; text-shadow: 0px 2px 4px rgba(0,0,0,0.8), 0px 0px 10px rgba(0,0,0,0.9); font-weight: 800; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; text-align: center; width: 120px; margin-left: -60px; margin-top: -10px;">${f.properties.Kota}<br/><span style="color: #4ade80; font-size: 14px;">${kotaCounts[f.properties.Kota] || 0} Unit</span></div>`,
                      iconSize: [0, 0]
                    })}
                    eventHandlers={{ click: () => { setSelectedKota(f.properties.Kota); setCurrentPage(1); } }}
                  />
                ))}
              </>
            )}
            
          </MapContainer>
          
          {/* Legend Overlay */}
          <div className="absolute bottom-6 left-6 z-[400] bg-[#131A32]/90 backdrop-blur-md border border-white/10 p-4 rounded-2xl shadow-xl">
            <h4 className="text-[10px] font-bold text-white tracking-widest uppercase mb-3">Tingkat Ketersediaan (Per Kota)</h4>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Rendah</span>
              <div className="w-32 h-2 rounded-full bg-gradient-to-r from-[#14532d] via-[#16a34a] to-[#4ade80]"></div>
              <span className="text-xs text-slate-400">Tinggi</span>
            </div>
          </div>

        </div>

      </div>

      {/* Rekomendasi Properti Horizontal Scroll */}
      <div className="mt-8 mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <span className="text-primary text-3xl">⭐</span> 
            Top Rekomendasi di {selectedKota === 'All' ? 'Seluruh Jakarta' : selectedKota}
          </h2>
          <button 
            onClick={() => { setSelectedKota('All'); setCurrentPage(1); }}
            className="text-sm font-bold text-white bg-white/10 hover:bg-white/20 px-5 py-2.5 rounded-full border border-white/20 transition-all hover:scale-105 hover:shadow-[0_0_15px_rgba(255,255,255,0.1)] flex items-center gap-2"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            Tampilkan Semua Wilayah
          </button>
        </div>
        
        {activeRecommendations.length > 0 ? (
          <div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
              {(() => {
                const itemsPerPage = 10;
                const paginatedRecs = activeRecommendations.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
                return paginatedRecs.map((prop, idx) => (
                  <div key={idx} className="w-full">
                    <PropertyCard property={prop} />
                  </div>
                ));
              })()}
            </div>
            
            {activeRecommendations.length > 0 && Math.ceil(activeRecommendations.length / 10) > 1 && (
              <div className="mt-8">
                <Pagination 
                  currentPage={currentPage}
                  totalPages={Math.ceil(activeRecommendations.length / 10)}
                  onPageChange={setCurrentPage}
                />
              </div>
            )}
          </div>
        ) : (
          <div className="w-full py-12 flex items-center justify-center border border-white/5 bg-white/5 rounded-2xl">
            <p className="text-slate-400">Tidak ada properti yang memenuhi kriteria batas harga Anda.</p>
          </div>
        )}
      </div>

    </div>
  );
}
