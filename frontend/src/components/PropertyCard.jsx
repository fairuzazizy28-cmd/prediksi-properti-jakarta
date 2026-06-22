import React from 'react';

export default function PropertyCard({ property }) {
  if (!property) return null;

  const formatRupiah = (number) => 
    new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(number);

  // Generate a distinct dummy image pattern based on the ID or Harga
  const seed = (property.Harga || 0) % 5;
  const gradients = [
    'from-indigo-500 to-purple-500',
    'from-blue-500 to-cyan-500',
    'from-emerald-500 to-teal-500',
    'from-rose-500 to-pink-500',
    'from-amber-500 to-orange-500'
  ];
  const bgClass = gradients[seed];

  return (
    <div className="bg-[#131A32] border border-white/10 rounded-2xl overflow-hidden hover:shadow-[0_0_20px_rgba(46,91,255,0.3)] transition-all group flex flex-col h-full cursor-pointer">
      
      {/* House Image Placeholder */}
      <div className={`h-40 w-full bg-gradient-to-br ${bgClass} relative overflow-hidden`}>
        <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-all"></div>
        {/* Abstract house icon overlay */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-30">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="white" className="drop-shadow-lg">
            <path d="M12 3L2 12h3v8h14v-8h3L12 3zm-2 15H7v-6h3v6zm6 0h-3v-6h3v6z" />
          </svg>
        </div>
        
        {/* Location Badge */}
        <div className="absolute top-3 left-3 bg-black/60 backdrop-blur-sm px-3 py-1 rounded-full border border-white/10">
          <span className="text-[10px] font-bold text-white uppercase tracking-wider">{property.Kota}</span>
        </div>
      </div>

      <div className="p-5 flex flex-col flex-grow">
        <h3 className="text-xl font-extrabold text-primary mb-1">
          {formatRupiah(property.Harga)}
        </h3>
        <p className="text-sm text-slate-400 mb-4 flex items-center gap-1">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
          {property['Kecamatan/Kawasan']}
        </p>

        <div className="grid grid-cols-2 gap-3 mt-auto pt-4 border-t border-white/5 mb-4">
          <div className="flex items-center gap-2">
             <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                <span className="text-sm">🛏️</span>
             </div>
             <div>
                <p className="text-[10px] text-slate-500 uppercase font-bold">K. Tidur</p>
                <p className="text-sm text-white font-bold">{property.Kamar_Tidur_Utama || 0}</p>
             </div>
          </div>
          
          <div className="flex items-center gap-2">
             <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                <span className="text-sm">🚿</span>
             </div>
             <div>
                <p className="text-[10px] text-slate-500 uppercase font-bold">K. Mandi</p>
                <p className="text-sm text-white font-bold">{property.Kamar_Mandi_Utama || 0}</p>
             </div>
          </div>

          <div className="flex items-center gap-2">
             <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                <span className="text-sm">📐</span>
             </div>
             <div>
                <p className="text-[10px] text-slate-500 uppercase font-bold">L. Tanah</p>
                <p className="text-sm text-white font-bold">{property.Luas_Tanah || 0} m²</p>
             </div>
          </div>

          <div className="flex items-center gap-2">
             <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                <span className="text-sm">🏠</span>
             </div>
             <div>
                <p className="text-[10px] text-slate-500 uppercase font-bold">L. Bangunan</p>
                <p className="text-sm text-white font-bold">{property.Luas_Bangunan || 0} m²</p>
             </div>
          </div>
        </div>

        {property.URL_ID && (
          <a 
            href={property.URL_ID} 
            target="_blank" 
            rel="noopener noreferrer"
            className="w-full py-2.5 rounded-xl bg-primary/10 hover:bg-primary/20 border border-primary/30 text-primary font-bold text-sm flex items-center justify-center gap-2 transition-colors"
          >
            Lihat di Rumah123
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          </a>
        )}

      </div>
    </div>
  );
}
