# File: jarak_logic.py

import math

# Mendefinisikan koordinat untuk tempat-tempat populer
lokasi_populer = {
    "Jalan Malioboro": (-7.7928, 110.3658), 
    "Prawirotaman": (-7.8190, 110.3706),  
    "Alun-Alun Kidul": (-7.8117, 110.3632),  
    "Alun-Alun Lor" : (-7.8036, 110.3643),
    "Tugu Yogyakarta": (-7.7828, 110.3670), 
    "Pasar Beringharjo": (-7.7985, 110.3657),
    "Museum Affandi" : (-7.7826, 110.3964),
    "Kebun Binatang Gembira Loka" : (-7.8059, 110.3966),
    "Jogja National Museum" : (-7.7998, 110.3533),
    "Titik Nol Kilometer" : (-7.8011, 110.3647),
    "Taman Pintar Yogyakarta" : (-7.8004, 110.3676),
    "Jalan Sosrowijayan" : (-7.7913, 110.3637),
    "Jalan Prawirotaman II" : (-7.8200, 110.3707),
    "Stasiun Tugu Yogyakarta" : (-7.7890, 110.3629), 
    "Jalan Kaliurang" : (-7.7110, 110.4082),
    "Jalan Magelang" : (-7.7418, 110.3626),
    "Jalan Solo" : (-7.7667, 110.4715),
    "Jalan Affandi" : (-7.7694, 110.3901),
    "Stasiun Lempuyangan" : (-7.7902, 110.3754),
    "Bandara Adisucipto" : (-7.7887, 110.4305)
}

# Mendefinisikan koordinat untuk tempat wisata
tempat_wisata = {
    "Keraton Kotagede": (-7.82969, 110.39771),
    "Keraton Ngayogyakarta Hadiningrat": (-7.80506, 110.36420),
    "Situs Taman Sari": (-7.80991, 110.35953),
    "Situs Warungboto": (-7.80913, 110.39319),
    "Kelenteng Fuk Ling Miau": (-7.80112, 110.36961),
    "Museum Sasmitaloka Panglima Besar Jenderal Soedirman": (-7.80211, 110.37547),
    "Museum Benteng Vredeburg": (-7.79957, 110.36612),
    "Monumen Yogya Kembali": (-7.74870, 110.36965),
    "Monumen Serangan Umum Satu Maret": (-7.80048, 110.36522),
    "Museum Kereta": (-7.80474, 110.36285)
}

# Fungsi untuk menghitung jarak menggunakan formula Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius Bumi dalam kilometer
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

# Fungsi untuk mengonversi nama tempat menjadi koordinat
def cari_koordinat_tempat(nama_tempat):
    return lokasi_populer.get(nama_tempat)

# Fungsi untuk menghitung jarak tempat wisata terdekat dari nama tempat
def hitung_jarak_dari_tempat(nama_tempat_input):
    koordinat = cari_koordinat_tempat(nama_tempat_input)
    if koordinat:
        user_lat, user_lon = koordinat
        jarak_ke_tempat_wisata = {}
        for nama_tempat, koordinat in tempat_wisata.items():
            jarak = haversine(user_lat, user_lon, koordinat[0], koordinat[1])
            jarak_ke_tempat_wisata[nama_tempat] = jarak
        return min(jarak_ke_tempat_wisata, key=jarak_ke_tempat_wisata.get), min(jarak_ke_tempat_wisata.values())
    else:
        return None, None
