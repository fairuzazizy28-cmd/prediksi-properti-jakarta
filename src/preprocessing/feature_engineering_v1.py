import pandas as pd
import numpy as np
import os

# =====================================================================
# PATH FILE
# =====================================================================
path_input = 'data/processed/dataset_properti_jakarta_master_cleaned.csv'
path_output = 'data/processed/dataset_properti_jakarta_master_fe1.csv'

print("Membaca dataset cleaned...")
if not os.path.exists(path_input):
    raise FileNotFoundError(f"File {path_input} tidak ditemukan. Harap pastikan dataset cleaned sudah ada.")
df = pd.read_csv(path_input)
print(f"Dimensi awal: {df.shape[0]} baris, {df.shape[1]} kolom.")

# 0. Menghapus properti dengan Luas_Tanah atau Luas_Bangunan bernilai 0
print("Membuang baris dengan Luas Tanah atau Luas Bangunan bernilai 0...")
df = df[(df['Luas_Tanah'] > 0) & (df['Luas_Bangunan'] > 0)]
print(f"Dimensi setelah pembuangan nilai 0: {df.shape[0]} baris.")
print("Memulai proses Feature Engineering...")

# 1. Rasio LB / LT (Proxy Jumlah Lantai)
# Aman dari division by zero karena Luas_Tanah sudah dipastikan > 0
df['Rasio_LB_LT'] = df['Luas_Bangunan'] / df['Luas_Tanah']

# 2. Kapasitas Parkir (Total Garasi Utama + Carport)
df['Kapasitas_Parkir'] = df['Garasi_Utama'] + df['Carport']

# 3. Rasio Kamar Tidur Utama / Kamar Mandi Utama
# Mengganti Kamar_Mandi_Utama = 0 dengan NaN untuk menghindari pembagian dengan nol
km_safe = df['Kamar_Mandi_Utama'].replace(0, np.nan)
df['Rasio_KT_KM'] = df['Kamar_Tidur_Utama'] / km_safe

# Jika kamar mandi = 0, asumsikan rasionya sama dengan jumlah Kamar Tidur Utama
df['Rasio_KT_KM'] = df['Rasio_KT_KM'].fillna(df['Kamar_Tidur_Utama'])

# 4. Kategori Keberadaan Kamar Pembantu (ART Room) - Biner 1/0
df['Ada_ART_Room'] = ((df['Kamar_Tidur_ART'] > 0) | (df['Kamar_Mandi_ART'] > 0)).astype(int)

# 5. Luas Bangunan per Kamar Tidur (Indikator Kelapangan Ruangan)
df['Luas_per_Kamar'] = df['Luas_Bangunan'] / (df['Kamar_Tidur_Utama'] + 1)

# 6. Sertifikat Biner (Apakah SHM?)
df['Is_SHM'] = (df['Sertifikat'].astype(str).str.upper() == 'SHM').astype(int)
print(f"Feature Engineering selesai! Berhasil menambahkan 6 fitur baru.")
print(f"Dimensi data akhir: {df.shape[0]} baris, {df.shape[1]} kolom.")
print(f"Menyimpan ke: {path_output}")
df.to_csv(path_output, index=False, encoding='utf-8-sig')
print("Proses Berhasil!")