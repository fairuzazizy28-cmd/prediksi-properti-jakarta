import { useState } from 'react';
import Pagination from '../components/Pagination';

const KECAMATAN_BY_KOTA = {
  "Jakarta Barat": ["Alfa Indah", "Angke", "Bandara", "Bojong Indah", "Cengkareng", "Cengkareng Barat", "Central Park", "Citra Garden", "Daan Mogot", "Duri Kepa", "Duri Kosambi", "Duri Pulo", "Duta Garden", "Gelong", "Gelong Baru", "Green Lake City", "Green Mansion", "Green Ville", "Green garden", "Grogol", "Grogol Petamburan", "Intercon", "Jalan Panjang", "Jelambar", "Jembatan Besi", "Jembatan Dua", "Jembatan Lima", "Joglo", "Kalideres", "Kamal", "Kapuk Kamal", "Karang Mulia", "Kav DKI", "Kebon Jeruk", "Kedoya", "Kedoya Baru", "Kedoya Selatan", "Kedoya Utara", "Kelapa Dua", "Kemanggisan", "Kembangan", "Kembangan Baru", "Kembangan Selatan", "Kepa Duri", "Kota Bambu Selatan", "Kota Bambu Utara", "Mangga Besar", "Mangga Dua", "Meruya", "Metland Puri", "Metro permata", "Mutiara Kedoya", "Palmerah", "Pegadungan", "Permata Buana", "Pesanggrahan", "Pinangsia", "Pos Pengumben", "Puri Indah", "Puri Mansion", "Puri Media", "Rawa Belong", "Rawa Buaya", "Roa Malaka", "S Parman", "Semanan", "Slipi", "Srengseng", "Sunrise Garden", "Taman Anggrek", "Taman Cosmos", "Taman Kencana", "Taman Kota", "Taman Meruya", "Taman Palem", "Taman Ratu", "Taman Surya", "Tamansari", "Tambora", "Tanjung Duren", "Tanjung Duren Selatan", "Tanjung Duren Utara", "Tanjung Gedong", "Tawakal", "Tomang", "Tubagus Angke", "Villa Meruya"],
  "Jakarta Pusat": ["Batu Ceper", "Batutulis", "Bendungan Hilir", "Bungur", "Cempaka Mas", "Cempaka Putih", "Cideng", "Cikini", "Gajah Mada", "Gambir", "Glodok", "Gondangdia", "Gunung Sahari", "Harmoni", "Hasyim Ashari", "Hayam Wuruk", "Johar Baru", "Karang Anyar", "Karet Tengsin", "Kartini", "Kebon Kacang", "Kebon Melati", "Kebon Sirih", "Kemayoran", "Kramat", "Menteng", "Menteng Atas", "Pangeran Jayakarta", "Pasar Baru", "Pegangsaan", "Pejompongan", "Percetakan Negara", "Petojo", "Roxy", "Salemba", "Sawah Besar", "Senayan", "Senen", "Sumur Batu", "Tambak Pegangsaan", "Tanah Abang", "Thamrin"],
  "Jakarta Selatan": ["Ampera", "Antasari", "Bangka", "Bintaro", "Blok M", "Blok S", "Bukit Duri", "CBD", "Casablanca", "Ciganjur", "Cikoko", "Cilandak", "Cinere", "Cipedak", "Cipete", "Cipulir", "Cirendeu", "Duren Tiga", "Fatmawati", "Gandaria", "Gatot Subroto", "Graha Bintaro", "Gudang Peluru", "Guntur", "Jagakarsa", "Jati Padang", "Jeruk Purut", "Kalibata", "Kapten Tendean", "Karet", "Kebagusan", "Kebayoran Baru", "Kebayoran Lama", "Kemandoran", "Kemang", "Kuningan", "Lebak Bulus", "Lenteng Agung", "MT Haryono", "Mampang", "Mampang Prapatan", "Manggarai", "Mega Kuningan", "Menteng Dalam", "Pakubuwono", "Pancoran", "Panglima Polim", "Pasar Minggu", "Patal Senayan", "Pejaten", "Pejaten Timur", "Pengadegan", "Permata Hijau", "Pesanggrahan", "Petukangan", "Pondok Indah", "Pondok Jaya", "Pondok Karya", "Pondok Labu", "Pondok Pinang", "Praja Dalam", "Prapanca", "Prof. Dr. Satrio", "Radio Dalam", "Ragunan", "Rempoa Ciputat Timur", "SCBD", "Saharjo", "Sektor 1 - Bintaro", "Sektor 2 - Bintaro", "Sektor 3 - Bintaro", "Sektor 3A-Bintaro", "Sektor 4 - Bintaro", "Sektor 5-Bintaro", "Sektor 6-Bintaro", "Sektor 8-Bintaro", "Senayan", "Senopati", "Setiabudi", "Simprug", "Simprug Garden", "Sinabung", "Sudirman", "Supomo", "TB Simatupang", "Tanah Kusir", "Tanjung Barat", "Tebet", "Terogong", "Ulujami", "Veteran", "Warung Buncit", "Wijaya", "patra kuningan"],
  "Jakarta Timur": ["Bambu Apus", "Buaran", "Cakung", "Cawang", "Cibubur", "Cijantung", "Cilangkap", "Cililitan", "Cipayung", "Cipinang", "Cipinang Melayu", "Ciracas", "Citra Grand", "Condet", "Dewi Sartika", "Duren Sawit", "Halim Perdana Kusuma", "Jakarta Garden City", "Jati Cempaka", "Jatinegara", "Jatiwaringin", "Kalimalang", "Kalisari", "Kampung Ambon", "Kampung Rambutan", "Kayu Jati", "Kayu Putih", "Klender", "Kota Wisata", "Kramat Jati", "Legenda Wisata", "Lubang Buaya", "Makasar", "Matraman", "Metland Menteng", "Otista", "Pasar Rebo", "Penggilingan", "Pinang Ranti", "Pisangan Lama", "Pondok Bambu", "Pondok Gede", "Pondok Kelapa", "Pondok Kopi", "Pondok Ranggon", "Pulo Asem", "Pulo Gadung", "Pulogebang", "Pulomas", "Raffles Hills", "Rawamangun", "Setu", "Taman Mini", "Utan Kayu"],
  "Jakarta Utara": ["Ancol", "Bandengan", "Cilincing", "Dadap", "Ebony Island", "Golf Island", "Jembatan Tiga", "Kamal", "Kapuk", "Kapuk Muara", "Kelapa Gading", "Koja", "Marunda", "Muara Karang", "Pademangan", "Pantai Indah Kapuk", "Pantai Indah Kapuk 2", "Pantai Mutiara", "Pegangsaan", "Penjaringan", "Pluit", "Plumpang", "Rawa Badak", "Rorotan", "Semper", "Sunter", "Taman Grisenda", "Tanjung Priok", "Teluk Gong"]
};

function Prediction() {
  const [formData, setFormData] = useState({
    kota: 'Jakarta Selatan',
    kecamatan: 'Bintaro',
    sertifikat: 'SHM',
    luas_tanah: 80,
    luas_bangunan: 120,
    kt_utama: 3,
    km_utama: 2,
    kt_art: 1,
    km_art: 1,
    garasi: 1,
    carport: 1,
    fasilitas_terpilih: ['Siap Huni', 'Bebas Banjir']
  });

  const [prediction, setPrediction] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [dp, setDp] = useState(20);
  const [tenor, setTenor] = useState(20);
  const [bunga, setBunga] = useState(5.5);
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => {
      const newState = {
        ...prev,
        [name]: name.includes('luas') || name.includes('kt') || name.includes('km') || name.includes('garasi') || name.includes('carport') 
                ? (value === '' ? '' : Number(value)) : value
      };
      // Auto update kecamatan to the first option if kota changes
      if (name === 'kota') {
        newState.kecamatan = KECAMATAN_BY_KOTA[value] ? KECAMATAN_BY_KOTA[value][0] : '';
      }
      return newState;
    });
  };

  const handleFasilitasChange = (fasilitas) => {
    setFormData(prev => {
      const isSelected = prev.fasilitas_terpilih.includes(fasilitas);
      if (isSelected) {
        return { ...prev, fasilitas_terpilih: prev.fasilitas_terpilih.filter(f => f !== fasilitas) };
      } else {
        return { ...prev, fasilitas_terpilih: [...prev.fasilitas_terpilih, fasilitas] };
      }
    });
  };

  const fetchPredictionAndRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch Prediction
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!response.ok) throw new Error('Gagal menghubungi AI Model');
      const data = await response.json();
      setPrediction(data);

      // 2. Fetch Recommendations
      const recRes = await fetch(`${API_BASE_URL}/api/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          kota: formData.kota,
          kecamatan: formData.kecamatan,
          luas_tanah: formData.luas_tanah,
          luas_bangunan: formData.luas_bangunan,
          kt_utama: formData.kt_utama,
          km_utama: formData.km_utama,
          carport: formData.carport,
          fasilitas_terpilih: formData.fasilitas_terpilih,
          harga_prediksi: data.harga_prediksi,
          top_n: 500
        })
      });
      if (recRes.ok) {
        const recData = await recRes.json();
        setRecommendations(recData.rekomendasi || []);
        setCurrentPage(1);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const harga_prediksi = prediction ? prediction.harga_prediksi : 0;
  const L = harga_prediksi * (1 - dp / 100);
  const r = (bunga / 12) / 100;
  const n = tenor * 12;
  const M = harga_prediksi > 0 ? (L * (r * Math.pow(1 + r, n))) / (Math.pow(1 + r, n) - 1) : 0;
  const cicilanPerBulan = M * 1.1; 
  
  const bunga_bulan = L * r;
  const pokok_bulan = M - bunga_bulan;
  const pct_pokok = cicilanPerBulan > 0 ? (pokok_bulan / cicilanPerBulan) * 100 : 0;
  const pct_bunga = cicilanPerBulan > 0 ? (bunga_bulan / cicilanPerBulan) * 100 : 0;

  const formatRupiah = (number) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(number);
  const formatShort = (number) => {
    if (number >= 1e9) return `Rp ${parseFloat((number / 1e9).toFixed(2))}M`;
    if (number >= 1e6) return `Rp ${parseFloat((number / 1e6).toFixed(2))}Jt`;
    return `Rp ${number}`;
  };

  // Menggunakan gambar premium dari mockup HTML pengguna
  const getDummyImage = (index) => {
    const images = [
      "https://lh3.googleusercontent.com/aida-public/AB6AXuAtPLwLx1iuykG_1QE70wbp6S3fIwFZL26OkcwDcgbM08Ppiv4nh7Qnt5O0forhABM_KE0YCoBnyHEPrA9lxV-M2ToRAJ_BBUMLOvRdcIgy_oajK_W-xW6wmFR8oSsGwNlpDXjfCgcexHGGN_9BxmX5gsIFPAGZ1OIpiqmDZU94rjAyW_iIK522BSJsZVekEIJAYZVm66EkiJgkmSLrOtJnhZS0TTdWw3uM51bH9a0ur-z7JpKTX9dPuDyE9eObR2o6iPzxBxTonFdG",
      "https://lh3.googleusercontent.com/aida-public/AB6AXuCYcw3zZj1jcK7oADvDjI3FmmhA66ogtsa9hplTFzppxte8Z23CZBsLNLVnHowUqw9U-sw3q7nV741lE17BjR7GuyxxAPqxfPbslADdPNVjPKoGljsOYOSVrhsdtzTWiP-MYd8SvV3z_lJkWa7hingXP7-M-URt5qrY7ZlzU-D_yJ-KyD2gWeJaDBbwGYpe3DDLN7A-nyuBjf0pJWMCV-8THmn1XBfTSDunHEjEX1fcOK84QP_J762SdUFI6fFm1W-fLx3O2EYTDMss",
      "https://lh3.googleusercontent.com/aida-public/AB6AXuBoyfRmZELcWOcZxnEscKCLuNjcSCyH1AxA7lYLk5ViWjew8QHGmiO7PUsgLegWEp_7RycbGMymGxsTcdbH15ux_ebAnNF5QEZBql-9vpstMhiE1AebZvWWtHiYSuP6jaQZPHYr-dSyhKKmYIztIXtZMb9Mx87znGgbRNpEDpYTChbjbOG-H7Y5Gvblnvp7zBRGUzWL5LEnaVUNG3SJAxNfR6SsRQOMSn-_MmRwnKN_IdSzBxn-KYIvYlckW83AnoblGURpBaotAwS9",
      "https://lh3.googleusercontent.com/aida-public/AB6AXuAUc7o9AieseQat6mGRWyiEKQP9_6ipQg9CLuIWNde9A426ZXyNZkgo9Oi7HWo7BopSHOJe-89fTJb1lzP9a8I4mIShBOiiI3bl0mDvMJdqdbP2tNZ_JG6CmuN1hxRudf3P48bClWpYrpcv_WAMHlZRxdM-Rcq_j4IloVQv_OW3xHjyi8PlD4vfMBHc-ycaxi0DIt_QFSG7_MgxvfHSBxTe787YRYTcQKUzoAN2qIClztRq-IFoosO6tJwifHKR-BCXE0kVqNSg8XoW"
    ];
    return images[index % images.length];
  };

  return (
    <div className="flex flex-col">
      <main className="flex-grow max-w-[1440px] mx-auto w-full px-container-padding py-6">
        
        <div className="grid grid-cols-12 gap-gutter mt-8">
          <div className="col-span-12 lg:col-span-4">
            <div className="bg-[#131A32] border border-white/5 p-6 rounded-[24px]">
              <h2 className="text-xl font-bold mb-6 text-white">Spesifikasi Properti</h2>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Kota</label>
                    <select name="kota" value={formData.kota} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white focus:outline-none focus:border-primary transition-colors">
                      <option value="Jakarta Selatan">Jakarta Selatan</option>
                      <option value="Jakarta Pusat">Jakarta Pusat</option>
                      <option value="Jakarta Barat">Jakarta Barat</option>
                      <option value="Jakarta Timur">Jakarta Timur</option>
                      <option value="Jakarta Utara">Jakarta Utara</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Sertifikat</label>
                    <select name="sertifikat" value={formData.sertifikat} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white focus:outline-none focus:border-primary transition-colors">
                      <option value="SHM">SHM</option>
                      <option value="HGB">HGB</option>
                      <option value="Lainnya">Lainnya</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Kecamatan</label>
                  <select name="kecamatan" value={formData.kecamatan} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white focus:outline-none focus:border-primary transition-colors">
                    {(KECAMATAN_BY_KOTA[formData.kota] || []).map(kec => (
                      <option key={kec} value={kec}>{kec}</option>
                    ))}
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Luas Tanah (m²)</label>
                    <input type="number" name="luas_tanah" value={formData.luas_tanah} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white focus:outline-none focus:border-primary" />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Luas Bangun (m²)</label>
                    <input type="number" name="luas_bangunan" value={formData.luas_bangunan} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white focus:outline-none focus:border-primary" />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">KT Utama</label>
                    <input type="number" name="kt_utama" value={formData.kt_utama} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white" />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">KM Utama</label>
                    <input type="number" name="km_utama" value={formData.km_utama} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white" />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">KT ART</label>
                    <input type="number" name="kt_art" value={formData.kt_art} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white" />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">KM ART</label>
                    <input type="number" name="km_art" value={formData.km_art} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white" />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Garasi</label>
                    <input type="number" name="garasi" value={formData.garasi} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white" />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Carport</label>
                    <input type="number" name="carport" value={formData.carport} onChange={handleInputChange} className="w-full bg-[#0A0F24] border border-white/10 rounded-xl px-4 py-3.5 text-sm font-semibold text-white" />
                  </div>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-3">Fasilitas Tambahan & Kata Kunci</label>
                  <div className="flex flex-wrap gap-2">
                    {[
                      'Siap Huni', 'Bebas Banjir', 'Komplek Perumahan', 
                      'Dekat Akses Transportasi', 'Dekat Sekolah', 
                      'Dekat Pusat Perbelanjaan', 'Dekat Fasilitas Kesehatan',
                      'Dekat Tempat Ibadah', 'Dekat Tempat Wisata', 'Dekat Landmark'
                    ].map((fas) => (
                      <button 
                        key={fas}
                        onClick={() => handleFasilitasChange(fas)}
                        className={`px-3 py-1 text-xs rounded-full border transition-all ${formData.fasilitas_terpilih.includes(fas) ? 'bg-primary text-white border-primary shadow-[0_0_10px_rgba(30,174,152,0.3)]' : 'border-white/10 text-slate-400 hover:border-primary/50'}`}
                      >
                        {formData.fasilitas_terpilih.includes(fas) && '✓ '} {fas}
                      </button>
                    ))}
                  </div>
                </div>
                <button 
                  onClick={fetchPredictionAndRecommendations} 
                  disabled={loading}
                  className={`w-full py-3 rounded-xl font-bold text-white mt-4 ${loading ? 'bg-gray-600' : 'gradient-button'}`}
                >
                  {loading ? 'Menganalisis...' : (
                    <div className="flex items-center justify-center gap-2">
                      <svg viewBox="0 0 24 24" fill="none" stroke="url(#btnIconGradient)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5 drop-shadow-[0_0_8px_rgba(196,181,253,0.8)]">
                        <defs>
                          <linearGradient id="btnIconGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#E9D5FF" />
                            <stop offset="100%" stopColor="#C084FC" />
                          </linearGradient>
                        </defs>
                        <circle cx="10" cy="10" r="7" />
                        <polyline points="6,12 10,8 13,11 19,4" />
                        <polyline points="15,4 19,4 19,8" />
                        <line x1="15" y1="15" x2="21" y2="21" />
                      </svg>
                      Analisis Harga AI
                    </div>
                  )}
                </button>
                {error && <p className="text-error text-sm mt-2 text-center">{error}</p>}
              </div>
            </div>
          </div>

          <div className="col-span-12 lg:col-span-8 grid grid-cols-12 gap-gutter">
            <div className="col-span-12 lg:col-span-12 bg-[#131A32] border border-white/5 rounded-[24px] p-8 flex flex-col items-center justify-center relative overflow-hidden">
               <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[300px] h-[300px] bg-primary/20 rounded-full blur-[100px] pointer-events-none"></div>

              <span className="font-bold text-[10px] text-primary tracking-widest uppercase mb-4 relative z-10">Hasil Kecerdasan Buatan</span>
              <h1 className="font-extrabold text-3xl text-white mb-4 relative z-10">Taksiran Harga Wajar</h1>
              
              {prediction ? (
                <>
                  <div className="drop-shadow-[0_0_15px_rgba(45,104,255,0.4)] text-5xl md:text-[64px] text-primary font-extrabold mb-8 text-center tracking-tight relative z-10">
                    {formatRupiah(harga_prediksi)}
                  </div>
                  <div className="grid grid-cols-2 gap-4 w-full max-w-lg relative z-10 mb-6">
                    <div className="bg-white/5 p-4 rounded-xl text-center">
                      <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Kisaran Bawah</p>
                      <p className="text-lg font-bold text-white">{formatRupiah(prediction.batas_bawah)}</p>
                    </div>
                    <div className="bg-white/5 p-4 rounded-xl text-center">
                      <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Kisaran Atas</p>
                      <p className="text-lg font-bold text-white">{formatRupiah(prediction.batas_atas)}</p>
                    </div>
                  </div>
                  
                  {/* Kepercayaan Model & MAPE */}
                  <div className="flex justify-center gap-4 relative z-10">
                    <div className="bg-[#0A0F24] border border-white/5 rounded-full px-4 py-3.5 text-sm font-semibold flex items-center gap-2">
                      <span className="text-slate-400 text-[10px] md:text-xs uppercase tracking-wider">Kepercayaan (R²)</span>
                      <span className="text-success font-bold text-sm">{(prediction.metrik.r2).toFixed(1)}%</span>
                    </div>
                    <div className="bg-[#0A0F24] border border-white/5 rounded-full px-4 py-3.5 text-sm font-semibold flex items-center gap-2">
                      <span className="text-slate-400 text-[10px] md:text-xs uppercase tracking-wider">Margin Nego (MAPE)</span>
                      <span className="text-warning font-bold text-sm">±{(prediction.metrik.mape).toFixed(1)}%</span>
                    </div>
                  </div>
                </>
              ) : (
                 <div className="text-center text-slate-400 py-12 relative z-10 flex flex-col items-center">
                  <div className="w-24 h-24 mb-6 rounded-3xl bg-[#0A0F24] flex items-center justify-center border border-white/5 shadow-[0_0_30px_rgba(30,174,152,0.15)] relative group">
                    <div className="absolute inset-0 bg-primary/20 rounded-3xl blur-xl group-hover:bg-primary/30 transition-all duration-500"></div>
                    <svg className="w-10 h-10 text-primary relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  </div>
                  <h3 className="text-xl text-white font-medium mb-2">Belum Ada Data</h3>
                  <p className="max-w-xs text-sm">Silakan sesuaikan spesifikasi properti di panel sebelah kiri, lalu klik tombol analisis untuk melihat taksiran harga wajar dari AI.</p>
                </div>
              )}
            </div>

            {prediction && (
              <div className="col-span-12 bg-[#131A32] border border-white/5 p-8 rounded-[32px] border-white/5">
                <div className="flex justify-between items-center mb-8">
                  <h2 className="font-headline-lg text-2xl">Kalkulator KPR Sederhana</h2>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between mb-2">
                        <label className="text-sm text-slate-400">Uang Muka (DP%)</label>
                        <span className="text-sm font-bold text-white">{dp}% ({formatShort(harga_prediksi * (dp/100))})</span>
                      </div>
                      <input type="range" min="5" max="50" step="5" value={dp} onChange={(e) => setDp(Number(e.target.value))} />
                    </div>
                    <div>
                      <div className="flex justify-between mb-2">
                        <label className="text-sm text-slate-400">Tenor Pinjaman</label>
                        <span className="text-sm font-bold text-white">{tenor} Tahun</span>
                      </div>
                      <input type="range" min="1" max="30" value={tenor} onChange={(e) => setTenor(Number(e.target.value))} />
                    </div>
                    <div>
                      <div className="flex justify-between mb-2">
                        <label className="text-sm text-slate-400">Suku Bunga (p.a)</label>
                        <span className="text-sm font-bold text-white">{bunga}%</span>
                      </div>
                      <input type="range" min="1" max="15" step="0.1" value={bunga} onChange={(e) => setBunga(Number(e.target.value))} />
                    </div>
                  </div>
                  
                  <div className="flex flex-col items-center justify-center">
                    <div className="relative w-48 h-48 mx-auto mb-6">
                      <svg viewBox="0 0 36 36" className="w-full h-full drop-shadow-[0_0_15px_rgba(30,174,152,0.3)]">
                        <path className="text-white/5" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3"></path>
                        <path className="text-orange-500" strokeDasharray="100, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3"></path>
                        <path className="text-primary" strokeDasharray={`${pct_pokok}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3"></path>
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-[10px] text-slate-400 uppercase tracking-widest mb-1">Estimasi Cicilan</span>
                        <div className="text-xl font-bold text-primary drop-shadow-[0_0_15px_rgba(45,104,255,0.4)]">{formatShort(cicilanPerBulan)}</div>
                        <span className="text-xs text-slate-400">/ bln</span>
                      </div>
                    </div>
                    <div className="flex gap-4 text-center">
                      <div className="flex items-center gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-primary"></div>
                        <span className="text-xs text-slate-400">Pokok ({pct_pokok.toFixed(0)}%)</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-tertiary"></div>
                        <span className="text-xs text-slate-400">Bunga ({pct_bunga.toFixed(0)}%)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Similar Properties Section */}
        {(recommendations.length > 0 || loading) && (
          <div className="mt-16 mb-8">
            <div className="flex justify-between items-end mb-6">
              <div>
                <h2 className="text-3xl font-extrabold text-white mb-2 flex items-center gap-4">
                  <svg className="w-8 h-8 text-[#8B5CF6] drop-shadow-[0_0_15px_rgba(139,92,246,0.5)] shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
                  </svg>
                  Rekomendasi Properti Serupa
                </h2>
                <p className="text-slate-400 font-medium ml-[48px]">Daftar properti di dataset yang paling mendekati spesifikasi Anda.</p>
              </div>
            </div>

            {loading ? (
              <div className="flex flex-col items-center justify-center py-24 bg-[#1A1F36]/50 rounded-[32px] border border-white/5 shadow-inner">
                 <svg className="animate-spin h-10 w-10 text-[#2E5BFF] mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                   <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                   <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                 </svg>
                 <p className="text-slate-300 font-medium tracking-wide">Sedang mencari properti terbaik...</p>
              </div>
            ) : (
              <>
                {/* Banner Logika Rekomendasi */}
                {(() => {
                  const exactKecamatan = recommendations.some(r => r['Kecamatan/Kawasan'] === formData.kecamatan);
                  const allHigher = recommendations.every(r => r.Harga > prediction.batas_atas);
                  const someLower = recommendations.some(r => r.Harga < prediction.batas_bawah);
                  
                  if (!exactKecamatan || allHigher) {
                    return (
                      <div className="mb-6 p-4 rounded-xl bg-warning/10 border border-warning/20 flex items-center gap-3">
                        <span className="text-warning text-xl">💡</span>
                        <p className="text-sm text-warning font-medium">Spesifikasi atau kisaran harga persis di kawasan pilihan Anda tidak tersedia. Menampilkan beberapa rekomendasi alternatif terdekat.</p>
                      </div>
                    );
                  } else if (someLower) {
                    return (
                      <div className="mb-6 p-4 rounded-xl bg-success/10 border border-success/20 flex items-center gap-3">
                        <span className="text-success text-xl">🎉</span>
                        <p className="text-sm text-success font-medium">Terdapat properti <b>Good Deal</b> yang harganya di bawah taksiran wajar pasar berdasarkan spesifikasi Anda!</p>
                      </div>
                    );
                  } else {
                    return (
                      <div className="mb-6 p-4 rounded-xl bg-primary/10 border border-primary/20 flex items-center gap-3">
                        <span className="text-primary text-xl">✅</span>
                        <p className="text-sm text-primary font-medium">Menampilkan rekomendasi properti yang paling sesuai dengan spesifikasi dan harga terdekat:</p>
                      </div>
                    );
                  }
                })()}

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-card-gap">
              {(() => {
                let relevantRecs = recommendations;
                if (recommendations.length > 0 && recommendations[0].Skor_Kemiripan > 0.8) {
                  relevantRecs = recommendations.slice(0, 10);
                }
                
                const itemsPerPage = 10;
                const totalPages = Math.ceil(relevantRecs.length / itemsPerPage);
                const paginatedRecs = relevantRecs.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
                
                return (
                  <>
                    {paginatedRecs.map((item, idx) => {
                      const isUndervalued = item.Harga < harga_prediksi;
                
                // Format Spesifikasi: Utama + Tambahan
                const ktStr = `${item.Kamar_Tidur_Utama || 0}${item.Kamar_Tidur_ART > 0 ? `+${item.Kamar_Tidur_ART}` : ''}`;
                const kmStr = `${item.Kamar_Mandi_Utama || 0}${item.Kamar_Mandi_ART > 0 ? `+${item.Kamar_Mandi_ART}` : ''}`;
                const garasiStr = `${item.Garasi_Utama || 0}${item.Carport > 0 ? `+${item.Carport}` : ''}`;

                // Ekstrak kata kunci yang bernilai 1
                const keywords = [];
                if (item.Fasilitas_Siap_Huni === 1) keywords.push('Siap Huni');
                if (item.Fasilitas_Bebas_Banjir === 1) keywords.push('Bebas Banjir');
                if (item.Fasilitas_Komplek_Perumahan === 1) keywords.push('Dalam Komplek');
                if (item.Fasilitas_Dekat_Akses_Transportasi === 1) keywords.push('Dekat Transportasi');
                if (item.Fasilitas_Dekat_Pusat_Perbelanjaan === 1) keywords.push('Dekat Mall');
                if (item.Fasilitas_Dekat_Sekolah === 1) keywords.push('Dekat Sekolah');
                if (item.Is_SHM === 1) keywords.push('SHM');
                
                return (
                  <div key={idx} className={`bg-[#1A1F36] rounded-[24px] overflow-hidden flex flex-col group transition-transform hover:-translate-y-2 border border-white/5 ${isUndervalued ? 'shadow-[0_8px_30px_rgba(57,255,20,0.15)]' : 'shadow-2xl'}`}>
                    {/* Top image */}
                    <div className="relative h-52 overflow-hidden bg-[#0A0F24]">
                      <img src={item.Image_URL || getDummyImage(idx)} alt="Property" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                      
                      {/* Good Deal Badge */}
                      {isUndervalued && (
                        <div className="absolute top-4 left-4 z-20">
                          <span className="px-3 py-1 bg-[#39FF14] text-[#0A0F24] font-bold text-[11px] rounded-md uppercase tracking-wide shadow-[0_0_15px_rgba(57,255,20,0.4)]">
                            Good Deal
                          </span>
                        </div>
                      )}
                    </div>
                    
                    <div className="flex flex-col flex-grow">
                      {/* Title & Location */}
                      <div className="px-5 pt-5 pb-2">
                        <h3 className="font-bold text-lg text-white line-clamp-1 mb-1">{item.Deskripsi || `Rumah di ${item['Kecamatan/Kawasan']}`}</h3>
                        <div className="flex items-center gap-1.5 text-slate-400">
                          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                          <span className="text-xs line-clamp-1">{item['Kecamatan/Kawasan']}, {item.Kota}</span>
                        </div>
                      </div>

                      {/* Price */}
                      <div className="px-5 pb-4">
                        <div className="text-[24px] font-extrabold text-primary tracking-tight drop-shadow-sm">{formatShort(item.Harga)}</div>
                      </div>

                      {/* Rooms - Minimalist Text */}
                      <div className="px-5 pb-5 flex justify-between items-center text-slate-300 border-b border-white/5">
                        <div className="flex items-center gap-2">
                          <svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M4 15v4"/><path d="M20 15v4"/><path d="M4 15H20V11C20 9 18 9 18 9H6C6 9 4 9 4 11V15Z"/><path d="M7 9V7C7 6 8 6 8 6h3C11 6 12 6 12 7V9"/><path d="M12 9V7C12 6 13 6 13 6h3C16 6 17 6 17 7V9"/>
                          </svg>
                          <span className="text-sm font-semibold">{ktStr}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M4 15c0 3 2 5 8 5s8-2 8-5V11H4V15Z"/><path d="M6 20v2"/><path d="M18 20v2"/><path d="M11 11V6C11 5 12 4 13 4h2C16 4 17 5 17 6v1"/><path d="M11 8h3"/>
                          </svg>
                          <span className="text-sm font-semibold">{kmStr}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M5 16h14c1 0 2-1 2-2v-3c0-1-1-2-2-2H5c-1 0-2 1-2 2v3C3 15 4 16 5 16Z"/><path d="M7 16v3"/><path d="M17 16v3"/><path d="M6 9l2-4h8l2 4"/><circle cx="8" cy="12" r="1"/><circle cx="16" cy="12" r="1"/><line x1="11" y1="12" x2="13" y2="12"/>
                          </svg>
                          <span className="text-sm font-semibold">{garasiStr}</span>
                        </div>
                      </div>

                      {/* LT / LB & Keywords */}
                      <div className="px-5 py-4 flex flex-col gap-4">
                        <div className="flex gap-5 text-xs font-semibold text-slate-400 uppercase tracking-wide">
                          <span>LT <span className="text-white text-sm ml-1">{item.Luas_Tanah}m²</span></span>
                          <span>LB <span className="text-white text-sm ml-1">{item.Luas_Bangunan}m²</span></span>
                        </div>
                        
                        <div className="flex flex-wrap gap-2">
                          {keywords.slice(0, 4).map(kw => (
                            <span key={kw} className="px-2.5 py-1 bg-white/10 text-white rounded-md text-[11px] font-medium whitespace-nowrap">
                              {kw}
                            </span>
                          ))}
                          {keywords.length > 4 && (
                            <span className="px-2.5 py-1 bg-white/5 text-slate-400 rounded-md text-[11px] font-medium whitespace-nowrap">
                              +{keywords.length - 4}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Link Rumah123 - Solid Blue */}
                      <div className="mt-auto px-5 pb-5">
                        <a href={item.URL_ID} target="_blank" rel="noreferrer" className="w-full flex items-center justify-center py-3 rounded-xl bg-[#2E5BFF] text-sm font-bold text-white hover:bg-[#1E3A8A] transition-colors duration-300">
                          Lihat Detail di rumah123
                        </a>
                      </div>
                    </div>
                  </div>
                );
              })}
              
              {totalPages > 1 && (
                <div className="col-span-full">
                  <Pagination 
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={setCurrentPage}
                  />
                </div>
              )}
              </>
              );
              })()}
            </div>
          </>
        )}
      </div>
        )}

      </main>
    </div>
  );
}

export default Prediction;
