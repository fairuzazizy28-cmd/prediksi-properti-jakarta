import pandas as pd
import sqlite3
import os

# =======================
# Mengkonfigurasi PATH
# =======================

PATH_CSV = 'data/processed/dataset_properti_jakarta_master_cleaned.csv'
PATH_DB = 'data/crawling/crawling_queue.db'
os.makedirs('data/crawling', exist_ok = True)

# Baca CSV
print("Membaca dataset cleaned...")
df = pd.read_csv(PATH_CSV)
print(f"Total data: {len(df)} baris")

# ambil kolom sebagai antrean
df_queue = df[['ID', 'URL_ID', 'Harga', 'Kota', 'Sertifikat']].copy()
df_queue = df_queue.dropna(subset=['URL_ID'])

# menambahkan kolom
df_queue