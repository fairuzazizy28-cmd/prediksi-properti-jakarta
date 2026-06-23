import pandas as pd
import os

MASTER_CSV = 'data/processed/dataset_properti_jakarta_master_fe2.csv'
IMAGES_CSV = 'data/processed/dataset_properti_jakarta_master_fe3_images.csv'
FINAL_CSV = 'data/processed/dataset_properti_jakarta_master_fe_final.csv'

if not os.path.exists(IMAGES_CSV):
    print("File hasil scraping (fe3_images.csv) belum ada. Jalankan scrape_images_async.py dulu.")
    exit()

df_master = pd.read_csv(MASTER_CSV)
df_images = pd.read_csv(IMAGES_CSV)

# Remove duplicates in case of failed resumes
df_images = df_images.drop_duplicates(subset=['ID'], keep='last')

# Merge
df_merged = pd.merge(df_master, df_images, on='ID', how='left')

# Save (Kita bisa menimpa file master lama, atau buat file baru)
# Lebih aman buat file baru, lalu kalau sukses, kita timpa master
df_merged.to_csv(FINAL_CSV, index=False)
print(f"Berhasil menggabungkan gambar! File disimpan di {FINAL_CSV}")

# Optional: Replace master with final
# import shutil
# shutil.move(FINAL_CSV, MASTER_CSV)
