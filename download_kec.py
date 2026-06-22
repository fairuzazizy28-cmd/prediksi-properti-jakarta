import urllib.request
import json
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
u = 'https://raw.githubusercontent.com/SakifAbdillah/jakartaKecamatanGeoJSON/master/jakarta_kecamatan.geojson'
try:
    d = json.loads(urllib.request.urlopen(u, context=ctx).read())
    print(f'Features: {len(d["features"])}')
    with open('frontend/public/jakarta-kecamatan.geojson', 'w') as f:
        json.dump(d, f)
except Exception as e:
    print(e)
