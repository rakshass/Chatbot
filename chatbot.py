import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('Support/intents.json').read())

words = pickle.load(open('Support/words.pkl', 'rb'))
classes = pickle.load(open('Support/classes.pkl', 'rb'))
model = load_model('Support/chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THREHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THREHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list =[]
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    global result
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(message):
    ints = predict_class(message)
    res = get_response(ints, intents)
    return res

# from flask import Flask, render_template, request
# app = Flask(__name__)
# app.static_folder = 'static'
# @app.route("/")
# def home():
#     return render_template("index.html")
# @app.route("/get")
# def get_bot_response():
#     userText = request.args.get('msg')
#     return chatbot_response(userText)
# if __name__ == "__main__":
#     app.run(debug=True)
