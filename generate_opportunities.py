import pandas as pd
import pickle
import json
import os

# Paths
MODEL_PATH = "models/model_lgbm_properti.pkl"
DATA_PATH = "data/processed/dataset_properti_jakarta_master_fe2.csv"
OUTPUT_PATH = "data/opportunities_cache.json"

print("Loading model and data...")
with open(MODEL_PATH, 'rb') as f:
    paket = pickle.load(f)
    
model = paket['model']
semua_fitur = paket['semua_fitur']

df = pd.read_csv(DATA_PATH)

print("Preparing features...")
# Ensure features match model
X = df[semua_fitur].copy()
for col in ['Kota', 'Kecamatan/Kawasan', 'Sertifikat']:
    if col in X.columns:
        X[col] = X[col].astype('category')

print("Predicting prices...")
import numpy as np
preds_log = model.predict(X)
preds = np.expm1(preds_log)

df['Prediksi_Harga'] = preds

# Filter where actual price is less than prediction
# Discount = (Pred - Actual) / Pred
df['Discount'] = (df['Prediksi_Harga'] - df['Harga']) / df['Prediksi_Harga']

# Only keep ones with positive discount, price > 1 Milyar, to avoid weird data
good_deals = df[(df['Discount'] > 0.15) & (df['Discount'] < 0.60) & (df['Harga'] > 1000000000)].copy()

print(f"Found {len(good_deals)} potential good deals.")

# Sort by Discount
good_deals = good_deals.sort_values('Discount', ascending=False)

# Take all instead of just top 20
top_all = good_deals.copy()

# Format output
output_data = []
for idx, row in top_all.iterrows():
    # Convert numbers to human readable
    def format_rupiah(angka):
        if angka >= 1e9:
            val = float(f"{angka/1e9:.2f}")
            return f"Rp {val:g} M"
        elif angka >= 1e6:
            val = float(f"{angka/1e6:.2f}")
            return f"Rp {val:g} Jt"
        return f"Rp {angka:,.0f}"
        
    # extract title from description roughly
    desc = str(row.get('Deskripsi', f"Rumah di {row['Kecamatan/Kawasan']}"))
    title = desc.split(',')[0][:40] if ',' in desc else desc[:40]
    if not title:
        title = f"Properti di {row['Kecamatan/Kawasan']}"
        
    output_data.append({
        "id": str(row['ID']),
        "url": row['URL_ID'],
        "title": title.title(),
        "location": f"{row['Kecamatan/Kawasan']}, {row['Kota']}",
        "actualPrice": format_rupiah(row['Harga']),
        "aiEstValue": format_rupiah(row['Prediksi_Harga']),
        "discountPercent": f"{int(row['Discount'] * 100)}%",
        "roi": f"{row['Discount'] * 100:.1f}%",
        "lt": str(row['Luas_Tanah']),
        "lb": str(row['Luas_Bangunan']),
        "numericPrice": int(row['Harga']),
        "numericROI": float(row['Discount'] * 100)
    })

with open(OUTPUT_PATH, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"Saved {len(output_data)} opportunities to {OUTPUT_PATH}")
