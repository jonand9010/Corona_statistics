#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Apr  5 21:35:00 2020
https://blog.furas.pl/python-scraping-how-to-get-data-from-interactive-plot-created-with-highcharts-gb.html
@author: root
"""

#%%
from bs4 import BeautifulSoup 
import requests
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time

class Import_data():
    def __init__(self, graph_nr):

        url = 'https://www.worldometers.info/coronavirus/country/sweden/'
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")
        
        all_scripts = soup.find_all('script')
   
        script = str(all_scripts[graph_nr])
        
        self.df = pd.DataFrame({'data': [], 'dates': []})

        data = script.split('data: [', 1)[1].split(']', 1)[0].split(',')
        data = [x.replace('null','0') for x in data ]
        data = [int(x) for x in data ]
        

        dates = script.split('categories: [', 1)[1].split(']', 1)[0].split(',')
        dates = [x.replace('"', '') for x in dates]
        new_dates = []

        for i in range(len(dates)):
            if i % 2 == 0:     
                new_dates.append(dates[i] + dates[i+1])
        
        self.df['data'] = data
        self.df['dates'] = new_dates


    
#%%
t0 = time.clock()
Daily_cases = Import_data(23)
Daily_deaths = Import_data(26)
print(time.clock())


# %%
from scipy.fft import fft, ifft, fftfreq
import plotly.express as px

import matplotlib.pyplot as plt

def freq_filter(y, filter):

    N = len(y)
    x = np.linspace(0,N, N)
    yf = fft(y)
    xf = np.real(fftfreq(N, 1))
    df_out = pd.DataFrame({'xf': np.real(xf), 'yf': yf})
    index = (np.abs(1/xf) >= filter[0,0]) & (np.abs(1/xf) <= filter[0,1]) | (np.abs(1/xf) >= filter[1, 0]) & (np.abs(1/xf) <= filter[1, 1])
    yf[index] = 0
    y = ifft(yf)



    return np.real(y), df_out
filter = np.array([[3.2, 3.7], [6, 8]])
y_filtered, df_spectrum = freq_filter(Daily_cases.df['data'], filter)
N = len(df_spectrum['xf'])

#%%
fig = make_subplots(rows = 3, cols = 1)
fig.append_trace(go.Scatter(x = Daily_cases.df['dates'], y = Daily_cases.df['data'], name = 'Daily cases', xaxis = "x1"), row= 1, col = 1)
fig.append_trace(go.Scatter(x = Daily_cases.df['dates'], y = y_filtered, name = 'Frequency filtered', xaxis = "x1"), row= 1, col = 1)
fig.append_trace(go.Scatter(x = 1/df_spectrum['xf'][:N//2], y = np.abs(df_spectrum['yf'][:N//2]), xaxis = "x2", name = 'Spectrum'), row= 2, col = 1)
fig.append_trace(go.Scatter(x = filter.flatten(), y = np.zeros(filter.flatten().shape),
            marker=dict(
            color='LightSkyBlue',
            size=15,
            opacity=0.5,
            line=dict(
                color='red',
                width=3
            )), name = 'Frequency filter')
            , row = 2, col = 1)
fig.update_xaxes(range=[2, 14], row=2, col=1)
fig.update_yaxes(range=[0, 0.3e6], row=2, col=1)
fig.append_trace(go.Scatter(x = Daily_deaths.df['dates'], y = Daily_deaths.df['data'], name = 'Daily deaths', xaxis = "x3"), row= 3, col = 1)
fig.show()
# %%
