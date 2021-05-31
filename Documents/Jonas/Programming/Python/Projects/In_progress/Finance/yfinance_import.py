#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:17:37 2020

@author: Jonas

source: https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
"""
#%%

import dash
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output 
import plotly.graph_objects as go

import seaborn as sns



#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE]) 
app = dash.Dash()
app.title = 'Jonas\'s Financial Dashboard'
app.layout = html.Div([ 
    html.Div([ 
        html.Div([ 
            dcc.Dropdown(id='company_selection1',options=[
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Google', 'value': 'GOOG'}],
            value = 'TSLA')]),
        dcc.Graph(id ='figure1', style={'background-color': '#eeeeee', 'padding': 10}),
    
        html.Div([ 
            dcc.Dropdown(id='company_selection2',options=[
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Google', 'value': 'GOOG'}],
            value = 'AAPL', style={'background-color': '#eeeeee', 'padding': 10})]),
        dcc.Graph(id ='figure2', style={'background-color': '#eeeeee', 'padding': 10}),
        ])
    ],style= {'backgroundcolor': '#eeeeee'})    
            
    #html.H3(id='text'),


import yfinance as yf
#import seaborn as sns
#sns.set()

tickerSymbol = 'KINV-B.ST'

#get data on this ticker



#%%
#sns.lineplot(data = df, x = df.index, y = 'Close')

@app.callback(Output(component_id = 'figure1', component_property = 'figure'), 
                [Input('company_selection1','value')])
def plot_financial_data(company):
    tickerData = yf.Ticker(company)
    #get the historical prices for this ticker
    df = tickerData.history(period = '1d', start = '2010-1-1', end = '2020-4-28')
    df.describe()

    

    datapoints = {'data': [go.Line(x=df.index, y=df.Close.values,
            marker_color='lightsalmon',
            name='Net Income')], 'layout': dict(xaxis={'title':'Date'}, 
            yaxis={'title':'Close'}, paper_bgcolor = '#eeeeee', plot_bgcolor = '#eeeeee' )}
        
    return datapoints


@app.callback(Output(component_id = 'figure2', component_property = 'figure'), 
                [Input('company_selection2','value')])
def plot_financial_data(company):
    tickerData = yf.Ticker(company)
    #get the historical prices for this ticker
    df = tickerData.history(period = '1d', start = '2010-1-1', end = '2020-4-28')
    df.describe()

    

    datapoints = {'data': [go.Line(x=df.index, y=df.Close.values,
            marker_color='lightsalmon',
            name='Net Income')], 'layout': dict(xaxis={'title':'Date'}, 
            yaxis={'title':'Close'}, paper_bgcolor = '#eeeeee', plot_bgcolor = '#eeeeee' )}
        
    return datapoints
# %%
if __name__ == '__main__': app.run_server(debug=True)