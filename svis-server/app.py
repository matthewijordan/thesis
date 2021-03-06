from flask import Flask, jsonify, json, request
import requests
from flask_cors import CORS
from datetime import datetime, timedelta
import json
from weather_au import api as wapi
import numpy as np

import predictive.poly as predictive

app = Flask(__name__)
# allow X-origin requests
CORS(app)

data_cache = {}

weather_cache = {}

# duo codes are in format (duocode, alternative search criteria)
duocodes = [
    ("08",None),("20",None),("21",None),("22",None),("23",None),("24",None),("25",None),("26",None),
    ("27",None),("28",None),("29",None),("30",None),("31","3101"),("32",None),("33",None),("34",None),
    ("35",None),("36","3607"),("37",None),("38",None),("39",None),("40",None),("41","4101"),("42","4205"),
    ("43",None),("44",None),("45",None),("46",None),("47",None),("48",None),("50",None),("51","5106"),
    ("52","5201"),("53","5301"),("54","5400"),("55","5501"),("56",None),("57",None),("59","5950"),("60",None),
    ("61",None),("62","6207"),("63","6302"),("64","6401"),("65","6501"),("66","6603"),("67","6701"),("70",None),
    ("71","7109"),("72","7209"),("73",None),("74","7466")
]



# fetch remotely
def fetch_data(date):
    url = 'https://pv-map.apvi.org.au/data'
    #date = '2020-03-07'
    json_resp = requests.post(url, data = {'day':date}).json()
    return json_resp

@app.route("/data/<string:date>")
def get_data(date = None, is_request=1):
    print("[SVIS-SERVER] request for date " + date)
    global data_cache
    d = data_cache.get(date)
    if d is None or len(d.get('postcode',[]))==0:
        print("[SVIS-SERVER] Fetching from origin date" + date)
        d = fetch_data(date)
        data_cache[date] = d
        if is_request: 
            print("[SVIS-SERVER] saving cache")
            with open('./data_cache.json', 'w+') as f:
                json.dump(data_cache, f)
    else:
        print("[SVIS-SERVER] Fetching from cache date " + date)
    return jsonify({date : d})


@app.route("/weather_data")
def get_weather_data(date = None):
    return jsonify(weather_cache)


@app.route("/predict", methods=["POST"])
def predict():
    content = request.json

    # date to days
    date = content["date"]
    dttm_utc = datetime.strptime(date,'%Y-%m-%d')
    dttm = dttm_utc + timedelta(hours=10)
    new_year_day = datetime(year=dttm.year, month=1, day=1)
    day_of_year = (dttm - new_year_day).days + 1

    time = float(content["time"])

    tempMin = float(content["predictTemperatureMin"])
    tempMax = float(content["predictTemperatureMax"])
    rainMin = float(content["predictRainfallMin"])
    rainMax = float(content["predictRainfallMax"])
    short_desc = predictive.weather_desc_mapping[content["predictWeatherType"]]

    pcdata = []

    with open('../svis-app/src/data/duocodes.json') as f:
        duo_data = json.load(f)

    # every 15 min interval
    for pcdataindex in range(0,96):
        timegroup = {}
        ts = dttm_utc + timedelta(minutes=15 * pcdataindex) - timedelta(hours=10)
        timegroup['ts'] = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
        for dc_k, dc_v in duo_data.items():
            timegroup[dc_k] = predictive.evaluateModel(
                dc_v['long'],
                dc_v['lat'],
                day_of_year,
                time,
                short_desc,
                tempMin,
                tempMax,
                rainMin,
                rainMax
            )
        pcdata.append(timegroup)

    return jsonify({
        "postcode": pcdata
    })

def pre_load_solar_data():
    print("[SVIS-SERVER] Trying to load data cache")
    global data_cache
    try:
        with open('./data_cache.json') as f:
            data_cache = json.load(f)
    except IOError:
        print("[SVIS-SERVER] No existing data cache file, fetching 365 days of data")
        for i in range(400):
            dayToFetch = datetime.today() - timedelta(days=i)
            print("[SVIS-SERVER] Pre-fetching data for d-" + str(i))
            get_data(dayToFetch.strftime('%Y-%m-%d'), is_request=0)
    get_data(datetime.today().strftime('%Y-%m-%d'), is_request=0)
    print("[SVIS-SERVER] saving cache")
    with open('./data_cache.json', 'w+') as f:
        json.dump(data_cache, f)
    return None

def pre_load_weather_data(force=False):
    print("[SVIS-SERVER] Loading weather data from cache")
    weather_cache_old = { "updated_dt": None}
    try:
        with open('./weather_cache.json') as f:
            weather_cache_old = json.load(f)
    except IOError:
        print("[SVIS-SERVER] No existing weather cache file")

    # if the stored data is out of date, or it's from todays date (meaning there could be new data), reach out for more data
    if (datetime.today().strftime('%Y-%m-%d') != weather_cache_old["updated_dt"] or force==True):
        print("[SVIS-SERVER] Cache out of date or force update, getting fresh data")
        temp_weather_cache = { "updated_dt": datetime.today().strftime('%Y-%m-%d') }
        for dc in duocodes:
            search_criteria = dc[0]+"00" if dc[1] is None else dc[1]
            w = wapi.WeatherApi(search=search_criteria, debug=0)
            temp_weather_cache[dc[0]] = w.forecasts_daily()
        # merge the cache so we dont lose old data
        print("[SVIS-SERVER] Merging cache")
        global weather_cache
        # add old values to cache
        weather_cache.update(weather_cache_old)
        # go through each duocode key (dck) and merge against list in weather cache
        for dck in temp_weather_cache:
            if dck == "updated_dt": continue
            for newWeather in temp_weather_cache[dck]:
                if newWeather == "updated_dt": continue
                replaced = 0
                if dck in weather_cache:
                    for oldWeatherIx in range(len(weather_cache[dck])):
                        if weather_cache[dck][oldWeatherIx]["date"][0:10] == newWeather["date"][0:10]:
                            weather_cache[dck][oldWeatherIx] = newWeather
                            replaced = 1
                if not replaced:
                    if dck in weather_cache:
                        weather_cache[dck].append(newWeather)
                    else:
                        weather_cache[dck] = [newWeather]
        print("[SVIS-SERVER] saving cache")
        with open('./weather_cache.json', 'w+') as f:
            json.dump(weather_cache, f)
    else:
        weather_cache.update(weather_cache_old)
        print(weather_cache)

    print("[SVIS-SERVER] done loading weather data")
    
    return None

@app.before_first_request
def do_before():
    pre_load_solar_data()
    pre_load_weather_data()
    train_model()

def train_model():
    # build data
    duocodes_pos = {}
    with open('../svis-app/src/data/duocodes.json') as f:
        duocodes_pos = json.load(f)
    dataPoints = []
    
    # params
    learning_rate = 0.1
    training_iteration = 30
    batch_size = 100
    display_step = 2
    
    # 

    return None


if __name__ == "__main__":
    print("[SVIS-SERVER] starting...")
    fetch_data(datetime.today().strftime('%Y-%m-%d'))
    app.run(debug=True, use_reloader=True, port=8800, host='0.0.0.0')
