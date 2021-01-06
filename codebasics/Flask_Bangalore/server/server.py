# from the command line: % python server.py which will give a URL like: http://127.0.0.1:5000/
from flask import Flask, request, jsonify
import util

# create an app
app = Flask(__name__)


# a test "hello world" app to test the Flask server
# run this in a browser: http://127.0.0.1:5000/hello
@app.route('/hello')
def hello():
    return "Hola!"


# return the location in Bangalore; locations are in artifacts/columns.json
# in Postman (download it), create a new tab, specify 'GET' method, then run this
# http://127.0.0.1:5000/get_location_names
@app.route('/get_location_names')
def get_location_names():
    response = jsonify({ 'locations': util.get_location_names() })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# in Postman, create a new tab with: http://127.0.0.1:5000/predict_home_price
# select POST method
# select Body, then form-data, then enter:
# Key=location, Value=1st Phase JP Nagar
# Key=total_sqft, Value=1000
# Key=bhk, Value=3
# Key=bath, Value=3
# click Send
@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    location = request.form['location']
    total_sqft = float(request.form['total_sqft'])
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({ 'estimated_price': util.estimate_price(location, total_sqft, bhk, bath) })
    return response


# run the app in the main function
if __name__ == "__main__":
    print("Starting Python Flask Server for Home Price Prediction...")
    util.load_artifacts()
    app.run()