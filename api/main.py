from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import json

app = Flask(__name__)
CORS(app) # Enable CORS for React Frontend communication

# Global Variables
MODEL_PATH = "models/model_lgbm_properti.pkl"
DATA_PATH = "data/processed/dataset_properti_jakarta_master_fe2.csv"
DAFTAR_FASILITAS = {
    'Siap Huni':                   'Fasilitas_Siap_Huni',
    'Bebas Banjir':                'Fasilitas_Bebas_Banjir',
    'Komplek Perumahan':           'Fasilitas_Komplek_Perumahan',
    'Dekat Akses Transportasi':    'Fasilitas_Dekat_Akses_Transportasi',
    'Dekat Sekolah':               'Fasilitas_Dekat_Sekolah',
    'Dekat Pusat Perbelanjaan':    'Fasilitas_Dekat_Pusat_Perbelanjaan',
    'Dekat Fasilitas Kesehatan':   'Fasilitas_Dekat_Fasilitas_Kesehatan',
    'Dekat Tempat Ibadah':         'Fasilitas_Dekat_Tempat_Ibadah',
    'Dekat Tempat Wisata':         'Fasilitas_Dekat_Tempat_Wisata',
    'Dekat Landmark':              'Fasilitas_Dekat_Landmark',
}

paket = None
model = None
df_master = None
median_lt_kec = {}
median_lb_kec = {}
all_features = []
metrik = {}

def load_assets():
    global paket, model, df_master, median_lt_kec, median_lb_kec, all_features, metrik
    try:
        with open(MODEL_PATH, 'rb') as f:
            paket = pickle.load(f)
        model = paket['model']
        median_lt_kec = paket['median_lt_per_kec']
        median_lb_kec = paket['median_lb_per_kec']
        all_features = paket['semua_fitur']
        metrik = paket['metrik']
        
        df_master = pd.read_csv(DATA_PATH)
        print("Models and Dataset loaded successfully.")
    except Exception as e:
        print(f"Error loading assets: {e}")

# Load assets on startup
load_assets()

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"message": "JKT PropTech API is running", "status": "OK"})

@app.route("/api/predict", methods=["POST"])
def predict_price():
    if model is None:
        return jsonify({"error": "Model is not loaded."}), 500
        
    try:
        req = request.json
        # 1. Bangun Input Features
        luas_tanah = req.get('luas_tanah', 0)
        luas_bangunan = req.get('luas_bangunan', 0)
        kt_utama = req.get('kt_utama', 0)
        km_utama = req.get('km_utama', 0)
        kt_art = req.get('kt_art', 0)
        km_art = req.get('km_art', 0)
        garasi = req.get('garasi', 0)
        carport = req.get('carport', 0)
        sertifikat = req.get('sertifikat', '')
        kecamatan = req.get('kecamatan', '')
        kota = req.get('kota', '')
        fasilitas_terpilih = req.get('fasilitas_terpilih', [])

        rasio_lb_lt = luas_bangunan / luas_tanah if luas_tanah > 0 else 1.0
        kapasitas_parkir = garasi + carport
        rasio_kt_km = kt_utama / km_utama if km_utama > 0 else kt_utama
        ada_art = 1 if (kt_art > 0 or km_art > 0) else 0
        luas_per_kamar = luas_bangunan / (kt_utama + 1)
        is_shm = 1 if sertifikat == 'SHM' else 0

        med_lt = median_lt_kec.get(kecamatan, luas_tanah)
        med_lb = median_lb_kec.get(kecamatan, luas_bangunan)
        lt_vs_median = luas_tanah / med_lt if med_lt > 0 else 1.0
        lb_vs_median = luas_bangunan / med_lb if med_lb > 0 else 1.0

        fitur_biner = {}
        for nama_display, nama_kolom in DAFTAR_FASILITAS.items():
            fitur_biner[nama_kolom] = 1 if nama_display in fasilitas_terpilih else 0

        data = {
            'Luas_Tanah': luas_tanah,
            'Luas_Bangunan': luas_bangunan,
            'Rasio_LB_LT': rasio_lb_lt,
            'Luas_per_Kamar': luas_per_kamar,
            'LT_vs_Median_Kecamatan': lt_vs_median,
            'LB_vs_Median_Kecamatan': lb_vs_median,
            'Kamar_Tidur_Utama': kt_utama,
            'Kamar_Tidur_ART': kt_art,
            'Kamar_Mandi_Utama': km_utama,
            'Kamar_Mandi_ART': km_art,
            'Garasi_Utama': garasi,
            'Carport': carport,
            'Kapasitas_Parkir': kapasitas_parkir,
            'Rasio_KT_KM': rasio_kt_km,
            'Kota': kota,
            'Kecamatan/Kawasan': kecamatan,
            'Sertifikat': sertifikat,
            'Is_SHM': is_shm,
            'Ada_ART_Room': ada_art,
            **fitur_biner
        }
        
        df_input = pd.DataFrame([data])
        df_input = df_input[all_features]
        for col in ['Kota', 'Kecamatan/Kawasan', 'Sertifikat']:
            df_input[col] = df_input[col].astype('category')

        # 2. Lakukan Prediksi
        prediksi_log = model.predict(df_input)
        harga_prediksi = float(np.expm1(prediksi_log[0]))

        # 3. Hitung Batas Kepercayaan
        mape_val = metrik['mape'] / 100
        batas_bawah = harga_prediksi * (1 - mape_val)
        batas_atas = harga_prediksi * (1 + mape_val)
        
        return jsonify({
            "harga_prediksi": harga_prediksi,
            "batas_bawah": batas_bawah,
            "batas_atas": batas_atas,
            "metrik": metrik
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

import time
import random

def scrape_rumah123_image(url):
    try:
        # Add random delay to prevent 429 rate limit
        time.sleep(random.uniform(0.3, 0.8))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            og_img = soup.find('meta', property='og:image')
            if og_img:
                return og_img['content']
    except Exception:
        pass
    return None

@app.route("/api/recommend", methods=["POST"])
def get_recommendation():
    if df_master is None:
        return jsonify({"error": "Dataset is not loaded."}), 500
        
    try:
        req = request.json
        kecamatan = req.get('kecamatan', '')
        kota = req.get('kota', '')
        luas_tanah = req.get('luas_tanah', 0)
        luas_bangunan = req.get('luas_bangunan', 0)
        harga_prediksi = req.get('harga_prediksi', 0)
        kt_utama = req.get('kt_utama', 0)
        km_utama = req.get('km_utama', 0)
        carport = req.get('carport', 0)
        fasilitas = req.get('fasilitas_terpilih', [])
        top_n = req.get('top_n', 4)

        df_lokasi = df_master[df_master['Kecamatan/Kawasan'] == kecamatan]
        if len(df_lokasi) < 3:
            df_lokasi = df_master[df_master['Kota'] == kota]
        if len(df_lokasi) == 0:
            return jsonify({"rekomendasi": []})

        df_lokasi = df_lokasi.copy()
        
        # Jarak dasar (Harga dan Luas)
        selisih_lt = np.abs(df_lokasi['Luas_Tanah'] - luas_tanah) / max(luas_tanah, 1)
        selisih_lb = np.abs(df_lokasi['Luas_Bangunan'] - luas_bangunan) / max(luas_bangunan, 1)
        selisih_harga = np.abs(df_lokasi['Harga'] - harga_prediksi) / max(harga_prediksi, 1)
        
        # Jarak tambahan (Kamar dan Garasi) - Maksimal penyimpangan 1.0 (100%) agar jika tidak masuk akal, Harga & Luas ambil alih
        selisih_kt = np.minimum(np.abs(df_lokasi['Kamar_Tidur_Utama'] - kt_utama) / max(kt_utama, 1), 1.0)
        selisih_km = np.minimum(np.abs(df_lokasi['Kamar_Mandi_Utama'] - km_utama) / max(km_utama, 1), 1.0)
        selisih_carport = np.minimum(np.abs(df_lokasi['Carport'] - carport) / max(carport, 1), 1.0)
        
        # Pengecekan Keyword (Fasilitas Tambahan)
        keyword_score = np.zeros(len(df_lokasi))
        if fasilitas:
            fas_map = {
                'Siap Huni': 'Fasilitas_Siap_Huni',
                'Bebas Banjir': 'Fasilitas_Bebas_Banjir',
                'Komplek Perumahan': 'Fasilitas_Komplek_Perumahan',
                'Dekat Akses Transportasi': 'Fasilitas_Dekat_Akses_Transportasi',
                'Dekat Sekolah': 'Fasilitas_Dekat_Sekolah',
                'Dekat Pusat Perbelanjaan': 'Fasilitas_Dekat_Pusat_Perbelanjaan',
                'Dekat Fasilitas Kesehatan': 'Fasilitas_Dekat_Fasilitas_Kesehatan',
                'Dekat Tempat Ibadah': 'Fasilitas_Dekat_Tempat_Ibadah',
                'Dekat Tempat Wisata': 'Fasilitas_Dekat_Tempat_Wisata',
                'Dekat Landmark': 'Fasilitas_Dekat_Landmark'
            }
            valid_fas = [fas_map[f] for f in fasilitas if f in fas_map and fas_map[f] in df_lokasi.columns]
            if valid_fas:
                matches = df_lokasi[valid_fas].sum(axis=1)
                # Semakin sedikit match, semakin tinggi nilai penaltinya
                keyword_score = 1.0 - (matches / len(valid_fas))

        # Skor Kemiripan Terpadu (Semakin kecil semakin baik)
        df_lokasi['Skor_Kemiripan'] = (
            (selisih_harga * 0.30) +
            (selisih_lt * 0.15) + (selisih_lb * 0.15) +
            (selisih_kt * 0.10) + (selisih_km * 0.10) + (selisih_carport * 0.05) +
            (keyword_score * 0.15)
        )
        
        rekomendasi_df = df_lokasi.sort_values(by='Skor_Kemiripan').head(top_n)
        rekomendasi = rekomendasi_df.replace({np.nan: None}).to_dict(orient="records")
        
        # Scrape images concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=top_n) as executor:
            future_to_item = {executor.submit(scrape_rumah123_image, item.get('URL_ID')): item for item in rekomendasi}
            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                item['Image_URL'] = future.result()
        
        return jsonify({
            'status': 'success',
            'rekomendasi': rekomendasi
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/affordability", methods=["POST"])
def get_affordability_heatmap():
    if df_master is None:
        return jsonify({"error": "Dataset is not loaded."}), 500
        
    try:
        req = request.json
        max_harga = req.get('max_harga', 0)
        
        affordable_df = df_master[df_master['Harga'] <= max_harga]
        kota_counts = affordable_df.groupby('Kota').size().to_dict()
        
        # Mapping Kecamatan to Kota for frontend GeoJSON matching (if still needed)
        mapping_df = df_master[['Kecamatan/Kawasan', 'Kota']].drop_duplicates()
        kecamatan_to_kota = mapping_df.set_index('Kecamatan/Kawasan')['Kota'].to_dict()
        
        # Recommendations
        recommendations = {}
        safe_df = affordable_df.fillna(0)
        for kota in safe_df['Kota'].unique():
            if pd.isna(kota): continue
            kota_df = safe_df[safe_df['Kota'] == kota].sort_values('Harga', ascending=False).head(10)
            recommendations[str(kota)] = kota_df.to_dict('records')
            
        recommendations['All'] = safe_df.sort_values('Harga', ascending=False).head(10).to_dict('records')
                
        return jsonify({
            'status': 'success',
            'kota_counts': {str(k): int(v) for k, v in kota_counts.items()},
            'kecamatan_to_kota': kecamatan_to_kota,
            'total_affordable': int(len(affordable_df)),
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/opportunities", methods=["GET"])
def get_opportunities():
    try:
        cache_path = "data/opportunities_cache.json"
        if not os.path.exists(cache_path):
            return jsonify({"error": "Cache not found"}), 404
            
        with open(cache_path, 'r') as f:
            opportunities = json.load(f)
            
        min_discount = int(request.args.get('min_discount', 25))
        location = request.args.get('location', 'Seluruh Jakarta').lower().replace('jakarta ', '')
        sort_by = request.args.get('sort', 'roi_desc')

        filtered_opps = []
        for opp in opportunities:
            if opp.get('numericROI', 0) < min_discount:
                continue
            if location != 'seluruh jakarta' and location not in opp['location'].lower():
                continue
            filtered_opps.append(opp)
            
        if sort_by == 'roi_desc':
            filtered_opps.sort(key=lambda x: x.get('numericROI', 0), reverse=True)
        elif sort_by == 'roi_asc':
            filtered_opps.sort(key=lambda x: x.get('numericROI', 0))
        elif sort_by == 'price_desc':
            filtered_opps.sort(key=lambda x: x.get('numericPrice', 0), reverse=True)
        elif sort_by == 'price_asc':
            filtered_opps.sort(key=lambda x: x.get('numericPrice', 0))
            
        # Limit to 20
        opportunities = filtered_opps[:20]
        
        FALLBACK_IMAGES = [
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=2075&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1510798831971-661eb04b3739?q=80&w=2000&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?q=80&w=2074&auto=format&fit=crop"
        ]
        
        # Scrape images concurrently with reduced workers and jitter to prevent 429
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_item = {executor.submit(scrape_rumah123_image, item.get('url')): item for item in opportunities}
            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                fallback_idx = abs(hash(item.get('url', ''))) % len(FALLBACK_IMAGES)
                consistent_fallback = FALLBACK_IMAGES[fallback_idx]
                try:
                    img_url = future.result()
                    item['image'] = img_url if img_url else consistent_fallback
                except Exception:
                    item['image'] = consistent_fallback
        
        return jsonify({
            'status': 'success',
            'data': opportunities
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
