import json
import time 
import datetime 
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path

fdir = str(Path(__file__).parent)

weather_desc_mapping  = {"windy" : 1., "fog" : 2., "light_shower" : 3., "rain" : 4., "hazy" : 2., "storm" : 6., "clear" : 1., "sunny" : 0., "shower" : 5., "cloudy" : 3., "mostly_sunny" : 1.}

def build_data():
    pv_data = None
    weather_data = None
    duo_data = None
    with open(fdir + '/../data_cache.json') as f:
        pv_data = json.load(f)
    with open(fdir + '/../weather_cache.json') as f:
        weather_data = json.load(f)
    with open(fdir + '/../../svis-app/src/data/duocodes.json') as f:
        duo_data = json.load(f)
    # populate the df object with each input data point
    dfx = [ [], [], [], [], [], [], [], [], [], [] ]
    #dfy = []
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
                    
                    short_desc  = weather_desc_mapping[wd['icon_descriptor']]
                    temp_min    = float(wd['temp_min'] or 0.)
                    temp_max    = float(wd['temp_max'] or 0.)
                    rain_min    = float(wd['rain']['amount']['min'] or 0.)
                    rain_max    = float(wd['rain']['amount']['max'] or 0.)
                    break
                
                dfx[0].append(x)
                dfx[1].append(y)
                dfx[2].append(day_of_year*1.0)
                dfx[3].append(minute_of_day*1.0)
                dfx[4].append(short_desc or 0.)
                dfx[5].append(temp_min or 0.)
                dfx[6].append(temp_max or 0.)
                dfx[7].append(rain_min or 0.)
                dfx[8].append(rain_max or 0.)
                dfx[9].append(output*1.0)

    return np.array(dfx)#[:,0:10000]

def modelFunction(X, z, a, b, c, d, e, f, g, h, i, j, k):#, d, e, f, g, h, i, j, k):
    return (
            z
            + a*X[0]
            + b/X[1]
            + c*np.sin(d*X[2]) # fit sin to day of year
            + e*np.power((k*X[3]+f),2)
            + g*X[4]
            + h*X[5]
            + i*X[6]
            + j*X[7]
        )

def evaluateModel(x,y,day_of_year,minute_of_day,short_desc,temp_min,temp_max,rain_min,rain_max):
    params = [ 
        4.20696762e+01, -1.20180545e-01, -1.54200847e+02, -1.47419025e-01,
        1.97953510e+00, -7.48322287e-02,  6.99992494e+00, -1.46788125e+00,
        -2.05269971e-01, -8.69240534e-02, -2.15258429e-01
    ]
    inputX = [
        float(x or 0.),
        float(y or 0.),
        float(day_of_year or 0.),
        float(minute_of_day or 0.),
        float(short_desc or 0.),
        float(temp_min or 0.),
        float(temp_max or 0.),
        float(rain_min or 0.),
        float(rain_max or 0.)
    ]
    return modelFunction(inputX, params[0], 
        params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9], params[10], params[11]
    )



def train():
    df = build_data()
    # initial guesses for params
    p0 = 54., 1., 1., 1., 2., 2., 7., 1., 1., 1., 1., 1.
    cf = curve_fit(modelFunction, df[0:8,:], df[9,:], p0)
    print(cf[0])
    testX = [135.6700048, -33.467076905, 146., 720., 1., 0., 15., 0., 0.]#,23.        ]
    print(modelFunction(testX, cf[0][0], cf[0][1], cf[0][2], cf[0][3], cf[0][4], cf[0][5], cf[0][6], cf[0][7], cf[0][8], cf[0][9], cf[0][10],cf[0][11]))


if __name__=='__main__':
    train()
    #print(evaluateModel(135.6700048, -33.467076905, 146., 10., 0., 0., 15., 0., 0.))