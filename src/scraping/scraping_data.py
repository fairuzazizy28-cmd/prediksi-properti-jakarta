import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.rumah123.com/jual/dki-jakarta/rumah/?maxPrice=50000000000&minPrice=100000000'
domain_utama = 'https://www.rumah123.com'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# melakukan permintaan GET ke URL dengan header yang ditentukan
response = requests.get(url, headers=headers)
print('Status Code:', response.status_code)

semua_data_properti = []
halaman = 1

# # cek sample scrap harga
# soup = BeautifulSoup(response.text, 'html.parser')
# harga_elemen = soup.find('span', {'data-testid': 'ldp-text-price'})
# if harga_elemen:
#     print("Data mentah ditemukan:", harga_elemen.text)
# else:
#     print("Elemen tidak ditemukan. Struktur HTML mungkin dimuat secara dinamis oleh JavaScript.")

# kawasan_elemen = soup.find('p', {'class': 'text-left font-medium text-greyText text-sm truncate px-4'})
# if kawasan_elemen:
#     print("Data mentah ditemukan:", kawasan_elemen.text)
# else:    print("Elemen tidak ditemukan. Struktur HTML mungkin dimuat secara dinamis oleh JavaScript.")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Mencari Semua Wadah Utama (Kartu Properti)
    # menggunakan data-name karena kemungkinan besar atribut ini konstan untuk semua rumah
    daftar_properti = soup.find_all('div', {'data-name': 'trackiner-wrapper'})
    print(f"Ditemukan {len(daftar_properti)} properti di halaman ini.\n")

    # bedah tiap properti satu per satu
    for index, properti in enumerate(daftar_properti,start=1):

        #ekstraksi link properti
        link_elemen = properti.find('a', href=re.compile(r'^/properti/'))
        
        if link_elemen:
            url_mentah = link_elemen['href']
            if url_mentah.startswith('/'):
                url_unik = domain_utama + url_mentah
            else:
                url_unik = url_mentah
        else:
            # Jika tidak ditemukan yang berawalan /properti/, kita ambil a href apa saja sebagai cadangan
            link_cadangan = properti.find('a', href=True)
            url_unik = link_cadangan['href'] if link_cadangan else "URL tidak ditemukan"
            
        print(f"Properti {index}: Primary Key (URL) - {url_unik}")

        # ekstraksi deskripsi
        deskripsi_elemen = properti.find('h2')
        deskripsi = deskripsi_elemen.text.strip() if deskripsi_elemen else "Deskripsi tidak ditemukan"
        print(f"Properti {index}: Deskripsi - {deskripsi}")

        # ekstraksi harga
        harga_elemen = properti.find('span', {'data-testid': 'ldp-text-price'})
        harga = harga_elemen.text.strip() if harga_elemen else "Harga tidak ditemukan"
        print(f"Properti {index}: Harga - {harga}")

        # ekstraksi kawasan
        kawasan_elemen = properti.find('p', {'class': 'text-left font-medium text-greyText text-sm truncate px-4'})
        kawasan = kawasan_elemen.text.strip() if kawasan_elemen else "Kawasan tidak ditemukan"
        print(f"Properti {index}: Kawasan - {kawasan}")

        # ekstaraksi Kamar Tidur
        kamar_tidur_elemen = 0
        kandidat_kamar_tidur = properti.find_all('span', {'class': 'flex items-center gap-x-1'})
        for span in kandidat_kamar_tidur:
            if 'bedroom-icon' in str(span):
                kamar_tidur_elemen = span.text.strip()
                break

        kamar_tidur = kamar_tidur_elemen if kamar_tidur_elemen else "Kamar tidur tidak ditemukan"
        print(f"Properti {index}: Kamar Tidur - {kamar_tidur}")

        # ekstraksi Kamar Mandi
        kamar_mandi_elemen = 0
        kandidat_kamar_mandi = properti.find_all('span', {'class': 'flex items-center gap-x-1'})
        for span in kandidat_kamar_mandi:
            if 'bathroom-icon' in str(span):
                kamar_mandi_elemen = span.text.strip()
                break

        kamar_mandi = kamar_mandi_elemen if kamar_mandi_elemen else "Kamar mandi tidak ditemukan"
        print(f"Properti {index}: Kamar Mandi - {kamar_mandi}")

        # ektraksi Garasi
        garasi_elemen = 0
        kandidat_garasi = properti.find_all('span', {'class': 'flex items-center gap-x-1'})
        for span in kandidat_garasi:
            if 'carports-icon' in str(span):
                garasi_elemen = span.text.strip()
                break
        
        garasi = garasi_elemen if garasi_elemen else "Garasi tidak ditemukan"
        print(f"Properti {index}: Garasi - {garasi}")

        # ektraksi Luas Tanah
        luas_tanah_elemen = 0
        kandidat_luas_tanah = properti.find_all('span', {'class': 'flex'})
        for span in kandidat_luas_tanah:
            if 'LT' in span.text:
                luas_tanah_elemen = span.text.strip()
                break
        
        luas_tanah = luas_tanah_elemen if luas_tanah_elemen else "Luas tanah tidak ditemukan"
        print(f"Properti {index}: Luas Tanah - {luas_tanah}")

        # ektraksi Luas Bangunan
        luas_bangunan_elemen = 0
        kandidat_luas_bangunan = properti.find_all('span', {'class': 'flex'})
        for span in kandidat_luas_bangunan:
            if 'LB' in span.text:
                luas_bangunan_elemen = span.text.strip()
                break

        luas_bangunan = luas_bangunan_elemen if luas_bangunan_elemen else "Luas bangunan tidak ditemukan"
        print(f"Properti {index}: Luas Bangunan - {luas_bangunan}")

        # ekstraksi kata kunci
        list_kata_kunci = []
        area_konten = properti.find('div', {'data-name': 'ldp-listing-content'})
        if area_konten:
            #menggunakan kata kunci 'no-scrollbar' karena kemungkinan besar kelas yang digunakan untuk menampung kata kunci di dalam kartu properti saja
            wadah_kapsul = area_konten.find('div', class_='no-scrollbar')
            if wadah_kapsul:
                list_kata_kunci = list(wadah_kapsul.stripped_strings)
                
        print(f"Properti {index}: Kata Kunci - {list_kata_kunci}\n{'='*50}\n")





