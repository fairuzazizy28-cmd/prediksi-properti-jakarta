import pandas as pd
import json
import time
import urllib.request
import urllib.parse
import os

DATASET_PATH = '../data/processed/dataset_properti_jakarta_master_fe2.csv'
OUTPUT_PATH = '../data/processed/jakarta_coordinates.json'

def get_coordinates(query):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'TaksirinJakarta/1.0 (test@example.com)'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    return None, None

def main():
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    
    # Get unique regions with their city
    unique_regions = df[['Kecamatan/Kawasan', 'Kota']].drop_duplicates()
    
    # Pre-populate with a few hardcoded fallbacks just in case
    coords_dict = {
        'Jakarta Selatan': (-6.2615, 106.8106),
        'Jakarta Pusat': (-6.1805, 106.8284),
        'Jakarta Barat': (-6.1683, 106.7588),
        'Jakarta Timur': (-6.2250, 106.9004),
        'Jakarta Utara': (-6.1214, 106.8770),
    }
    
    print(f"Found {len(unique_regions)} unique regions to geocode.")
    
    results = {}
    for index, row in unique_regions.iterrows():
        kecamatan = row['Kecamatan/Kawasan']
        kota = row['Kota']
        
        # Clean up some common neighborhood names that Nominatim might struggle with
        search_query = f"{kecamatan}, {kota}, DKI Jakarta, Indonesia"
        
        print(f"Geocoding: {search_query}")
        lat, lon = get_coordinates(search_query)
        
        # Fallback to city center if specific region not found
        if lat is None:
            print(f"  -> Not found, trying just the city: {kota}")
            lat, lon = coords_dict.get(kota, (-6.2088, 106.8456)) # default to Central Jakarta
            
        results[kecamatan] = {"lat": lat, "lng": lon}
        time.sleep(1.2) # Nominatim policy: 1 request per second max
        
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"Successfully saved coordinates for {len(results)} regions to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
