from flask import Flask, request, jsonify
import util

app = Flask(__name__)


@app.route('/hello')
def hello():
    return "Hola, mundo!"


@app.route('/classify_image', methods=['GET', 'POST'])
def classify_image():
    # get base64-encoded string from form
    image_data = request.form['image_data']

    # classify the base64-encoded string before converting it to JSON
    response = jsonify(util.classify_image(image_data))

    # add Access-Control-Allow-Origin
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    util.load_artifacts()
    app.run(port=5000)