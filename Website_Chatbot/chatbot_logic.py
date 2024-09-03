import joblib
import json
from collections import Counter
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string

# Load the model
model = joblib.load('grid_search_model.pkl')

# Load the JSON data
with open('word_dimension_dict.json') as content:
    word_dimension_dict = json.load(content)

# Importing the dataset
with open('data train.json', encoding='utf-8') as content:
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

# Your chatbot function
def get_response(user_input):
    # Chatbot testing logic
    # Preprocess user input
    user_input = [ltrs.lower() for ltrs in user_input if ltrs not in string.punctuation]
    user_input = ''.join(user_input)

    # Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    ignore_words = []  # Add any words you want to ignore
    user_input = ' '.join([stemmer.stem(w.lower()) for w in user_input.split() if w not in ignore_words])

    # MENGHITUNG SETIAP TER, YANG MUNCUL DI DATASET
    # Defining a utility function to calculate the number of times a word appears in a whole dataset
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

    # Transform the user input using the same word_dimension_dict
    user_input_transformed = transform_custom([user_input], word_dimension_dict).toarray()

    # Use the trained model to predict the response
    response_label = model.predict(user_input_transformed)[0]
    response_probabilities = model.predict_proba(user_input_transformed)[0]

    return response_label, response_probabilities

