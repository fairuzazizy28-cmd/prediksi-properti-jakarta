"""
train_dan_simpan_model.py
=========================
Skrip untuk melatih model LightGBM dan menyimpannya ke file .pkl
beserta data pendukung (lookup median kecamatan, mapping kota-kecamatan, dll.)
agar bisa digunakan oleh dashboard Streamlit.

Jalankan skrip ini SATU KALI sebelum menjalankan dashboard:
  venv\Scripts\python.exe src/modeling/train_dan_simpan_model.py
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_absolute_percentage_error
from sklearn.ensemble import IsolationForest
from lightgbm import LGBMRegressor

# =====================================================================
# 1. LOAD & BERSIHKAN DATASET
# =====================================================================
file_path = "data/processed/dataset_properti_jakarta_master_fe2.csv"
print("Membaca dataset hasil Feature Engineering...")
df = pd.read_csv(file_path).dropna(subset=['Harga'])
print(f"Total data awal: {df.shape[0]} baris")

# Pembersihan outlier
def filter_extreme_outliers(dataframe, column, multiplier=3.0):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = max(0, Q1 - multiplier * IQR)
    upper_bound = Q3 + multiplier * IQR
    return dataframe[(dataframe[column] >= lower_bound) & (dataframe[column] <= upper_bound)]

df_cleaned = df.copy()
df_cleaned = filter_extreme_outliers(df_cleaned, 'Luas_Tanah', multiplier=3.0)
df_cleaned = filter_extreme_outliers(df_cleaned, 'Luas_Bangunan', multiplier=3.0)

iso_forest = IsolationForest(contamination=0.015, random_state=42, n_jobs=-1)
outlier_predictions = iso_forest.fit_predict(df_cleaned[['Harga', 'Luas_Tanah', 'Luas_Bangunan']])
df_final = df_cleaned[outlier_predictions == 1].copy()
print(f"Total data setelah pembersihan outlier: {df_final.shape[0]} baris")

# =====================================================================
# 2. SIAPKAN LOOKUP TABLE UNTUK DASHBOARD
# =====================================================================
print("Menyiapkan lookup table median kecamatan...")

# Median Luas Tanah & Luas Bangunan per Kecamatan (untuk fitur LT_vs_Median & LB_vs_Median)
median_lt_per_kec = df_final.groupby('Kecamatan/Kawasan')['Luas_Tanah'].median().to_dict()
median_lb_per_kec = df_final.groupby('Kecamatan/Kawasan')['Luas_Bangunan'].median().to_dict()

# Mapping Kota -> Daftar Kecamatan (untuk dropdown cascading di dashboard)
kota_ke_kecamatan = df_final.groupby('Kota')['Kecamatan/Kawasan'].apply(
    lambda x: sorted(x.unique().tolist())
).to_dict()

# Daftar semua kecamatan unik (untuk validasi input bebas)
semua_kecamatan = sorted(df_final['Kecamatan/Kawasan'].unique().tolist())

# Daftar kota unik
semua_kota = sorted(df_final['Kota'].unique().tolist())

# =====================================================================
# 3. DEFINISI FITUR & TRAINING MODEL
# =====================================================================
numeric_features = [
    'Luas_Tanah', 'Luas_Bangunan', 'Rasio_LB_LT', 'Luas_per_Kamar',
    'LT_vs_Median_Kecamatan', 'LB_vs_Median_Kecamatan',
    'Kamar_Tidur_Utama', 'Kamar_Tidur_ART', 'Kamar_Mandi_Utama',
    'Kamar_Mandi_ART', 'Garasi_Utama', 'Carport', 'Kapasitas_Parkir', 'Rasio_KT_KM'
]

categorical_features = ['Kota', 'Kecamatan/Kawasan', 'Sertifikat']

binary_features = [
    'Is_SHM', 'Ada_ART_Room',
    'Fasilitas_Siap_Huni', 'Fasilitas_Bebas_Banjir', 'Fasilitas_Komplek_Perumahan',
    'Fasilitas_Dekat_Akses_Transportasi', 'Fasilitas_Dekat_Sekolah',
    'Fasilitas_Dekat_Pusat_Perbelanjaan', 'Fasilitas_Dekat_Fasilitas_Kesehatan',
    'Fasilitas_Dekat_Tempat_Ibadah', 'Fasilitas_Dekat_Tempat_Wisata', 'Fasilitas_Dekat_Landmark'
]

all_features = numeric_features + categorical_features + binary_features

X = df_final[all_features].copy()
y = df_final['Harga']

# Ubah kolom kategorikal menjadi tipe category
for col in categorical_features:
    X[col] = X[col].astype('category')

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
y_train_log = np.log1p(y_train)

# Training
print("Melatih model LightGBM Regressor...")
model = LGBMRegressor(
    n_estimators=1200,
    learning_rate=0.02,
    num_leaves=255,
    colsample_bytree=0.8,
    subsample=0.8,
    random_state=42,
    n_jobs=-1,
    verbose=-1
)
model.fit(X_train, y_train_log)

# Evaluasi
y_pred_log = model.predict(X_test)
y_pred = np.expm1(y_pred_log)
r2 = r2_score(y_test, y_pred) * 100
mae = mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred) * 100

print(f"\nR2 Score  : {r2:.2f}%")
print(f"MAE       : Rp {mae:,.2f}")
print(f"MAPE      : {mape:.2f}%")

# =====================================================================
# 4. SIMPAN MODEL & DATA PENDUKUNG KE FILE .pkl
# =====================================================================
os.makedirs('models', exist_ok=True)

paket_model = {
    'model': model,
    'fitur_numerik': numeric_features,
    'fitur_kategorikal': categorical_features,
    'fitur_biner': binary_features,
    'semua_fitur': all_features,
    'median_lt_per_kec': median_lt_per_kec,
    'median_lb_per_kec': median_lb_per_kec,
    'kota_ke_kecamatan': kota_ke_kecamatan,
    'semua_kecamatan': semua_kecamatan,
    'semua_kota': semua_kota,
    'metrik': {
        'r2': r2,
        'mae': mae,
        'mape': mape
    }
}

path_model = 'models/model_lgbm_properti.pkl'
with open(path_model, 'wb') as f:
    pickle.dump(paket_model, f)

print(f"\nModel dan data pendukung berhasil disimpan ke: {path_model}")
print(f"Ukuran file: {os.path.getsize(path_model) / (1024*1024):.2f} MB")
print("Selesai! Silakan jalankan dashboard Streamlit Anda.")
