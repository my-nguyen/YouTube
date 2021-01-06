from flask import Flask, jsonify, request
import json
from datafile import data
import numpy as np
import pickle

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    response = json.dumps({'response': 'hola MY NGUYEN!'})
    return response, 200


def load_model():
    file_name = "glassdoor_model.pkl"
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
        model = data['model']
    return model


def process(data_in):
    X = np.array(data_in).reshape(1, -1)
    model = load_model()
    prediction = model.predict(X)[0]
    response = json.dumps({'response': prediction})
    return response, 200


@app.route('/hardcode', methods=['GET'])
def hardcode():
    return process(data)


@app.route('/predict', methods=['GET'])
def predict():
    request_json = request.get_json()
    X = request_json['input']
    return process(X)


if __name__ == '__main__':
    app.run(debug=True)