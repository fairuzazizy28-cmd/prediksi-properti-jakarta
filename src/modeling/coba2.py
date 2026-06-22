import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_absolute_percentage_error
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest, VotingRegressor

# Import Algoritma Regresi Terbaik
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

# =====================================================================
# 1. LOAD DATASET & OUTLIER REMOVAL
# =====================================================================
file_path = "data/processed/dataset_properti_jakarta_master_fe1.csv"
print("Membaca dataset hasil Feature Engineering...")
df = pd.read_csv(file_path).dropna(subset=['Harga'])

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

# Isolation Forest
iso_forest = IsolationForest(contamination=0.02, random_state=42, n_jobs=-1)
outlier_predictions = iso_forest.fit_predict(df_cleaned[['Harga', 'Luas_Tanah', 'Luas_Bangunan']])
df_final = df_cleaned[outlier_predictions == 1]
print(f"Data setelah pembersihan outlier: {df_final.shape[0]} baris\n")

# =====================================================================
# 2. DEFINISI FITUR & TARGET
# =====================================================================
numeric_features = [
    'Luas_Tanah', 'Luas_Bangunan', 'Rasio_LB_LT', 'Luas_per_Kamar',
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

X = df_final[numeric_features + categorical_features + binary_features]
y = df_final['Harga']

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
y_train_log = np.log1p(y_train)  # Log Transform Target

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median'))]), numeric_features),
        ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), categorical_features),
        ('bin', 'passthrough', binary_features)
    ])

# =====================================================================
# 3. INISIALISASI MODEL (SEMUA DENGAN LOG TRANSFORM TARGET)
# =====================================================================
# Model 1: LightGBM
lgb_model = LGBMRegressor(
    n_estimators=800, learning_rate=0.03, num_leaves=127, 
    random_state=42, n_jobs=-1, verbose=-1
)

# Model 2: XGBoost
xgb_model = XGBRegressor(
    n_estimators=800, learning_rate=0.03, max_depth=7, 
    random_state=42, n_jobs=-1, verbosity=0
)

# Model 3: CatBoost
cat_model = CatBoostRegressor(
    iterations=800, learning_rate=0.05, depth=7, 
    random_state=42, verbose=0, thread_count=-1
)

# Model 4: Ensemble (Voting Regressor - Rata-rata dari ketiganya)
ensemble_model = VotingRegressor(
    estimators=[
        ('lgb', lgb_model),
        ('xgb', xgb_model),
        ('cat', cat_model)
    ],
    n_jobs=-1
)

daftar_model = {
    'LightGBM': lgb_model,
    'XGBoost': xgb_model,
    'CatBoost': cat_model,
    'Ensemble (Gabungan)': ensemble_model
}

# =====================================================================
# 4. TRAINING & EVALUASI
# =====================================================================
hasil_evaluasi = []

for nama, regressor in daftar_model.items():
    print(f"Melatih model: {nama}...")
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', regressor)
    ])
    
    # Train
    pipeline.fit(X_train, y_train_log)
    
    # Predict & Inverse Log Transform
    y_pred_log = pipeline.predict(X_test)
    y_pred = np.expm1(y_pred_log)
    
    # Hitung Metrik
    r2 = r2_score(y_test, y_pred) * 100
    mae = mean_absolute_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
    
    hasil_evaluasi.append({
        'Model': nama,
        'R2 Score (%)': f"{r2:.2f}%",
        'MAE (Rupiah)': f"Rp {mae:,.2f}",
        'MAPE (%)': f"{mape:.2f}%"
    })

# =====================================================================
# 5. TAMPILKAN TABEL HASIL KOMPARASI AKHIR
# =====================================================================
df_hasil = pd.DataFrame(hasil_evaluasi)
print("\n" + "="*70)
print("=== TABEL PERBANDINGAN ALGORITMA TERBAIK (DENGAN LOG TRANSFORM) ===")
print("="*70)
print(df_hasil.to_string(index=False))
print("="*70)