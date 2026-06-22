import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

u = 'https://raw.githubusercontent.com/thetrisatria/geojson-indonesia/master/prov/id-jk.geojson'
try:
    d = json.loads(urllib.request.urlopen(u, context=ctx).read())
    print("Features:", len(d["features"]))
    names = []
    for f in d['features']:
        names.append(f['properties'].get('name', f['properties']))
    print(names)
    with open('frontend/public/jakarta-5-kota.geojson', 'w') as out:
        json.dump(d, out)
except Exception as e:
    print(e)
