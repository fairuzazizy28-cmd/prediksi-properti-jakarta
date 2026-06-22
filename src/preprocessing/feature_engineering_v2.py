import pandas as pd
import numpy as np
import os

# =====================================================================
# PATH FILE
# =====================================================================
path_input = 'data/processed/dataset_properti_jakarta_master_cleaned.csv'
path_output = 'data/processed/dataset_properti_jakarta_master_fe2.csv'

print("Membaca dataset cleaned...")
if not os.path.exists(path_input):
    raise FileNotFoundError(f"File {path_input} tidak ditemukan.")

df = pd.read_csv(path_input)
print(f"Dimensi awal: {df.shape[0]} baris, {df.shape[1]} kolom.")

# =====================================================================
# STEP 1: DEDUPLIKASI DATA (Mencegah Overfitting & Data Leakage)
# =====================================================================
print("Melakukan deduplikasi iklan properti...")
kolom_duplikat = [
    'Harga', 'Kecamatan/Kawasan', 'Kota', 'Sertifikat', 
    'Kamar_Tidur_Utama', 'Kamar_Mandi_Utama', 'Luas_Tanah', 'Luas_Bangunan'
]
df = df.drop_duplicates(subset=kolom_duplikat, keep='first')
print(f"Dimensi setelah deduplikasi: {df.shape[0]} baris.")

# =====================================================================
# STEP 2: PENYARINGAN DATA SAMPAH (Domain-Specific Outlier Cleaning)
# =====================================================================
print("Menyaring data berdasarkan rasio harga per m2 tanah yang realistis...")
# Buang Luas Tanah & Luas Bangunan bernilai 0
df = df[(df['Luas_Tanah'] > 0) & (df['Luas_Bangunan'] > 0)]

# Hitung harga per m2 tanah
df['Harga_per_m2_Tanah'] = df['Harga'] / df['Luas_Tanah']

# Filter: Hanya pertahankan properti dengan harga tanah Rp 3 Juta/m2 s.d Rp 150 Juta/m2
df = df[(df['Harga_per_m2_Tanah'] >= 3_000_000) & (df['Harga_per_m2_Tanah'] <= 150_000_000)]
df = df.drop(columns=['Harga_per_m2_Tanah']) # Hapus kolom temp agar tidak target leakage
print(f"Dimensi setelah pembersihan harga per m2: {df.shape[0]} baris.")

# =====================================================================
# STEP 3: KONTEKS LINGKUNGAN (Kecamatan Grouping)
# =====================================================================
print("Membuat fitur perbandingan berbasis Kecamatan...")
median_lt_kec = df.groupby('Kecamatan/Kawasan')['Luas_Tanah'].transform('median').replace(0, np.nan)
df['LT_vs_Median_Kecamatan'] = (df['Luas_Tanah'] / median_lt_kec).fillna(1.0)

median_lb_kec = df.groupby('Kecamatan/Kawasan')['Luas_Bangunan'].transform('median').replace(0, np.nan)
df['LB_vs_Median_Kecamatan'] = (df['Luas_Bangunan'] / median_lb_kec).fillna(1.0)

# =====================================================================
# STEP 4: FITUR TURUNAN STANDAR
# =====================================================================
df['Rasio_LB_LT'] = df['Luas_Bangunan'] / df['Luas_Tanah']
df['Kapasitas_Parkir'] = df['Garasi_Utama'] + df['Carport']

km_safe = df['Kamar_Mandi_Utama'].replace(0, np.nan)
df['Rasio_KT_KM'] = df['Kamar_Tidur_Utama'] / km_safe
df['Rasio_KT_KM'] = df['Rasio_KT_KM'].fillna(df['Kamar_Tidur_Utama'])

df['Ada_ART_Room'] = ((df['Kamar_Tidur_ART'] > 0) | (df['Kamar_Mandi_ART'] > 0)).astype(int)
df['Luas_per_Kamar'] = df['Luas_Bangunan'] / (df['Kamar_Tidur_Utama'] + 1)
df['Is_SHM'] = (df['Sertifikat'].astype(str).str.upper() == 'SHM').astype(int)

# =====================================================================
# SAVE DATASET FINAL
# =====================================================================
print(f"Feature Engineering selesai! Total fitur yang dimiliki sekarang: {df.shape[1]}")
print(f"Menyimpan dataset baru ke: {path_output}")
df.to_csv(path_output, index=False, encoding='utf-8-sig')
print("Selesai! Silakan jalankan kembali file training Anda.")