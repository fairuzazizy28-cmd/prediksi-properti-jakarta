import pandas as pd
import glob

# membaca dan gabungkan semua file
print("Mencari file CSV partisi...")
daftar_file = glob.glob('data_jak*.csv')
print(f"Ditemukan {len(daftar_file)} file. Memulai proses merging...")

# baca fle dan masukan dalam dataframe
list_dataframe = []
for file in daftar_file:
    df_temp = pd.read_csv(file)
    list_dataframe.append(df_temp)

df_master = pd.concat(list_dataframe, ignore_index=True)
print(f"Total data sebelum diacak: {len(df_master)} baris.")


# randomiasasi data untuk menghindari bias urutan
print("Mengacak urutan baris data...")
# frac=1 berarti mengambil 100% sampel dari data aslinya
# random_state=42 digunakan agar hasil acakan ini konsisten
df_acak = df_master.sample(frac=1, random_state=42).reset_index(drop=True)

# menambahkan kolom ID unik untuk setiap baris data
print("Menyisipkan kolom ID...")
# insert(loc=0, ...) memasukkan kolom baru tepat di indeks ke-0
# range(1, len() + 1) memberikan angka berurutan mulai dari 1 sampai baris terakhir
df_acak.insert(0, 'ID', range(1, len(df_acak) + 1))


# export hasil akhir ke CSV
nama_file_final = 'dataset_properti_jakarta_master.csv'
df_acak.to_csv(nama_file_final, index=False, encoding='utf-8-sig')

print("\n" + "="*50)
print(f"SUKSES! Dataset akhir berhasil dibuat: {nama_file_final}")
print(f"Total Dimensi Data: {df_acak.shape[0]} baris dan {df_acak.shape[1]} kolom.")
print("="*50)

# Menampilkan 5 baris pertama untuk preview
print("\nPreview 5 data pertama:")
print(df_acak.head())
