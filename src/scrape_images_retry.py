import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import os
import csv
import random
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# File paths
INPUT_CSV = 'data/processed/dataset_properti_jakarta_master_fe2.csv'
OUTPUT_CSV = 'data/processed/dataset_properti_jakarta_master_fe3_images.csv'

# User Agents untuk menghindari blokir
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

# 1. Baca dataset utama
df_master = pd.read_csv(INPUT_CSV)
total_master = len(df_master)

# 2. Cari ID mana yang SUDAH berhasil (punya link gambar)
successful_ids = set()
if os.path.exists(OUTPUT_CSV):
    try:
        df_existing = pd.read_csv(OUTPUT_CSV)
        # Ambil hanya baris yang Image_URL nya tidak kosong dan diawali 'http'
        if 'Image_URL' in df_existing.columns:
            valid_rows = df_existing[df_existing['Image_URL'].str.startswith('http', na=False)]
            successful_ids = set(valid_rows['ID'].tolist())
    except Exception as e:
        print(f"Bisa mengabaikan error baca: {e}")

# 3. Saring URL yang BELUM berhasil
urls_to_process = df_master[~df_master['ID'].isin(successful_ids)][['ID', 'URL_ID']]

print(f"Total data master: {total_master}")
print(f"Sudah Sukses (Gambar Valid): {len(successful_ids)}")
print(f"Sisa yang harus di-scrape (bolong-bolong): {len(urls_to_process)}")

def get_session():
    session = requests.Session()
    # Otomatis retry jika server error (500, 502, 503, 504) atau 429 (Too Many Requests)
    retry = Retry(connect=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_image_url(row):
    url_id = row['URL_ID']
    idx = row['ID']
    
    if not isinstance(url_id, str) or not url_id.startswith('http'):
        return None
        
    session = get_session()
    
    # Coba maksimal 2 kali untuk setiap URL jika di blokir (403)
    for attempt in range(2):
        try:
            time.sleep(random.uniform(0.5, 2.0))
            
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }
            
            response = session.get(url_id, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                og_img = soup.find('meta', property='og:image')
                if og_img and og_img.get('content') and og_img['content'].startswith('http'):
                    return {'ID': idx, 'Image_URL': og_img['content']}
                else:
                    return None # Halaman sukses tapi tidak ada gambar
            elif response.status_code in [403, 401]:
                # Kena blokir anti-bot, tidur sebentar
                time.sleep(random.uniform(3.0, 7.0))
            else:
                return None
                
        except Exception:
            time.sleep(2)
            
    return None

file_exists = os.path.exists(OUTPUT_CSV)
with open(OUTPUT_CSV, mode='a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    if not file_exists or os.path.getsize(OUTPUT_CSV) == 0:
        writer.writerow(['ID', 'Image_URL'])
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(get_image_url, row): row for _, row in urls_to_process.iterrows()}
        
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Scraping Missing Images"):
            result = future.result()
            # HANYA SIMPAN JIKA BERHASIL (Agar yang gagal bisa diulang lagi di masa depan)
            if result is not None and result.get('Image_URL'):
                writer.writerow([result['ID'], result['Image_URL']])
                f.flush()

print("Scraping Selesai! Jangan lupa jalankan merge_images.py lagi.")
