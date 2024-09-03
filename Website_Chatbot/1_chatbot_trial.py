# File: app.py

import streamlit as st
from chatbot_logic import get_response, tanggapan
import numpy as np
from jarak_logic import hitung_jarak_dari_tempat  # Impor dari jarak_logic.py

def main():
    st.title("Chatbot Pari")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    sorry = "Maaf pertanyaan yang anda masukkan tidak dapat saya pahami. Silahkan masukkan pertanyaan lainnya"

    if user_input := st.chat_input("Mau Kemanakah Kamu Hari Ini?"):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        response_label, response_probabilities = get_response(user_input)
        max_probability_index = np.argmax(response_probabilities)

        # Menginisialisasi state jika belum ada
        if 'awaiting_cek_input' not in st.session_state:
            st.session_state['awaiting_cek_input'] = False
        
        if st.session_state['awaiting_cek_input'] and user_input.startswith("#cek "):
            actual_input = user_input[5:].strip()
            tempat_terdekat, jarak = hitung_jarak_dari_tempat(actual_input)

            if tempat_terdekat:
                response = f"Tempat wisata terdekat dari {actual_input} adalah {tempat_terdekat} dengan jarak {jarak:.2f} km."
            else:
                response = "Maaf, lokasi yang Anda masukkan tidak ditemukan."

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Reset state setelah menampilkan hasil
            st.session_state['awaiting_cek_input'] = False

        if response_probabilities[max_probability_index] > 0.2:
            response_data = tanggapan.get(response_label, "No valid response found for the predicted label " + response_label + ".")

            if response_label == 'tempat_wisata_terdekat':
                st.session_state['awaiting_cek_input'] = True
                # Proses input pengguna jika dalam mode menunggu input 'cek'
                with st.chat_message("assistant"):
                    st.markdown(response_data[0])
                st.session_state.messages.append({"role": "assistant", "content": response_data[0]})
            else:
                with st.chat_message("assistant"):
                    st.markdown(response_data[0])
                st.session_state.messages.append({"role": "assistant", "content": response_data[0]})
        
        # Jika pengguna memberikan respons lain dan bukan dalam mode 'cek'
        if not st.session_state['awaiting_cek_input']:
            if response_probabilities[max_probability_index] < 0.2:
                with st.chat_message("assistant"):
                    st.markdown(sorry)
                st.session_state.messages.append({"role": "assistant", "content": sorry})
                
if __name__ == "__main__":
    main()
