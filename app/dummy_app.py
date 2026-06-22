import streamlit as st
import pandas as pd

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA (WAJIB PALING ATAS)
# ==========================================
st.set_page_config(
    page_title="Valuasi Properti Jakarta",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed" # Menyembunyikan sidebar bawaan
)

# ==========================================
# 2. INJEKSI CSS KUSTOM (SECRET SAUCE)
# ==========================================
st.markdown("""
<style>
    /* Menyembunyikan elemen bawaan Streamlit agar terlihat seperti web mandiri */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Modifikasi Kartu / Container Utama */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Mempercantik Tombol Prediksi (Warna, Bayangan, dan Animasi Hover) */
    .stButton>button {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        border-radius: 8px;
        height: 55px;
        font-weight: 700;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(37, 99, 235, 0.3);
        border: 1px solid #60A5FA;
    }

    /* Mempercantik Kotak Hasil Metrik (Nilai Harga) */
    div[data-testid="metric-container"] {
        background-color: #F8FAFC;
        border-left: 5px solid #2563EB;
        border-radius: 5px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Warna teks label metrik */
    div[data-testid="stMetricLabel"] {
        font-size: 1.1rem;
        font-weight: 600;
        color: #475569;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER APLIKASI
# ==========================================
st.title("🏡 Sistem Cerdas Valuasi Properti DKI Jakarta")
st.markdown("""
Platform prediktif ini memanfaatkan algoritma *Machine Learning* untuk mengestimasi nilai pasar wajar 
rumah tapak berdasarkan spesifikasi arsitektur, lokasi strategis, dan status legalitas.
""")
st.markdown("---")

# ==========================================
# 4. FUNGSI SIMULASI PREDIKSI (DUMMY)
# ==========================================
def simulasi_prediksi_harga(lt, lb, kt, km, garasi, sertifikat):
    base_harga = 500_000_000
    faktor_lt = lt * 15_000_000
    faktor_lb = lb * 8_000_000
    faktor_kt = kt * 50_000_000
    sertifikat_multiplier = 1.2 if sertifikat == "SHM" else 1.0
    
    total_estimasi = (base_harga + faktor_lt + faktor_lb + faktor_kt) * sertifikat_multiplier
    return int(total_estimasi)

# ==========================================
# 5. TATA LETAK MENGGUNAKAN TABS
# ==========================================
tab1, tab2 = st.tabs(["📊 Kalkulator Valuasi", "📖 Tentang Model"])

with tab1:
    # Membagi layar tab pertama menjadi 2 kolom
    kolom_kiri, kolom_kanan = st.columns([1.2, 1], gap="large")

    with kolom_kiri:
        st.subheader("📋 Input Spesifikasi Aset")
        
        # Kelompok Input 1: Lokasi & Legalitas
        col_wil, col_sertif = st.columns(2)
        with col_wil:
            pilihan_wilayah = st.selectbox("Wilayah Administratif", ["Jakarta Selatan", "Jakarta Barat", "Jakarta Timur", "Jakarta Utara", "Jakarta Pusat"])
        with col_sertif:
            input_sertifikat = st.selectbox("Legalitas", ["SHM", "HGB", "Lainnya"])
            
        input_kawasan = st.text_input("Kecamatan / Kelurahan", placeholder="Contoh: Tebet, Kebayoran Baru")
        
        # Kelompok Input 2: Dimensi Menggunakan Slider agar lebih interaktif
        st.write("**Dimensi Lahan & Bangunan**")
        input_lt = st.slider("Luas Tanah (m²)", min_value=20, max_value=1000, value=120, step=5)
        input_lb = st.slider("Luas Bangunan (m²)", min_value=20, max_value=1000, value=100, step=5)
            
        # Kelompok Input 3: Fasilitas
        st.write("**Fasilitas Ruang**")
        col_kt, col_km, col_gr = st.columns(3)
        with col_kt:
            input_kt = st.number_input("Kamar Tidur", min_value=1, max_value=10, value=3)
        with col_km:
            input_km = st.number_input("Kamar Mandi", min_value=1, max_value=10, value=2)
        with col_gr:
            input_gr = st.number_input("Garasi/Carport", min_value=0, max_value=5, value=1)
            
        # Kelompok Input 4: Expander untuk Opsi Tambahan
        with st.expander("🛠️ Fitur & Kondisi Tambahan (Opsional)"):
            fitur_banjir = st.checkbox("Berada di Zona Bebas Banjir")
            fitur_komplek = st.checkbox("Terletak di Dalam Komplek/Cluster")
            fitur_jalan = st.checkbox("Akses Jalan 2 Mobil")

        st.write("") # Spasi kosong
        # Tombol Aksi
        tombol_prediksi = st.button("Hitung Estimasi Harga Pasar")

    # ==========================================
    # BAGIAN OUTPUT (KOLOM KANAN)
    # ==========================================
    with kolom_kanan:
        st.subheader("📈 Hasil Analisis")
        
        if tombol_prediksi:
            # Panggil fungsi kalkulasi
            hasil_estimasi = simulasi_prediksi_harga(input_lt, input_lb, input_kt, input_km, input_gr, input_sertifikat)
            
            st.success("Proses komputasi selesai!")
            
            # Tampilan Metrik yang sudah dipercantik dengan CSS
            st.metric(
                label="Estimasi Valuasi Maksimal",
                value=f"Rp {hasil_estimasi:,}".replace(",", ".")
            )
            
            # Info Detail
            st.info(f"""
            **Rangkuman Properti:**
            📍 Lokasi: **{input_kawasan}, {pilihan_wilayah}**
            📜 Status: **{input_sertifikat}**
            📐 Fisik: **LT {input_lt} m² | LB {input_lb} m²**
            """)
            
            st.caption("⚠️ Nilai di atas adalah estimasi statistik. Harga aktual dapat dipengaruhi oleh kondisi fisik bangunan dan negosiasi pasar.")
        else:
            # State awal
            st.markdown("""
            <div style='text-align: center; padding: 50px 20px; color: #94A3B8; border: 2px dashed #CBD5E1; border-radius: 10px;'>
                <h4>Belum ada data yang diproses.</h4>
                <p>Silakan isi parameter di sebelah kiri dan klik tombol <b>Hitung Estimasi Harga Pasar</b>.</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.header("Arsitektur Model")
    st.write("Bagian ini nantinya akan diisi dengan penjelasan *feature importance* (variabel apa yang paling mempengaruhi harga di Jakarta), metrik evaluasi model seperti RMSE dan $R^2$, serta grafik visualisasi *dataset* hasil *scraping* yang telah dibersihkan.")