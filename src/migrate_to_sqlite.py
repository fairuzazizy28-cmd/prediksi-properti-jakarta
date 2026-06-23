import pandas as pd
import sqlite3
import joblib
import os
import json

# File paths
CSV_FILE = 'data/processed/dataset_properti_jakarta_master_fe_final.csv'
DB_FILE = 'data/properti.db'
MODEL_PATH = 'models/model_lgbm_properti.pkl'

def format_rupiah(number):
    if number >= 1e9:
        return f"Rp {round(number / 1e9, 2)} M"
    elif number >= 1e6:
        return f"Rp {round(number / 1e6, 2)} Juta"
    return f"Rp {number}"

def migrate():
    print("Mulai proses migrasi ke SQLite...")
    
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    
    # 1. Load CSV into properties table
    print("Membaca CSV utama...")
    df = pd.read_csv(CSV_FILE)
    
    # Save to SQLite
    print("Menyimpan ke tabel 'properties'...")
    df.to_sql('properties', conn, index=False, if_exists='replace')
    
    # Add indexes for fast querying
    print("Membuat Index untuk Kecamatan dan Kota...")
    conn.execute('CREATE INDEX idx_kecamatan ON properties ("Kecamatan/Kawasan")')
    conn.execute('CREATE INDEX idx_kota ON properties ("Kota")')
    conn.execute('CREATE INDEX idx_harga ON properties ("Harga")')
    
    print("Membuat tabel 'opportunities' menggunakan model AI...")
    import pickle
    with open(MODEL_PATH, 'rb') as f:
        paket = pickle.load(f)
    model = paket['model']
    
    all_features = paket['semua_fitur']
    
    # Pastikan urutan fitur sama persis dengan saat model dilatih
    X = df[all_features].copy()
    X.fillna(0, inplace=True)
    
    for col in ['Kota', 'Kecamatan/Kawasan', 'Sertifikat']:
        X[col] = X[col].astype('category')
        
    import numpy as np
    prediksi_log = model.predict(X)
    df['Predicted_Harga'] = np.expm1(prediksi_log)
    
    # Hitung ROI (Seberapa di bawah harga pasar)
    df['ROI_Percent'] = ((df['Predicted_Harga'] - df['Harga']) / df['Harga']) * 100
    
    # Filter hanya Good Deals (ROI > 10%)
    good_deals = df[df['ROI_Percent'] > 10].copy()
    
    opportunities = []
    for _, row in good_deals.iterrows():
        # Gunakan fallback default jika image null, tapi sisakan URL aslinya jika ada
        img = row['Image_URL'] if pd.notna(row['Image_URL']) and str(row['Image_URL']).startswith('http') else None
        
        opportunities.append({
            'id': row['ID'],
            'url': row['URL_ID'],
            'title': row['Deskripsi'] if pd.notna(row['Deskripsi']) else 'Properti Good Deal',
            'location': f"{row['Kecamatan/Kawasan']}, {row['Kota']}",
            'actualPrice': format_rupiah(row['Harga']),
            'aiEstValue': format_rupiah(row['Predicted_Harga']),
            'numericPrice': row['Harga'],
            'numericROI': row['ROI_Percent'],
            'roi': f"{row['ROI_Percent']:.1f}%",
            'discountPercent': int(row['ROI_Percent']),
            'image': img
        })
    
    opp_df = pd.DataFrame(opportunities)
    
    # Simpan ke tabel 'opportunities'
    print(f"Menyimpan {len(opp_df)} properti Good Deal ke tabel 'opportunities'...")
    opp_df.to_sql('opportunities', conn, index=False, if_exists='replace')
    
    # Tambahkan Index untuk ROI (karena sering di-sort)
    conn.execute('CREATE INDEX idx_roi ON opportunities ("numericROI")')
    conn.execute('CREATE INDEX idx_location ON opportunities ("location")')
    conn.execute('CREATE INDEX idx_numprice ON opportunities ("numericPrice")')
    
    conn.close()
    print("Migrasi Database Selesai! File SQLite tersimpan di 'data/properti.db'")

if __name__ == "__main__":
    migrate()
