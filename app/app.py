"""
app.py — Dashboard Prediksi Harga & Rekomendasi Properti Jakarta
================================================================
Jalankan dengan:
  venv\Scripts\Activate.ps1
  streamlit run app/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import textwrap
from bs4 import BeautifulSoup

# =====================================================================
# KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="JKT PropTech | Prediksi Harga AI",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk mempercantik Sidebar dan elemen Native lainnya
st.markdown("""
    <style>
    /* Styling Sidebar Navigation agar lebih elegan */
    [data-testid="stSidebarNavItems"] {
        padding-top: 0.5rem;
    }
    .stRadio [role="radiogroup"] {
        gap: 0 !important;
    }
    .stRadio [role="radiogroup"] > label {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 4px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
        background-color: transparent;
    }
    .stRadio [role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.05);
    }
    
    /* Sembunyikan bulatan asli radio button untuk kesan modern/links */
    .stRadio [role="radiogroup"] > label > div:first-child {
        display: none;
    }
    
    /* Mengatur padding bagian utama agar lebih pas */
    .block-container {
        padding-top: 3rem !important;
        max-width: 1300px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 1. LOAD MODEL & DATABASE
# =====================================================================
@st.cache_resource
def load_model():
    with open('models/model_lgbm_properti.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_database():
    return pd.read_csv('data/processed/dataset_properti_jakarta_master_fe2.csv')

paket = load_model()
model          = paket['model']
median_lt_kec  = paket['median_lt_per_kec']
median_lb_kec  = paket['median_lb_per_kec']
kota_ke_kec    = paket['kota_ke_kecamatan']
semua_kecamatan = paket['semua_kecamatan']
semua_kota     = paket['semua_kota']
all_features   = paket['semua_fitur']
metrik         = paket['metrik']

df_master = load_database()

# =====================================================================
# 2. DAFTAR KATA KUNCI / FASILITAS
# =====================================================================
DAFTAR_FASILITAS = {
    'Siap Huni':                   'Fasilitas_Siap_Huni',
    'Bebas Banjir':                'Fasilitas_Bebas_Banjir',
    'Komplek Perumahan':           'Fasilitas_Komplek_Perumahan',
    'Dekat Akses Transportasi':    'Fasilitas_Dekat_Akses_Transportasi',
    'Dekat Sekolah':               'Fasilitas_Dekat_Sekolah',
    'Dekat Pusat Perbelanjaan':    'Fasilitas_Dekat_Pusat_Perbelanjaan',
    'Dekat Fasilitas Kesehatan':   'Fasilitas_Dekat_Fasilitas_Kesehatan',
    'Dekat Tempat Ibadah':         'Fasilitas_Dekat_Tempat_Ibadah',
    'Dekat Tempat Wisata':         'Fasilitas_Dekat_Tempat_Wisata',
    'Dekat Landmark':              'Fasilitas_Dekat_Landmark',
}

# =====================================================================
# 3. HELPER FUNCTIONS (KPR, FORMATTING, SCRAPING)
# =====================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def ambil_foto_rumah123(url):
    """Mengambil link foto utama (og:image) secara live dari halaman Rumah123."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "id-ID,id;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_og = soup.find("meta", property="og:image")
            if meta_og and meta_og.get("content"):
                return meta_og["content"]
    except Exception:
        pass
    return None

def dapatkan_rekomendasi(input_user, harga_prediksi, df_master, top_n=4):
    """Mencari properti nyata terdekat dari database berdasarkan input user."""
    df_lokasi = df_master[df_master['Kecamatan/Kawasan'] == input_user['Kecamatan/Kawasan']]
    if len(df_lokasi) < 3:
        df_lokasi = df_master[df_master['Kota'] == input_user['Kota']]
    if len(df_lokasi) == 0:
        return pd.DataFrame()

    df_lokasi = df_lokasi.copy()
    selisih_lt = np.abs(df_lokasi['Luas_Tanah'] - input_user['Luas_Tanah']) / max(input_user['Luas_Tanah'], 1)
    selisih_lb = np.abs(df_lokasi['Luas_Bangunan'] - input_user['Luas_Bangunan']) / max(input_user['Luas_Bangunan'], 1)
    selisih_harga = np.abs(df_lokasi['Harga'] - harga_prediksi) / max(harga_prediksi, 1)

    df_lokasi['Skor_Kemiripan'] = (selisih_lt * 0.3) + (selisih_lb * 0.3) + (selisih_harga * 0.4)
    rekomendasi = df_lokasi.sort_values(by='Skor_Kemiripan').head(top_n).reset_index(drop=True)
    return rekomendasi

def bangun_input_prediksi(kota, kecamatan, sertifikat, luas_tanah, luas_bangunan,
                           kt_utama, kt_art, km_utama, km_art,
                           garasi, carport, fasilitas_terpilih):
    """Membangun DataFrame input dengan semua fitur turunan untuk model LGBM."""
    rasio_lb_lt = luas_bangunan / luas_tanah if luas_tanah > 0 else 1.0
    kapasitas_parkir = garasi + carport
    rasio_kt_km = kt_utama / km_utama if km_utama > 0 else kt_utama
    ada_art = 1 if (kt_art > 0 or km_art > 0) else 0
    luas_per_kamar = luas_bangunan / (kt_utama + 1)
    is_shm = 1 if sertifikat == 'SHM' else 0

    med_lt = median_lt_kec.get(kecamatan, luas_tanah)
    med_lb = median_lb_kec.get(kecamatan, luas_bangunan)
    lt_vs_median = luas_tanah / med_lt if med_lt > 0 else 1.0
    lb_vs_median = luas_bangunan / med_lb if med_lb > 0 else 1.0

    fitur_biner = {}
    for nama_display, nama_kolom in DAFTAR_FASILITAS.items():
        fitur_biner[nama_kolom] = 1 if nama_display in fasilitas_terpilih else 0

    data = {
        'Luas_Tanah': luas_tanah,
        'Luas_Bangunan': luas_bangunan,
        'Rasio_LB_LT': rasio_lb_lt,
        'Luas_per_Kamar': luas_per_kamar,
        'LT_vs_Median_Kecamatan': lt_vs_median,
        'LB_vs_Median_Kecamatan': lb_vs_median,
        'Kamar_Tidur_Utama': kt_utama,
        'Kamar_Tidur_ART': kt_art,
        'Kamar_Mandi_Utama': km_utama,
        'Kamar_Mandi_ART': km_art,
        'Garasi_Utama': garasi,
        'Carport': carport,
        'Kapasitas_Parkir': kapasitas_parkir,
        'Rasio_KT_KM': rasio_kt_km,
        'Kota': kota,
        'Kecamatan/Kawasan': kecamatan,
        'Sertifikat': sertifikat,
        'Is_SHM': is_shm,
        'Ada_ART_Room': ada_art,
        **fitur_biner
    }
    df_input = pd.DataFrame([data])
    df_input = df_input[all_features]

    for col in ['Kota', 'Kecamatan/Kawasan', 'Sertifikat']:
        df_input[col] = df_input[col].astype('category')

    return df_input

def hitung_kpr(harga, dp_pct, tenor_tahun, bunga_pa):
    """Menghitung rincian cicilan KPR dan porsi pembagiannya."""
    L = harga * (1 - dp_pct / 100)
    r = (bunga_pa / 12) / 100
    n = tenor_tahun * 12
    
    if r > 0:
        M = L * (r * (1 + r)**n) / ((1 + r)**n - 1)
    else:
        M = L / n
        
    M_total = M * 1.1 # Ditambah estimasi pajak/asuransi 10%
    
    bunga_bulan = L * r
    pokok_bulan = M - bunga_bulan
    pajak_bulan = M_total - M
    
    pct_pokok = (pokok_bulan / M_total) * 100
    pct_bunga = (bunga_bulan / M_total) * 100
    pct_pajak = 10.0
    
    return M_total, pct_pokok, pct_bunga, pct_pajak

def format_rupiah_short(nilai):
    if nilai >= 1e9:
        return f"Rp {nilai / 1e9:.1f}M"
    elif nilai >= 1e6:
        return f"Rp {nilai / 1e6:.1f}Jt"
    else:
        return f"Rp {nilai:,.0f}"

def format_rupiah_full(nilai):
    return f"Rp {nilai:,.0f}"


# =====================================================================
# 4. INISIALISASI SESSION STATE
# =====================================================================
if 'prediksi_selesai' not in st.session_state:
    st.session_state['prediksi_selesai'] = False
if 'komparator_list' not in st.session_state:
    st.session_state['komparator_list'] = []

# =====================================================================
# 5. NAVIGASI SIDEBAR (NATIVE STREAMLIT)
# =====================================================================
st.sidebar.markdown("## 🏡 JKT PropTech AI")
st.sidebar.markdown("Navigasi Menu Utama:")
pilihan_menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Prediksi AI & Kalkulator KPR", 
     "Beranda & Affordability Map", 
     "🔥 Good Deal Finder", 
     "⚖️ Komparator Properti", 
     "📊 Analytical Insights"],
     label_visibility="collapsed"
)
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Fairuz Azizy")


# =====================================================================
# HALAMAN: PREDIKSI AI & KALKULATOR KPR (HALAMAN UTAMA/KEDUA)
# =====================================================================
if pilihan_menu == "Prediksi AI & Kalkulator KPR":
    
    if not st.session_state['prediksi_selesai']:
        # Tampilan Form Input NATIVE Streamlit (Tanpa injeksi HTML yang tumpang tindih)
        st.markdown("<h1 style='text-align: center;'>Prediksi Cerdas Harga Properti</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8e90a2;'>Masukkan spesifikasi detail properti Anda dan biarkan AI kami memberikan taksiran harga pasar yang akurat.</p>", unsafe_allow_html=True)
        st.write("")

        with st.form(key="prop_form", border=True):
            st.markdown("### 📋 Detail Spesifikasi Properti")
            st.divider()
            
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown("#### 📍 Lokasi & Dimensi")
                kota_input = st.selectbox("Kota", options=semua_kota, index=0)
                daftar_kec_kota = kota_ke_kec.get(kota_input, semua_kecamatan)
                kecamatan_input = st.selectbox("Kecamatan / Kawasan", options=daftar_kec_kota, index=0)
                
                luas_tanah = st.number_input("Luas Tanah (m²)", min_value=20, max_value=5000, value=120, step=5)
                luas_bangunan = st.number_input("Luas Bangunan (m²)", min_value=20, max_value=5000, value=150, step=5)
                jumlah_lantai = st.number_input("Jumlah Lantai", min_value=1, max_value=5, value=2, step=1)
                
            with col2:
                st.markdown("#### 🛏️ Fasilitas Dasar")
                sertifikat_input = st.selectbox("Jenis Sertifikat", options=['SHM', 'HGB', 'Lainnya'], index=0)
                
                col_k1, col_k2 = st.columns(2)
                with col_k1:
                    kt_utama = st.number_input("Kamar Tidur Utama", min_value=0, max_value=20, value=3)
                    km_utama = st.number_input("Kamar Mandi Utama", min_value=0, max_value=20, value=2)
                    garasi = st.number_input("Kapasitas Garasi", min_value=0, max_value=10, value=1)
                with col_k2:
                    kt_art = st.number_input("Kamar Tidur ART", min_value=0, max_value=5, value=1)
                    km_art = st.number_input("Kamar Mandi ART", min_value=0, max_value=5, value=1)
                    carport = st.number_input("Kapasitas Carport", min_value=0, max_value=10, value=1)
                    
            st.markdown("#### 🏷️ Fasilitas Pendukung Lingkungan")
            fasilitas_terpilih = st.multiselect(
                "Pilih fasilitas yang tersedia:",
                options=list(DAFTAR_FASILITAS.keys()),
                default=['Siap Huni', 'Bebas Banjir']
            )
            
            st.write("")
            tombol_prediksi = st.form_submit_button("🔮 Mulai Taksiran Harga AI", use_container_width=True, type="primary")

        # Logika Prediksi
        if tombol_prediksi:
            df_input = bangun_input_prediksi(
                kota=kota_input, kecamatan=kecamatan_input, sertifikat=sertifikat_input,
                luas_tanah=luas_tanah, luas_bangunan=luas_bangunan,
                kt_utama=kt_utama, kt_art=kt_art, km_utama=km_utama, km_art=km_art,
                garasi=garasi, carport=carport, fasilitas_terpilih=fasilitas_terpilih
            )
            
            prediksi_log = model.predict(df_input)
            harga_prediksi = float(np.expm1(prediksi_log[0]))

            mape_val = metrik['mape'] / 100
            batas_bawah = harga_prediksi * (1 - mape_val)
            batas_atas = harga_prediksi * (1 + mape_val)

            input_rekom = {
                'Kota': kota_input, 'Kecamatan/Kawasan': kecamatan_input,
                'Luas_Tanah': luas_tanah, 'Luas_Bangunan': luas_bangunan
            }
            list_rekom = dapatkan_rekomendasi(input_rekom, harga_prediksi, df_master, top_n=4)

            # Simpan state
            st.session_state['prediksi_selesai'] = True
            st.session_state['harga_prediksi'] = harga_prediksi
            st.session_state['batas_bawah'] = batas_bawah
            st.session_state['batas_atas'] = batas_atas
            st.session_state['list_rekom'] = list_rekom
            st.session_state['input_kecamatan'] = kecamatan_input
            st.session_state['input_kota'] = kota_input
            st.rerun()

    else:
        # =====================================================================
        # TAMPILAN HASIL PREDIKSI (NATIVE STREAMLIT LAYOUT MENIRU DESAIN UI)
        # =====================================================================
        harga_pred = st.session_state['harga_prediksi']
        bt_bawah = st.session_state['batas_bawah']
        bt_atas = st.session_state['batas_atas']
        rekom_data = st.session_state['list_rekom']

        col_header, col_btn = st.columns([8, 2])
        with col_header:
            st.markdown("## 🔮 Hasil Analisis Properti")
        with col_btn:
            if st.button("⬅️ Hitung Ulang Spesifikasi", use_container_width=True):
                st.session_state['prediksi_selesai'] = False
                st.rerun()
        
        st.divider()

        # Layout Utama: Kiri (Harga) vs Kanan (KPR)
        col_main, col_kpr = st.columns([6, 4], gap="large")

        # KOLOM KIRI: TAKSIRAN HARGA
        with col_main:
            st.markdown("<p style='text-align: center; color: #8e90a2; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0;'>Taksiran Harga AI</p>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: #3b82f6; font-size: 3.5rem; text-shadow: 0 0 15px rgba(59,130,246,0.3); margin-top: 0; margin-bottom: 2rem;'>{format_rupiah_full(harga_pred)}</h1>", unsafe_allow_html=True)
            
            # Margin Rentang Harga (Dibungkus agar sejajar tinggi dengan kalkulator KPR)
            with st.container(border=True):
                st.markdown("<p style='color: #8e90a2; font-size: 14px; font-weight: 600; margin-bottom: 15px;'>📊 RENTANG AKURASI PREDIKSI</p>", unsafe_allow_html=True)
                col_min, col_max = st.columns(2)
                with col_min:
                    st.markdown(f"**Kisaran Bawah**")
                    st.markdown(f"### {format_rupiah_full(bt_bawah)}")
                    st.progress(1.0 - (metrik['mape'] / 100.0), text=f"Batas Akurasi: {100 - metrik['mape']:.1f}%")
                
                with col_max:
                    st.markdown(f"**Kisaran Atas**")
                    st.markdown(f"### {format_rupiah_full(bt_atas)}")
                    st.progress(min(metrik['r2'] / 100.0, 1.0), text=f"Skor R-Squared: {metrik['r2']:.1f}%")
                
                st.write("")
                st.markdown("<p style='font-size: 12px; color: #64748b; text-align: center; margin-top: 5px;'><em>*Estimasi dipengaruhi oleh kondisi makroekonomi dan negosiasi pasar sesungguhnya.</em></p>", unsafe_allow_html=True)

        # KOLOM KANAN: KALKULATOR KPR
        with col_kpr:
            with st.container(border=True):
                st.markdown("#### 🏦 Kalkulator KPR")
                
                dp_val = st.slider("Uang Muka (DP %)", 5, 50, 20, 5)
                tenor_val = st.slider("Tenor (Tahun)", 1, 30, 20, 1)
                bunga_val = st.slider("Suku Bunga (p.a %)", 1.0, 15.0, 5.5, 0.1)
                
                M_total, pct_pokok, pct_bunga, pct_pajak = hitung_kpr(harga_pred, dp_val, tenor_val, bunga_val)
                
                st.divider()
                st.markdown("<p style='text-align: center; color: #8e90a2; font-size: 11px; text-transform: uppercase; margin-bottom: 0;'>Cicilan per Bulan</p>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center; color: #dde1fe; margin-top: 0;'>{format_rupiah_short(M_total)}</h2>", unsafe_allow_html=True)
                
                # Menampilkan breakdown sederhana
                st.caption(f"🔵 Pokok: {pct_pokok:.0f}% &nbsp; | &nbsp; 🟠 Bunga: {pct_bunga:.0f}% &nbsp; | &nbsp; ⚪ Pajak: {pct_pajak:.0f}%")

        st.write("")

        # BAGIAN BAWAH: REKOMENDASI PROPERTI
        st.markdown("### 🏘️ Rekomendasi Properti Sejenis")
        
        if not rekom_data.empty:
            harga_rekom_terdekat = rekom_data.iloc[0]['Harga']
            
            # Logika Peringatan Sesuai Margin
            if harga_rekom_terdekat > bt_atas:
                st.warning("⚠️ **Catatan:** Properti dengan spesifikasi dan harga pada rentang tersebut tidak tersedia. Berikut adalah beberapa rekomendasi alternatif terdekat.")
            elif harga_rekom_terdekat < bt_bawah:
                st.success("🔥 **Good Deal!** Ditemukan rekomendasi properti dengan spesifikasi serupa yang ditawarkan di bawah taksiran batas bawah AI.")
            else:
                st.info("✅ Menampilkan rekomendasi properti serupa dengan spesifikasi dan harga terdekat.")

            cols = st.columns(len(rekom_data))
            for idx, row in rekom_data.iterrows():
                with cols[idx]:
                    with st.container(border=True):
                        # Ambil gambar
                        with st.spinner("Memuat foto..."):
                            link_foto = ambil_foto_rumah123(row['URL_ID'])
                        if not link_foto:
                            link_foto = "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80"
                        
                        st.image(link_foto, use_container_width=True)
                        
                        # Info properti
                        st.markdown(f"#### {row['Kecamatan/Kawasan']} Residence")
                        st.markdown(f"<p style='color:#94a3b8; font-size:13px; margin-top:-10px; margin-bottom:10px;'>📍 {row['Kecamatan/Kawasan']}, {row['Kota']}</p>", unsafe_allow_html=True)
                        st.markdown(f"### <span style='color:#3b82f6'>{format_rupiah_short(row['Harga'])}</span>", unsafe_allow_html=True)
                        
                        # Dimensi
                        st.markdown(f"**LT / LB:** {row['Luas_Tanah']} m² / {row['Luas_Bangunan']} m²")
                        
                        # Perhitungan Kamar dan Parkir dengan format X + Y
                        kt_utama = int(row['Kamar_Tidur_Utama'])
                        kt_art = int(row.get('Kamar_Tidur_ART', 0)) if not pd.isna(row.get('Kamar_Tidur_ART', 0)) else 0
                        kt_str = f"{kt_utama} + {kt_art}" if kt_art > 0 else f"{kt_utama}"
                        
                        km_utama = int(row['Kamar_Mandi_Utama'])
                        km_art = int(row.get('Kamar_Mandi_ART', 0)) if not pd.isna(row.get('Kamar_Mandi_ART', 0)) else 0
                        km_str = f"{km_utama} + {km_art}" if km_art > 0 else f"{km_utama}"
                        
                        garasi_val = int(row.get('Garasi_Utama', 0)) if not pd.isna(row.get('Garasi_Utama', 0)) else 0
                        carport_val = int(row.get('Carport', 0)) if not pd.isna(row.get('Carport', 0)) else 0
                        parkir_str = f"{garasi_val} + {carport_val}" if carport_val > 0 else f"{garasi_val}"

                        st.markdown(f"<div style='display:flex; gap:16px; color:#cbd5e1; font-size:14px; margin-top:8px; margin-bottom:12px; font-weight: 500;'>"
                                    f"<span>🛏️ {kt_str}</span>"
                                    f"<span>🛁 {km_str}</span>"
                                    f"<span>🚗 {parkir_str}</span>"
                                    f"</div>", unsafe_allow_html=True)
                        
                        # Menambahkan Kata Kunci/Fasilitas (Badges/Bubbles Abu-abu)
                        fasilitas_list = []
                        for nama_display, nama_kolom in DAFTAR_FASILITAS.items():
                            if row.get(nama_kolom, 0) == 1:
                                fasilitas_list.append(nama_display)
                                
                        if fasilitas_list:
                            # Buat HTML span elements untuk setiap fasilitas (max 4)
                            badges = [f"<span style='background-color:#1e293b; color:#94a3b8; padding:4px 8px; border-radius:12px; font-size:10px; border:1px solid #334155; display:inline-block; margin-bottom:6px; margin-right:6px;'>{f}</span>" for f in fasilitas_list[:4]]
                            st.markdown(f"<div style='min-height: 45px;'>{''.join(badges)}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='min-height: 45px;'></div>", unsafe_allow_html=True)
                        
                        st.link_button("🔗 Buka di Rumah123", row['URL_ID'], use_container_width=True)
        else:
            st.info("Tidak ditemukan data rekomendasi di area ini.")

# =====================================================================
# HALAMAN LAINNYA (STUBS)
# =====================================================================
elif pilihan_menu == "Beranda & Affordability Map":
    st.title("Peta Keterjangkauan (Affordability Map)")
    st.info("Dalam pengembangan.")

elif pilihan_menu == "🔥 Good Deal Finder":
    st.title("Peluang Investasi (Good Deal Finder)")
    st.info("Dalam pengembangan.")

elif pilihan_menu == "⚖️ Komparator Properti":
    st.title("Komparator Properti")
    st.info("Dalam pengembangan.")

elif pilihan_menu == "📊 Analytical Insights":
    st.title("Analisis Pasar Properti Jakarta")
    st.info("Dalam pengembangan.")
