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
import sqlite3

app = Flask(__name__)
CORS(app) # Enable CORS for React Frontend communication

# Global Variables
MODEL_PATH = "models/model_lgbm_properti.pkl"
DB_PATH = "data/properti.db"
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
median_lt_kec = {}
median_lb_kec = {}
all_features = []
metrik = {}

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def load_assets():
    global paket, model, median_lt_kec, median_lb_kec, all_features, metrik
    try:
        with open(MODEL_PATH, 'rb') as f:
            paket = pickle.load(f)
        model = paket['model']
        median_lt_kec = paket['median_lt_per_kec']
        median_lb_kec = paket['median_lb_per_kec']
        all_features = paket['semua_fitur']
        metrik = paket['metrik']
        print("Models loaded successfully.")
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


@app.route("/api/recommend", methods=["POST"])
def get_recommendation():
    try:
        req = request.json
        kecamatan = req.get('kecamatan', '')
        kota = req.get('kota', '')
        luas_tanah = req.get('luas_tanah', 0)
        luas_bangunan = req.get('luas_bangunan', 0)
        kt_utama = req.get('kt_utama', 0)
        km_utama = req.get('km_utama', 0)
        carport = req.get('carport', 0)
        fasilitas_terpilih = req.get('fasilitas_terpilih', [])
        harga_prediksi = req.get('harga_prediksi', 0)
        top_n = req.get('top_n', 50) # Request more for pagination

        valid_fas_columns = [DAFTAR_FASILITAS[f] for f in fasilitas_terpilih if f in DAFTAR_FASILITAS]
        if valid_fas_columns:
            matches_sql = " + ".join([f'"{col}"' for col in valid_fas_columns])
            keyword_sql = f"(1.0 - ((CAST({matches_sql} AS FLOAT)) / {len(valid_fas_columns)})) * 0.15"
        else:
            keyword_sql = "0.0"

        # Handle zero division by ensuring denominator > 0
        p_harga = harga_prediksi if harga_prediksi > 0 else 1.0
        p_lt = luas_tanah if luas_tanah > 0 else 1.0
        p_lb = luas_bangunan if luas_bangunan > 0 else 1.0
        p_kt = kt_utama if kt_utama > 0 else 1.0
        p_km = km_utama if km_utama > 0 else 1.0
        p_cp = carport if carport > 0 else 1.0

        query = f"""
        SELECT *, 
          (ABS(Harga - ?) / ?) * 0.30 +
          (ABS(Luas_Tanah - ?) / ?) * 0.15 +
          (ABS(Luas_Bangunan - ?) / ?) * 0.15 +
          (ABS(Kamar_Tidur_Utama - ?) / ?) * 0.10 +
          (ABS(Kamar_Mandi_Utama - ?) / ?) * 0.10 +
          (ABS(Carport - ?) / ?) * 0.05 +
          (CASE WHEN "Kecamatan/Kawasan" = ? THEN 0.0 ELSE 2.0 END) +
          {keyword_sql} AS Skor_Kemiripan
        FROM properties
        WHERE "Kota" = ?
        ORDER BY Skor_Kemiripan ASC
        LIMIT ?
        """
        params = (
            harga_prediksi, p_harga,
            luas_tanah, p_lt,
            luas_bangunan, p_lb,
            kt_utama, p_kt,
            km_utama, p_km,
            carport, p_cp,
            kecamatan, kota, top_n
        )
        
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        rekomendasi = [dict(row) for row in rows]
        conn.close()

        return jsonify({
            'status': 'success',
            'rekomendasi': rekomendasi
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/affordability", methods=["POST"])
def get_affordability_heatmap():
    try:
        req = request.json
        max_harga = req.get('max_harga', 0)
        
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Total affordable count
        cursor.execute("SELECT COUNT(*) FROM properties WHERE Harga <= ?", (max_harga,))
        total_affordable = cursor.fetchone()[0]
        
        # Kota counts
        cursor.execute("SELECT Kota, COUNT(*) FROM properties WHERE Harga <= ? GROUP BY Kota", (max_harga,))
        kota_counts = dict(cursor.fetchall())
        
        # Mapping Kecamatan to Kota
        cursor.execute('SELECT "Kecamatan/Kawasan", "Kota" FROM properties GROUP BY "Kecamatan/Kawasan"')
        kecamatan_to_kota = dict(cursor.fetchall())
        
        # Recommendations (Return 500 per kota for pagination)
        recommendations = {}
        for kota in kota_counts.keys():
            if not kota: continue
            cursor.execute("SELECT * FROM properties WHERE Harga <= ? AND Kota = ? ORDER BY Harga DESC LIMIT 500", (max_harga, kota))
            recommendations[kota] = [dict(row) for row in cursor.fetchall()]
            
        cursor.execute("SELECT * FROM properties WHERE Harga <= ? ORDER BY Harga DESC LIMIT 500", (max_harga,))
        recommendations['All'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
                
        return jsonify({
            'status': 'success',
            'kota_counts': {str(k): int(v) for k, v in kota_counts.items()},
            'kecamatan_to_kota': kecamatan_to_kota,
            'total_affordable': int(total_affordable),
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/opportunities", methods=["GET"])
def get_opportunities():
    try:
        min_discount = int(request.args.get('min_discount', 25))
        location = request.args.get('location', 'Seluruh Jakarta').lower().replace('jakarta ', '')
        sort_by = request.args.get('sort', 'roi_desc')

        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        where_clause = "numericROI >= ?"
        params = [min_discount]
        
        if location != 'seluruh jakarta' and location != 'seluruh':
            where_clause += " AND LOWER(location) LIKE ?"
            params.append(f"%{location}%")
            
        order_clause = ""
        if sort_by == 'roi_desc': order_clause = "ORDER BY numericROI DESC"
        elif sort_by == 'roi_asc': order_clause = "ORDER BY numericROI ASC"
        elif sort_by == 'price_desc': order_clause = "ORDER BY numericPrice DESC"
        elif sort_by == 'price_asc': order_clause = "ORDER BY numericPrice ASC"
        
        # Return up to 1000 opportunities for pagination
        query = f"SELECT * FROM opportunities WHERE {where_clause} {order_clause} LIMIT 1000"
        cursor.execute(query, params)
        opportunities = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Default images array for the few that might still fail
        FALLBACK_IMAGES = [
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=2075&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?q=80&w=2070&auto=format&fit=crop"
        ]
        
        # Ensure fallback for null images
        for item in opportunities:
            if not item.get('image'):
                fallback_idx = abs(hash(item.get('url', ''))) % len(FALLBACK_IMAGES)
                item['image'] = FALLBACK_IMAGES[fallback_idx]
        
        return jsonify({
            'status': 'success',
            'data': opportunities
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
