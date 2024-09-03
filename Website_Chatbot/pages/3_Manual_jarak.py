import streamlit as st
import math
from jarak_logic import hitung_jarak_dari_tempat
import pandas as pd

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
    "Keraton Kotagede": (-7.8298, 110.3977),
    "Keraton Ngayogyakarta Hadiningrat": (-7.8051, 110.3642),
    "Situs Taman Sari": (-7.8100, 110.3596),
    "Situs Warungboto": (-7.8099, 110.3933),
    "Kelenteng Fuk Ling Miau": (-7.8016, 110.3695),
    "Museum Sasmitaloka Panglima Besar Jenderal Soedirman": (-7.8021, 110.3754),
    "Museum Benteng Vredeburg": (-7.8000, 110.3662),
    "Monumen Yogya Kembali": (-7.7494, 110.3696),
    "Monumen Serangan Umum Satu Maret": (-7.8011, 110.3651),
    "Museum Kereta": (-7.8051, 110.3630)
}

# Fungsi untuk mengonversi nama tempat menjadi koordinat
def cari_koordinat_tempat(nama_tempat):
    return lokasi_populer.get(nama_tempat)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius Bumi dalam kilometer
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    # Menyimpan langkah-langkah perhitungan
    steps = {
        "dLat (radians)": dLat,
        "dLon (radians)": dLon,
        "a": a,
        "c": c,
        "Distance (km)": distance
    }
    return distance, steps

def hitung_jarak(nama_tempat_input):
    koordinat = cari_koordinat_tempat(nama_tempat_input)
    if koordinat:
        user_lat, user_lon = koordinat
        steps_list = []
        for nama_tempat, koordinat in tempat_wisata.items():
            distance, steps = haversine(user_lat, user_lon, koordinat[0], koordinat[1])
            steps["Tempat Wisata"] = nama_tempat
            steps_list.append(steps)
        return pd.DataFrame(steps_list)
    else:
        return None

def jarak():
    st.title("Manual Cek Jarak")

    st.header("Penjelasan proses cek jarak")
    st.write("Proses cek jarak dilakukan menggunakan Rumus Haversine untuk menentukan jarak antara 2 titik berdasarkan Longitude dan Longitude yang ada di dalam data.")
    st.write("Aturan dalam cek jarak yaitu : \n\n1. Hasil chatbot harus masuk kedalam label tempat_wisata_terdekat yang selanjutnya bot akan masuk kedalam mode cek dengan 2 pilihan input yaitu : \n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\u2022 User menginput #cek 'Nama_lokasi' \n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\u2022 User  menginput selain #cek \n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Jika input masuk kedalam pilihan kedua maka akan masuk ke dalam alur chatbot biasanya \n\n2. Lokasi yang dapat dicek jaraknya terbatas pada lokasi yang sudah ditentukan \n\n3. Awal penulisan nama lokasi harus menggunakan huruf kapital contoh : #cek Tugu Yogyakarta ")

    st.markdown("---")
    st.header("Respon Label tempat_wisata_terdekat")
    st.write("Berikut respon jika input masuk kedalam label tempat_wisata_terdekat :")
    tempat_wisata_terdekat = "Saat ini anda berada dimana ??? \n\n1. Nama Jalan \n\n\u2022 Jalan Malioboro \n\n\u2022 Jalan Prawirotaman \n\n\u2022 Jalan Sosrowijayan \n\n\u2022 Jalan Prawirotaman II \n\n\u2022 Jalan Kaliurang \n\n\u2022 Jalan Magelang \n\n\u2022 Jalan Solo \n\n\u2022 Jalan Gejayan \n\n2. Transportasi \n\n\u2022 Stasiun Tugu Yogyakarta \n\n\u2022 Stasiun Lempuyangan \n\n\u2022 Bandara Adisucipto \n\n3. Tempat \n\n\u2022 Alun-Alun Kidul \n\n\u2022 Alun-Alun Lor \n\n\u2022 Pasar Beringharjo \n\n\u2022 Museum Affandi \n\n\u2022 Kebun Binatang Gembira Loka \n\n\u2022 Jogja National Museum \n\n\u2022 Titik Nol Kilometer \n\n\u2022 Taman Pintar Yogyakarta \n\n\u2022 Tugu Yogyakarta \n\nAnda dapat mengecek tempat wisata bersejarah terdeket dari lokasi anda dengan menyamakan lokasi anda dengan lokasi diatas. Silahkan masukkan lokasi anda dengan format #cek (lokasi anda sesuai dengan daftar yang tersedia). \n\nHarap perhatikan setiap awal kata lokasi menggunakan huruf kapital untuk memudahkan pencarian. \n\nExample : #cek Tugu Yogyakarta"
    with st.expander("Label tempat_wisata_terdekat"):
        st.write(tempat_wisata_terdekat)

    st.markdown("---")

    st.header("Pilihan Nama Lokasi")
    st.write("Lokasi yang dapat di cek masih terbatas pada daftar dibawah ini :")
    jalan = "\n\n\u2022 Jalan Malioboro \n\n\u2022 Jalan Prawirotaman \n\n\u2022 Jalan Sosrowijayan \n\n\u2022 Jalan Prawirotaman II \n\n\u2022 Jalan Kaliurang \n\n\u2022 Jalan Magelang \n\n\u2022 Jalan Solo \n\n\u2022 Jalan Gejayan"
    transport = "Transportasi \n\n\u2022 Stasiun Tugu Yogyakarta \n\n\u2022 Stasiun Lempuyangan \n\n\u2022 Bandara Adisucipto"
    tempat = "\n\n\u2022 Alun-Alun Kidul \n\n\u2022 Alun-Alun Lor \n\n\u2022 Pasar Beringharjo \n\n\u2022 Museum Affandi \n\n\u2022 Kebun Binatang Gembira Loka \n\n\u2022 Jogja National Museum \n\n\u2022 Titik Nol Kilometer \n\n\u2022 Taman Pintar Yogyakarta \n\n\u2022 Tugu Yogyakarta"
    with st.expander("Nama Jalan"):
        st.write(jalan)
    with st.expander("Transportasi"):
        st.write(transport)
    with st.expander("Tempat"):
        st.write(tempat)
    
    st.header("Input lokasi ")
    # Menampilkan input teks
    user_input = st.text_input("Masukan #cek nama_lokasi")

    # if user_input.startswith("#cek "):
    #     actual_input = user_input[5:].strip()
    #     tempat_terdekat, jarak = hitung_jarak_dari_tempat(actual_input)
    #     if tempat_terdekat:
    #         response = f"Tempat wisata terdekat dari {actual_input} adalah {tempat_terdekat} dengan jarak {jarak:.2f} km."
    #     else:
    #         response = "Maaf, lokasi yang Anda masukkan tidak ditemukan."
    
    if user_input.startswith("#cek "):
        actual_input = user_input[5:].strip()
        tempat_terdekat, jarak = hitung_jarak_dari_tempat(actual_input)
        if tempat_terdekat:
            response = f"Tempat wisata terdekat dari {actual_input} adalah {tempat_terdekat} dengan jarak {jarak:.2f} km."
        else:
            response = "Maaf, lokasi yang Anda masukkan tidak ditemukan."

    # with st.expander("Perhitungan Haversein"):
    #     st.write(response)
            
    df_steps = hitung_jarak(actual_input)
    if df_steps is not None:
        with st.expander("Langkah-langkah Perhitungan Haversine"):
            st.dataframe(df_steps)

    st.header("Hasil Respon")
    st.write("Dari hasil perhitungan diatas akan diambil Distance atau jarak yang paling kecil dan akan dimasukkan kedalam respon")
    with st.expander("Hasil cek"):
        st.write(response)

jarak()