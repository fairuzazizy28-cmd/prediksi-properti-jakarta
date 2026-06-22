import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_absolute_percentage_error
from sklearn.ensemble import IsolationForest
from lightgbm import LGBMRegressor

# =====================================================================
# 1. LOAD DATASET (Menggunakan file master_fe2.csv)
# =====================================================================
file_path = "data/processed/dataset_properti_jakarta_master_fe2.csv"
print("Membaca dataset hasil Feature Engineering...")
df = pd.read_csv(file_path).dropna(subset=['Harga'])
print(f"Total data awal: {df.shape[0]} baris")

# =====================================================================
# 2. PEMBERSIHAN OUTLIER MULTIVARIAT (Isolation Forest)
# =====================================================================
print("Membersihkan outlier numerik ekstrem...")
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

# Isolation Forest untuk membuang anomali harga yang tidak rasional terhadap ukuran tanah/bangunan
iso_forest = IsolationForest(contamination=0.015, random_state=42, n_jobs=-1)
outlier_predictions = iso_forest.fit_predict(df_cleaned[['Harga', 'Luas_Tanah', 'Luas_Bangunan']])
df_final = df_cleaned[outlier_predictions == 1].copy()
print(f"Total data setelah pembersihan outlier: {df_final.shape[0]} baris\n")

# =====================================================================
# 3. KATEGORISASI FITUR & TIPE DATA CATEGORICAL NATIVE
# =====================================================================
numeric_features = [
    'Luas_Tanah', 'Luas_Bangunan', 'Rasio_LB_LT', 'Luas_per_Kamar',
    'LT_vs_Median_Kecamatan', 'LB_vs_Median_Kecamatan',
    'Kamar_Tidur_Utama', 'Kamar_Tidur_ART', 'Kamar_Mandi_Utama', 
    'Kamar_Mandi_ART', 'Garasi_Utama', 'Carport', 'Kapasitas_Parkir', 'Rasio_KT_KM'
]

categorical_features = ['Kota', 'Kecamatan/Kawasan', 'Sertifikat']

binary_features = [
    'Ada_ART_Room',
    'Fasilitas_Siap_Huni', 'Fasilitas_Bebas_Banjir', 'Fasilitas_Komplek_Perumahan', 
    'Fasilitas_Dekat_Akses_Transportasi', 'Fasilitas_Dekat_Sekolah', 
    'Fasilitas_Dekat_Pusat_Perbelanjaan', 'Fasilitas_Dekat_Fasilitas_Kesehatan',
    'Fasilitas_Dekat_Tempat_Ibadah', 'Fasilitas_Dekat_Landmark'
]

# Ambil fitur terpilih
X = df_final[numeric_features + categorical_features + binary_features].copy()
y = df_final['Harga']

# UBAH FITUR KATEGORIKAL MENJADI TIPE 'category' (Sangat Penting untuk LightGBM)
for col in categorical_features:
    X[col] = X[col].astype('category')

# Split Data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Log Transform Target
y_train_log = np.log1p(y_train)

# =====================================================================
# 4. TRAINING MODEL LIGHTGBM DENGAN HYPERPARAMETER TEROPTIMASI
# =====================================================================
print("Melatih model LightGBM Regressor (Full Segmentasi)...")
model = LGBMRegressor(
    n_estimators=1200,          # Ditambah agar model belajar lebih dalam
    learning_rate=0.02,         # Diperkecil agar update bobot lebih halus
    num_leaves=255,             # Diperbesar untuk menangkap interaksi spasial yang kompleks
    colsample_bytree=0.8,       # Mengambil 80% fitur acak per pohon untuk mencegah overfitting
    subsample=0.8,              # Mengambil 80% sampel acak untuk mencegah overfitting
    random_state=42,
    n_jobs=-1,
    verbose=-1
)

# Latih Model
model.fit(X_train, y_train_log)

# =====================================================================
# 5. EVALUASI MODEL
# =====================================================================
# Prediksi
y_pred_log = model.predict(X_test)
y_pred = np.expm1(y_pred_log)  # Kembalikan ke Rupiah asli

# Hitung Metrik Evaluasi
r2 = r2_score(y_test, y_pred) * 100
mae = mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred) * 100

print("\n" + "="*50)
print("=== HASIL EVALUASI MODEL FINAL (FULL SEGMENTASI) ===")
print("="*50)
print(f"R2 Score (Akurasi)  : {r2:.2f}%")
print(f"Mean Absolute Error : Rp {mae:,.2f}")
print(f"MAPE (Rata-rata % Error): {mape:.2f}%")
print("="*50)

# =====================================================================
# 6. TAMPILKAN FEATURE IMPORTANCE (Untuk seleksi fitur lanjutan)
# =====================================================================
importances = model.feature_importances_
importances_normalized = (importances / importances.sum()) * 100

df_importance = pd.DataFrame({
    'Fitur': X.columns.tolist(),
    'Tingkat Kepentingan (%)': importances_normalized
}).sort_values(by='Tingkat Kepentingan (%)', ascending=False).reset_index(drop=True)

print("\n=== DAFTAR TINGKAT KEPENTINGAN FITUR (FEATURE IMPORTANCE) ===")
print(df_importance.to_string())