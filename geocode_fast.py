import pandas as pd
import json
import random

df = pd.read_csv('data/processed/dataset_properti_jakarta_master_fe2.csv')
cities = {
    'Jakarta Selatan': (-6.2615, 106.8106),
    'Jakarta Pusat': (-6.1805, 106.8284),
    'Jakarta Barat': (-6.1683, 106.7588),
    'Jakarta Timur': (-6.2250, 106.9004),
    'Jakarta Utara': (-6.1214, 106.8770)
}
res = {}

for _, r in df[['Kecamatan/Kawasan', 'Kota']].drop_duplicates().iterrows():
    c = cities.get(r['Kota'], (-6.2088, 106.8456))
    res[r['Kecamatan/Kawasan']] = {
        'lat': c[0] + random.uniform(-0.02, 0.02),
        'lng': c[1] + random.uniform(-0.02, 0.02)
    }

with open('data/processed/jakarta_coordinates.json', 'w') as f:
    json.dump(res, f)
