from flask import Flask, jsonify, json
import requests
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
# allow X-origin requests
CORS(app)

data_cache = {}

# fetch remotely
def fetch_data(date):
    url = 'https://pv-map.apvi.org.au/data'
    #date = '2020-03-07'
    json_resp = requests.post(url, data = {'day':date}).json()
    return json_resp

@app.route("/data/<string:date>")
def get_data(date = None):
    print("[SVIS-SERVER] request for date " + date)
    d = data_cache.get(date)
    if d is None:
        print("[SVIS-SERVER] Fetching from origin date" + date)
        d = fetch_data(date)
        data_cache[date] = d
    else:
        print("[SVIS-SERVER] Fetching from cache date" + date)
    return jsonify({
        date : d
    })

@app.before_first_request
def pre_load_data():
    print("[SVIS-SERVER] filling cache")
    today = datetime.today().strftime('%Y-%m-%d')
    fetch_data(today)
    return None

if __name__ == "__main__":
    print("[SVIS-SERVER] starting...")
    fetch_data(datetime.today().strftime('%Y-%m-%d'))
    app.run(debug=True, use_reloader=True, port=8800, host='0.0.0.0')
