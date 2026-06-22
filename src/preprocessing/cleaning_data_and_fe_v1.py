import pandas as pd
import re
from collections import Counter
import ast

pd.set_option('display.max_columns', None)
# ==========================================
path_input = 'data/raw/dataset_properti_jakarta_master_raw.csv'
path_output = 'data/processed/dataset_properti_jakarta_master_cleaned.csv'
df = pd.read_csv(path_input)
print(f"Dimensi Data Awal: {df.shape[0]} baris dan {df.shape[1]} kolom.")
# ==========================================

# Menampilkan informasi umum tentang data
print(df.info())
print(df.isnull().sum())
print(df.head(5))

# CLEANING

# menentukan pola regex untuk membersihkan harga
POLA_HARGA = re.compile(r'([\d\.,]+)\s*(juta|miliar|milliar|m)', re.IGNORECASE)

def bersihkan_harga(teks_harga):
    if pd.isna(teks_harga):
        return None  
    
    teks = str(teks_harga).lower()
    teks = teks.replace('rp', '').replace('rp.', '').strip().replace(' ', '')
    pencarian = POLA_HARGA.search(teks)

    if pencarian:
        angka_str = pencarian.group(1).replace(',','.')
        angka = float(angka_str)
        satuan = pencarian.group(2)
        
        if 'juta' in satuan:
            return int(angka * 1_000_000)
        elif 'miliar' in satuan or 'milliar' in satuan or satuan == 'm':
            return int(angka * 1_000_000_000)
            
    # fallback jika tidak sesuai pola, ambil angka saja
    angka_saja = re.sub(r'[^\d]', '', teks)
    return int(angka_saja) if angka_saja else None

def bersihkan_luas(teks):
    if pd.isna(teks):
        return None
    
    teks = str(teks).lower().replace(' ', '')
    angka_saja = re.sub(r'[^\d]', '', teks)
    return int(angka_saja) if angka_saja else None

def pisah_spesifikasi(teks):
    if pd.isna(teks):
        return 0, 0
    
    teks = str(teks).replace(' ', '') # Hapus spasi kosong
    
    if '+' in teks:
        bagian = teks.split('+')
        utama = int(bagian[0]) if bagian[0].isdigit() else 0
        art = int(bagian[1]) if bagian[1].isdigit() else 0
        return utama, art
    else:
        utama = int(teks) if teks.isdigit() else 0
        return utama, 0
    
def pisah_kawasan(teks):
    if pd.isna(teks):
        return None, None
    
    if ',' in str(teks):
        bagian = str(teks).split(',')
        kecamatan = bagian[0].strip()
        kota = bagian[1].strip()
        return kecamatan, kota
    else:
        return str(teks).strip(), None

# eksekusi pembersihan harga
print("Membaca dataset mentah...")
df = pd.read_csv(path_input)
print(f"Dimensi awal: {df.shape[0]} baris.")

# Mengganti karakter enter (\r atau \n) di kolom deskripsi dengan spasi biasa
df['Deskripsi'] = df['Deskripsi'].fillna('').astype(str).str.replace(r'[\r\n]+', ' ', regex=True)

print("Membersihkan kolom 'Harga'...")
df['Harga'] = df['Harga'].apply(bersihkan_harga)
df['Luas_Bangunan'] = df['Luas_Bangunan'].apply(bersihkan_luas)
df['Luas_Tanah'] = df['Luas_Tanah'].apply(bersihkan_luas)

# eksekusi kamar tidur
idx_kt = df.columns.get_loc('Kamar_Tidur')
kamar_tidur_baru = df['Kamar_Tidur'].apply(lambda x: pd.Series(pisah_spesifikasi(x)))
df = df.drop(columns=['Kamar_Tidur'])
df.insert(idx_kt, 'Kamar_Tidur_Utama', kamar_tidur_baru[0])
df.insert(idx_kt + 1, 'Kamar_Tidur_ART', kamar_tidur_baru[1])

# eksekusi kamar mandi
idx_km = df.columns.get_loc('Kamar_Mandi')
kamar_mandi_baru = df['Kamar_Mandi'].apply(lambda x: pd.Series(pisah_spesifikasi(x)))
df = df.drop(columns=['Kamar_Mandi'])
df.insert(idx_km, 'Kamar_Mandi_Utama', kamar_mandi_baru[0])
df.insert(idx_km + 1, 'Kamar_Mandi_ART', kamar_mandi_baru[1])

# eksekusi garasi
idx_garasi = df.columns.get_loc('Garasi')
garasi_baru = df['Garasi'].apply(lambda x: pd.Series(pisah_spesifikasi(x)))
df = df.drop(columns=['Garasi'])
df.insert(idx_garasi, 'Garasi_Utama', garasi_baru[0])
df.insert(idx_garasi + 1, 'Carport', garasi_baru[1])


# cek kata kunci
semua_tag = []
for baris in df['Kata_Kunci'].dropna():
    try:
        # Mengubah string list "[...]" menjadi list asli [...]
        list_tag = ast.literal_eval(baris)
        if isinstance(list_tag, list):
            # Memasukkan semua tag ke dalam satu list besar
            semua_tag.extend(list_tag)
    except (ValueError, SyntaxError):
        # Jika ada baris yang rusak/error, dilewati saja
        continue
    
# ----------------------------------------------------
# 3. MENGHITUNG FREKUENSI UNIQUE VALUE
# ----------------------------------------------------
# Counter membantu menghitung berapa kali setiap tag muncul secara otomatis
counter_kata_kunci = Counter(semua_tag)
# Mengubah hasil hitungan menjadi DataFrame Pandas agar rapi dan mudah dianalisis
df_unik = pd.DataFrame(
    counter_kata_kunci.items(), 
    columns=['Kata_Kunci_Unik', 'Jumlah_Kemunculan']
)
# Mengurutkan dari yang paling sering muncul ke yang paling jarang
df_unik = df_unik.sort_values(by='Jumlah_Kemunculan', ascending=False).reset_index(drop=True)
# Menghitung persentase kemunculan terhadap total seluruh properti
df_unik['Persentase (%)'] = (df_unik['Jumlah_Kemunculan'] / len(df)) * 100
# Menampilkan tabel hasil unique value
print("=== DAFTAR UNIQUE VALUE KATA KUNCI ===")
print(df_unik.to_string(index=False)) # to_string() digunakan agar tabel tidak terpotong saat diprint

idx_kw = df.columns.get_loc('Kawasan')
kw_data = df['Kawasan'].apply(lambda x: pd.Series(pisah_kawasan(x)))
df = df.drop(columns=['Kawasan'])
df.insert(idx_kw, 'Kecamatan/Kawasan', kw_data[0])
df.insert(idx_kw + 1, 'Kota', kw_data[1])

# ekssekusi kolom Kata_Kunci
def proses_ekstraksi_kata_kunci(df):
    df_temp = df.copy()
    
    # 1. Pastikan kolom Kata_Kunci dibaca sebagai List asli (bukan String teks)
    df_temp['Kata_Kunci'] = df_temp['Kata_Kunci'].fillna('[]').apply(ast.literal_eval)
    
    # 2. Definisikan kata kunci pilihan yang berdampak besar pada harga
    fitur_pilihan = [
        'Siap Huni', 'Bebas Banjir', 'Komplek Perumahan',
        'Dekat Akses Transportasi', 'Dekat Sekolah', 'Dekat Pusat Perbelanjaan', 'Dekat Fasilitas Kesehatan', 'Dekat Tempat Ibadah', 'Dekat Tempat Wisata', 'Dekat Landmark'
    ]
    
    # 3. Ekstraksi menjadi kolom biner (1 jika ada kata kunci tersebut, 0 jika tidak)
    for fit in fitur_pilihan:
        # Menghasilkan nama kolom baru: "Fasilitas_Bebas_Banjir", "Fasilitas_Akses_Transportasi", dll.
        nama_kolom = 'Fasilitas_' + fit.replace(' ', '_')
        df_temp[nama_kolom] = df_temp['Kata_Kunci'].apply(lambda x: 1 if fit in x else 0)
        
    # 4. Hapus kolom Kata_Kunci asli karena sudah tidak dibutuhkan
    df_temp = df_temp.drop(columns=['Kata_Kunci'])
    
    return df_temp

# Contoh penggunaan
df = proses_ekstraksi_kata_kunci(df)


print(df.head(5))
print(df.dtypes)

print("Menyimpan dataset bersih ke folder processed...")
df.to_csv(path_output, index=False, encoding='utf-8-sig')

# print("Menyimpan dataset bersih ke file baru...")
# df.to_csv(path_output, index=False, encoding='utf-8-sig')
# print(f"Selesai! Data berhasil diamankan di: {path_output}")
