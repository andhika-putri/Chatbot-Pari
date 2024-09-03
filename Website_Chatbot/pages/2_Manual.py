import streamlit as st
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string
from collections import Counter
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
import joblib
import json
import numpy as np
import pandas as pd

# Load the model
model = joblib.load('D:\Kampus\TA\program\web\grid_search_model.pkl')

# Load the JSON data
with open('D:\Kampus\TA\program\web\word_dimension_dict.json') as content:
    word_dimension_dict = json.load(content)

# Importing the dataset
with open('D:\Kampus\TA\program\web\data train.json') as content:
    data1 = json.load(content)

# Mendapatkan semua data ke dalam list
label = []
inputs = []
tanggapan = {}
words = []
classes = []
documents = []
ignore_words = ['?', '!']

for intent in data1['intensi']:
    tanggapan[intent['label']] = intent['tanggapan']
    for lines in intent['pola']:
        inputs.append(lines)
        label.append(intent['label'])
        for pattern in intent['pola']:
            w = pattern.split()  # Split the text into words
            words.extend(w)
            documents.append((w, intent['label']))
            # add to our classes list
            if intent['label'] not in classes:
                classes.append(intent['label'])

# Fungsi untuk menghapus tanda baca
def remove_punctuation(user_input):
    user_input = [ltrs.lower() for ltrs in user_input if ltrs not in string.punctuation]
    remove_punctuation_result = ''.join(user_input)
    return remove_punctuation_result

# Fungsi untuk melakukan stemming
def do_stemming(user_input):
    # Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    ignore_words = []  # Tambahkan kata-kata yang ingin diabaikan
    stemming_result = ' '.join([stemmer.stem(w.lower()) for w in user_input.split() if w not in ignore_words])
    return stemming_result

def tfidf_cal(dataset, word_dimension_dict):
    data_for_df = []

    for idx, row in enumerate(dataset):
        word_freq = dict(Counter(row.split()))
        total_terms_in_doc = len(row.split())

        for word, freq in word_freq.items():
            if len(word) < 2:
                continue
            col_index = word_dimension_dict.get(word, -1)
            if col_index != -1:
                tf = freq / total_terms_in_doc
                df = count_of_word_in_whole_dataset(dataset, word)
                idf = (1 + np.log((1 + len(dataset)) / (1 + df)))
                tf_idf_value = tf * idf

                data_for_df.append({
                    'Term': word,
                    'Term Occurrences': freq,
                    'Total Term Occurrences': total_terms_in_doc,
                    'Document Frequency': df,
                    'TF': tf,
                    'IDF': idf,
                    'TF-IDF': tf_idf_value
                })

    df_tfidf = pd.DataFrame(data_for_df)

    # Omitting the creation of sparse matrix and normalization for DataFrame creation
    return df_tfidf

def count_of_word_in_whole_dataset(dataset, word):
    count = 0
    for row in dataset:
        if word in row:
            count = count + 1
    return count

# Transform custom
# MENGHITUNG TF IDF DI DALAM DATASET
def transform_custom(dataset, word_dimension_dict):
    rows = []
    columns = []
    values = []

    for idx, row in enumerate(dataset):  # for each document in the dataset
        # it will return a dict type object where key is the word and values are its frequency, {word:frequency}
        word_freq = dict(Counter(row.split()))
        # for every unique word in the document
        for word, freq in word_freq.items():
            if len(word) < 2:
                continue
            col_index = word_dimension_dict.get(word, -1)  # retrieving the dimension number of a word
            if col_index != -1:
                # we are storing the index of the document
                rows.append(idx)
                # we are storing the dimensions of the word
                columns.append(col_index)
                tf_idf_value = (freq / len(row.split())) * (
                        1 + (np.log((1 + len(dataset)) / (1 + count_of_word_in_whole_dataset(dataset, word)))))

                values.append(tf_idf_value)

    sparse_matrix = csr_matrix((values, (rows, columns)), shape=(len(dataset), len(word_dimension_dict)))
    final_normalized_output = normalize(sparse_matrix)

    return final_normalized_output

# Aplikasi Streamlit
def hitung():
    st.title("Manual Chatbot")

    st.header("Input User")
    # Menampilkan input teks
    user_input = st.text_input("Masukkan teks:")

    st.header("Prepocessing")
    st.markdown("Remove Punctuation")
    # Melakukan perhitungan menggunakan fungsi remove_punctuation
    remove = remove_punctuation(user_input)
    # Menampilkan hasil perhitungan di dalam box
    with st.expander("Hasil Remove Punctuation"):
        st.write(remove)

    st.markdown("Stemming")
    # Melakukan perhitungan menggunakan fungsi do_stemming
    stemming_result = do_stemming(remove)
    # Menampilkan hasil perhitungan di dalam box
    with st.expander("Hasil Stemming"):
        st.write(stemming_result)

    st.markdown("Tokenisai")
    # Melakukan perhitungan menggunakan fungsi do_stemming
    tokenize = stemming_result.split()
    # Membuat DataFrame dari hasil tokenisasi
    df_tokenized = pd.DataFrame({'Token': tokenize,})
    # Menampilkan hasil tokenisasi dalam DataFrame
    with st.expander("Hasil Tokenisasi (DataFrame)"):
        st.dataframe(df_tokenized)

    st.header("Menghitung Pembobotan TF-IDF")
    # Melakukan perhitungan menggunakan fungsi tfidf
    df_tfidf = tfidf_cal([stemming_result], word_dimension_dict )
    # Menampilkan hasil perhitungan di dalam box
    with st.expander("Hasil TF-IDF"):
        st.dataframe(df_tfidf)

    # Melakukan perhitungan menggunakan fungsi do_stemming
    l2 = transform_custom([stemming_result], word_dimension_dict).toarray()
    with st.expander("Hasil TFIDF setelah di normalisasi"):
        # Membuat DataFrame pandas dari hasil TF-IDF
        norml2 = pd.DataFrame(l2, columns=list(word_dimension_dict.keys()))

        # Setting format angka untuk menampilkan lebih banyak digit di belakang koma
        pd.options.display.float_format = '{:.6f}'.format

        st.dataframe(norml2)
    
    st.header("Train Model Untuk Memprediksi Respon")
    # Use the trained model to predict the response
    response_label = model.predict(l2)[0]
    response_probabilities = model.predict_proba(l2)[0]
    # Find the index of the maximum probability
    max_probability_index = np.argmax(response_probabilities)

    st.markdown("Mendapatkan nilai probabilitas di semua label")
    with st.expander("Nilai probabilitas yang didapatkan"):
        st.write(response_probabilities)

    st.markdown("Nilai max probabilitas dari seluruh label")
    # Menampilkan hasil perhitungan di dalam box
    with st.expander("Nilai max probabilitas yang didapatkan"):
        st.write(response_probabilities[max_probability_index])

    st.markdown("Index label dan nama label dari max probabilitas yang didapat")
    # Menampilkan hasil perhitungan di dalam box
    with st.expander("Hasil label yang di dapatkan"):
        st.write(max_probability_index , '\n\n', response_label)
    
    st.header("Hasil Respon Yang Didapat")
    st.caption("Jika nilai max probabilitas yang didapat kurang dari 0.2 maka akan keluar respon \n\n **'Maaf pertanyaan yang anda masukkan tidak dapat saya pahami. Silahkan masukkan pertanyaan lainnya'**")
    with st.expander("Hasil label yang di dapatkan"):
        sorry = "Maaf pertanyaan yang anda masukkan tidak dapat saya pahami. Silahkan masukkan pertanyaan lainnya"
        # Menampilkan hasil perhitungan di dalam box
        if response_probabilities[max_probability_index] > 0.2:
            # Fetch the response for the predicted label from the tanggapan dictionary
            response_data = tanggapan.get(response_label, "No valid response found for the predicted label " + response_label + ".")
            st.write(response_data[0])
        else:
            st.write("Maaf pertanyaan yang anda masukkan tidak dapat saya pahami. Silahkan masukkan pertanyaan lainnya")
    
    
hitung()