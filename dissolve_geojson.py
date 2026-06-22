import pandas as pd
import geopandas as gpd
import json

# 1. Load dataset
df = pd.read_csv('data/processed/dataset_properti_jakarta_master_fe2.csv')
mapping = df[['Kecamatan/Kawasan', 'Kota']].drop_duplicates()
kec_to_kota = mapping.set_index('Kecamatan/Kawasan')['Kota'].to_dict()

# 2. Load geojson
with open('frontend/public/jakarta-kota.geojson', 'r') as f:
    geo = json.load(f)

# Add Kota to features
for f in geo['features']:
    kec = f['properties'].get('name')
    # Try exact match
    kota = kec_to_kota.get(kec)
    if not kota:
        # Fallback fuzzy match
        for k in kec_to_kota.keys():
            if str(k).lower() == str(kec).lower():
                kota = kec_to_kota[k]
                break
    
    if not kota:
        print(f"Warning: No match for {kec}")
        kota = "Unknown"
        
    f['properties']['Kota'] = kota

with open('temp_mapped.geojson', 'w') as f:
    json.dump(geo, f)

# 3. Dissolve using geopandas
gdf = gpd.read_file('temp_mapped.geojson')
gdf = gdf[gdf['Kota'] != 'Unknown']

dissolved = gdf.dissolve(by='Kota').reset_index()

# Centroids
dissolved['centroid_lng'] = dissolved.geometry.centroid.x
dissolved['centroid_lat'] = dissolved.geometry.centroid.y

# Drop unneeded columns to keep geojson clean
cols_to_keep = ['Kota', 'centroid_lng', 'centroid_lat', 'geometry']
dissolved = dissolved[cols_to_keep]

# Ensure properties are preserved correctly
dissolved.to_file('frontend/public/jakarta-5-kota.geojson', driver='GeoJSON')
print("Successfully dissolved to 5 Kota!")
