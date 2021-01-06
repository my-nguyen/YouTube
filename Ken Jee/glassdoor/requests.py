# -*- coding: utf-8 -*-
import requests
from datafile import data

URL = 'http://127.0.0.1:5000/predict'
headers = { 'Content-Type': 'application/json' }
data = { 'input': data }

req = requests.get(URL, headers=headers, json=data) 
req.json()