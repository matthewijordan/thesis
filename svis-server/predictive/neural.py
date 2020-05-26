from pathlib import Path

from pandas import DataFrame

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import json
import time 
import datetime 

fdir = str(Path(__file__).parent)

def build_data():
    data_cache = None
    weather_data = None
    with open(fdir + '/../data_cache.json') as f:
        pv_data = json.load(f)
    with open(fdir + '/../weather_cache.json') as f:
        weather_data = json.load(f)
    with open(fdir + '/../../svis-app/src/data/duocodes.json') as f:
        duo_data = json.load(f)
    # populate the df object with each input data point
    df = []
    for pv_data_key, pv_data in pv_data.items(): # for each entry in pv data, which represents data fora given day
        for timegroup in pv_data['postcode']: # for every reporting of postcode data
            timestamp = timegroup['ts']
            for pc_k, pc_v in timegroup.items():
                if pc_k == 'ts': continue #ignore this entry
                # -- BASE DATA POINT -----------------------------------------
                #   location info
                x = duo_data[pc_k]['long']
                y = duo_data[pc_k]['lat']
                #   output
                output = pc_v
                #   time/date calcs
                dttm_utc = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%SZ')
                dttm = dttm_utc + datetime.timedelta(hours=10)
                new_year_day = datetime.datetime(year=dttm.year, month=1, day=1)
                #   time/date
                day_of_year = (dttm - new_year_day).days + 1
                minute_of_day = ( dttm.hour * 60 ) + dttm.minute
                #   weather
                short_desc  = None
                temp_min    = None
                temp_max    = None
                rain_min    = None
                rain_max    = None
                for wd in weather_data[pc_k]:
                    if wd["date"][0:10] != pv_data_key[0:10]: 
                        continue # not todays weather
                    # numericise short desc
                    
                    short_desc  = {"windy" : 1, "fog" : 2, "light_shower" : 3, "rain" : 4, "hazy" : 2, "storm" : 6, "clear" : 1, "sunny" : 0, "shower" : 5, "cloudy" : 3, "mostly_sunny" : 1}[wd['icon_descriptor']]
                    temp_min    = int(wd['temp_min'] or 0)
                    temp_max    = int(wd['temp_max'] or 0)
                    rain_min    = int(wd['rain']['amount']['min'] or 0)
                    rain_max    = int(wd['rain']['amount']['max'] or 0)
                
                df.append( [
                    x,
                    y,
                    day_of_year,
                    minute_of_day,
                    short_desc,
                    temp_min,
                    temp_max,
                    rain_min,
                    rain_max,
                    output
                ] )
    return df[0:20]

def train_ml():
    # load dataset
    #build_data()
    dataframe = DataFrame.from_dict(build_data())
    dataset = dataframe.values
    # split into input (X) and output (Y) variables
    X = dataset[:,0:8]
    Y = dataset[:,9]
    # define wider model
    def wider_model():
        # create model
        model = Sequential()
        model.add(Dense(20, input_dim=8, kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        # Compile model
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model
    # evaluate model with standardized dataset
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    estimators.append(('mlp', KerasRegressor(build_fn=wider_model, epochs=100, batch_size=5, verbose=0)))
    pipeline = Pipeline(estimators)
    kfold = KFold(n_splits=10)
    results = cross_val_score(pipeline, X, Y, cv=kfold)
    print("Wider: %.2f (%.2f) MSE" % (results.mean(), results.std()))
    print('done')

if __name__ == '__main__':
    train_ml()