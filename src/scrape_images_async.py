import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import os
import csv
from tqdm import tqdm

# File paths
INPUT_CSV = 'data/processed/dataset_properti_jakarta_master_fe2.csv'
OUTPUT_CSV = 'data/processed/dataset_properti_jakarta_master_fe3_images.csv'

# Read the existing dataset
df = pd.read_csv(INPUT_CSV)
total_rows = len(df)

# Setup output file (Create if not exists, or append if it does for resume capability)
file_exists = os.path.exists(OUTPUT_CSV)

# If we are resuming, we need to know which URLs we already scraped
processed_urls = set()
if file_exists:
    try:
        df_existing = pd.read_csv(OUTPUT_CSV)
        if 'URL_ID' in df_existing.columns and 'Image_URL' in df_existing.columns:
            processed_urls = set(df_existing['URL_ID'].dropna().tolist())
    except Exception as e:
        print(f"Bisa mengabaikan error baca: {e}")

# Filter URLs to process
urls_to_process = df[~df['URL_ID'].isin(processed_urls)][['ID', 'URL_ID']]

print(f"Total data: {total_rows}")
print(f"Sudah diproses: {len(processed_urls)}")
print(f"Sisa yang harus di-scrape: {len(urls_to_process)}")

import random

def get_image_url(row):
    url_id = row['URL_ID']
    idx = row['ID']
    
    if not isinstance(url_id, str) or not url_id.startswith('http'):
        return {'ID': idx, 'Image_URL': ''}
        
    try:
        # Add random delay to prevent IP block
        time.sleep(random.uniform(0.5, 1.5))
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Timeout 10 seconds to avoid hanging
        response = requests.get(url_id, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # The most reliable image for Rumah123 is usually in the OG meta tag
            og_img = soup.find('meta', property='og:image')
            img_url = og_img['content'] if og_img else ''
            return {'ID': idx, 'Image_URL': img_url}
        else:
            return {'ID': idx, 'Image_URL': ''}
    except Exception as e:
        return {'ID': idx, 'Image_URL': ''}

# We use append mode so we don't lose data if the script crashes
with open(OUTPUT_CSV, mode='a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write header if file is empty
    if not file_exists or os.path.getsize(OUTPUT_CSV) == 0:
        writer.writerow(['ID', 'Image_URL'])
        
    # We use ThreadPoolExecutor to speed up the requests
    # Use 3 workers to not hammer the server too hard (avoid IP block)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        futures = {executor.submit(get_image_url, row): row for _, row in urls_to_process.iterrows()}
        
        # Process as they complete
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Scraping Images"):
            result = future.result()
            writer.writerow([result['ID'], result['Image_URL']])
            f.flush() # Ensure data is written to disk immediately

print("Scraping selesai! Jalankan script penggabung (jika diperlukan) atau gunakan merge_images.py")
