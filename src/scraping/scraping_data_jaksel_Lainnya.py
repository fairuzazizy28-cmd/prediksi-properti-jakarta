import re
import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

# BLOK KONFIGURASI 

POPULASI_JAKSEL_TERBARU = 129266  

# Formula Target: Mengambil 10% dari 10% dari populasi Lainnya tersebut
TARGET_SAMPEL = int(POPULASI_JAKSEL_TERBARU * 0.10 * 0.10)  

# URL target 
base_url = 'https://www.rumah123.com/jual/jakarta-selatan/rumah/?certificates%5B%5D=6&certificates%5B%5D=5&certificates%5B%5D=7&certificates%5B%5D=8&certificates%5B%5D=9&certificates%5B%5D=10&certificates%5B%5D=3&certificates%5B%5D=4&maxPrice=50000000000&minPrice=500000000&transactedIncluded=1'
domain_utama = 'https://www.rumah123.com'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Nome file output hasil akhir
NAMA_FILE_OUTPUT = 'data_jaksel_Lainnya_final.csv'
# ==============================================================================

semua_data_properti = []
halaman = 1

print(f"=== STRATIFIED SAMPLING: Lainnya JAKARTA SELATAN ===")
print(f"Populasi Acuan : {POPULASI_JAKSEL_TERBARU}")
print(f"Target Kuota    : {TARGET_SAMPEL} data")
print(f"================================================")

# 2. PERULANGAN TUNGGAL BERDASARKAN HALAMAN
while len(semua_data_properti) < TARGET_SAMPEL:
    # Merakit URL dinamis dengan menambahkan parameter halaman di paling belakang
    url_dinamis = f"{base_url}&page={halaman}"
    
    print(f"\nMengakses Halaman {halaman}...")
    try:
        response = requests.get(url_dinamis, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Proses berhenti. Server merespons dengan Status Code: {response.status_code}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        daftar_properti = soup.find_all('div', {'data-name': 'trackiner-wrapper'})
        
        if len(daftar_properti) == 0:
            print("Halaman kosong. Seluruh data yang tersedia di website sudah habis tersapu.")
            break
            
        print(f"Mengekstrak {len(daftar_properti)} properti dari halaman ini.")

        # ekstraksi data properti satu per satu
        for properti in daftar_properti:
            if len(semua_data_properti) >= TARGET_SAMPEL:
                break

            # Ekstraksi link sebagai Primary Key
            link_elemen = properti.find('a', href=re.compile(r'^/properti/'))
            if link_elemen:
                url_mentah = link_elemen['href']
                url_unik = domain_utama + url_mentah if url_mentah.startswith('/') else url_mentah
            else:
                link_cadangan = properti.find('a', href=True)
                url_unik = link_cadangan['href'] if link_cadangan else "URL tidak ditemukan"

            # Ekstraksi Deskripsi
            deskripsi_elemen = properti.find('h2')
            deskripsi = deskripsi_elemen.text.strip() if deskripsi_elemen else "Deskripsi tidak ditemukan"

            # Ekstraksi Harga
            harga_elemen = properti.find('span', {'data-testid': 'ldp-text-price'})
            harga = harga_elemen.text.strip() if harga_elemen else "Harga tidak ditemukan"

            # Ekstraksi Kawasan
            kawasan_elemen = properti.find('p', {'class': 'text-left font-medium text-greyText text-sm truncate px-4'})
            kawasan = kawasan_elemen.text.strip() if kawasan_elemen else "Kawasan tidak ditemukan"

            # Ekstraksi Kamar Tidur
            kamar_tidur_elemen = 0
            kandidat_kamar_tidur = properti.find_all('span', {'class': 'flex items-center gap-x-1'})
            for span in kandidat_kamar_tidur:
                if 'bedroom-icon' in str(span):
                    kamar_tidur_elemen = span.text.strip()
                    break
            kamar_tidur = kamar_tidur_elemen if kamar_tidur_elemen else "0"

            # Ekstraksi Kamar Mandi
            kamar_mandi_elemen = 0
            kandidat_kamar_mandi = properti.find_all('span', {'class': 'flex items-center gap-x-1'})
            for span in kandidat_kamar_mandi:
                if 'bathroom-icon' in str(span):
                    kamar_mandi_elemen = span.text.strip()
                    break
            kamar_mandi = kamar_mandi_elemen if kamar_mandi_elemen else "0"

            # Ekstraksi Garasi
            garasi_elemen = 0
            kandidat_garasi = properti.find_all('span', {'class': 'flex items-center gap-x-1'})
            for span in kandidat_garasi:
                if 'carports-icon' in str(span):
                    garasi_elemen = span.text.strip()
                    break
            garasi = garasi_elemen if garasi_elemen else "0"

            # Ekstraksi Luas Tanah
            luas_tanah_elemen = 0
            kandidat_luas_tanah = properti.find_all('span', {'class': 'flex'})
            for span in kandidat_luas_tanah:
                if 'LT' in span.text:
                    luas_tanah_elemen = span.text.strip()
                    break
            luas_tanah = luas_tanah_elemen if luas_tanah_elemen else "0"

            # Ekstraksi Luas Bangunan
            luas_bangunan_elemen = 0
            kandidat_luas_bangunan = properti.find_all('span', {'class': 'flex'})
            for span in kandidat_luas_bangunan:
                if 'LB' in span.text:
                    luas_bangunan_elemen = span.text.strip()
                    break
            luas_bangunan = luas_bangunan_elemen if luas_bangunan_elemen else "0"

            # Ekstraksi Kata Kunci
            list_kata_kunci = []
            area_konten = properti.find('div', {'data-name': 'ldp-listing-content'})
            if area_konten:
                wadah_kapsul = area_konten.find('div', class_='no-scrollbar')
                if wadah_kapsul:
                    list_kata_kunci = list(wadah_kapsul.stripped_strings)

            # TABULARISASI & AUTOMATIC LABELING
            data_baris = {
                'URL_ID': url_unik,
                'Deskripsi': deskripsi,
                'Harga': harga,
                'Kawasan': kawasan,
                'Sertifikat': 'Lainnya',  
                'Kamar_Tidur': kamar_tidur,
                'Kamar_Mandi': kamar_mandi,
                'Garasi': garasi,
                'Luas_Tanah': luas_tanah,
                'Luas_Bangunan': luas_bangunan,
                'Kata_Kunci': list_kata_kunci
            }
            
            semua_data_properti.append(data_baris)

        print(f"Progress Saat Ini: {len(semua_data_properti)} / {TARGET_SAMPEL} data diamankan.")

        # sistem checkpoint berkala setiap 100 halaman 
        if halaman % 100 == 0:
            print(f"[SYSTEM] Membuat file cadangan sementara di halaman {halaman}...")
            df_temp = pd.DataFrame(semua_data_properti)
            df_temp.to_csv(f'backup_Lainnya_jaksel_{len(semua_data_properti)}_baris.csv', index=False)

        # setting waktu delay
        jeda = random.uniform(2, 4)
        time.sleep(jeda)
        halaman += 1
        
    except Exception as error_koneksi:
        print(f"Terjadi gangguan jaringan: {error_koneksi}. Mencoba lanjut ke halaman berikutnya...")
        time.sleep(5)
        halaman += 1

print("\n" + "="*50)
print("PROSES SELESAI!")
print(f"Mengonversi {len(semua_data_properti)} baris data ke format DataFrame...")

df_final = pd.DataFrame(semua_data_properti)
df_final.to_csv(NAMA_FILE_OUTPUT, index=False, encoding='utf-8-sig')

print(f"SUKSES! File Berhasil Disimpan dengan nama: '{NAMA_FILE_OUTPUT}'")
print("="*50)