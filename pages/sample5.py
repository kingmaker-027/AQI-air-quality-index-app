import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import numpy as np
import pandas as pd 
import plotly.express as px
from app import app
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Data = pd.read_csv('data/City_day01.csv')
Data['Date']=pd.to_datetime(Data['Date'])
Data['year'] = Data['Date'].dt.year
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

City_dropdown5=dcc.Dropdown([ 2015, 2016, 2017, 2018, 2019, 2020], 2020 )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sidebar = html.Div(
    [
        html.H3("AQI Dash"),#html.H3("Sidebar", className="display-4"),
        html.Hr(),
        html.P("The AQI Dashboard presents both summary and detailed information regarding the AQI Level for each city", className="lead"),
        html.Hr(),
        html.H4(children='Avg AQI Level'),
        html.P('SELECT YEAR : ',style={'color' :'#E10B0B'}),

        City_dropdown5,
    ],
    style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#B6D7A8",
    "margin-top": "5rem",
    "margin-left": "1rem",
    "border":"solid black 1px"

    },
)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

header= html.Div([
        html.H1(children='Air Quality Index',
        style={'textAlign':'center','font-weight': 'bold','marginTop':10,'marginBottom':10}),
        html.Hr(),
        html.P("Let us know what we breathe....! ", className="lead"),
        html.P('The Air Quality Index (AQI) is used for reporting daily air quality. It tells you how clean or pollutedyour air is, and what associated health effects might be a concern for you.',
        style={'textAlign':'left','font-style': 'italic','color' :'#0000FF'}),
        html.Hr(),
        html.H4(children='Avg AQI Level Of Cities in year wise'),
        html.P('Here we go.. '),
        dcc.Graph(id='AQI-graph5'),
        html.P(' *use mouse cursor to access the values & doble click to zoom out.',
        style={'textAlign':'left','font-style': 'italic','color' :'#b20000'})

],style={
    "background-color": "#F0F0E5",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"}
)

layout = html.Div([Sidebar,header])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(
    Output(component_id='AQI-graph5', component_property='figure'),
    Input(component_id=City_dropdown5, component_property='value')
)
def update_graph(YEAR):
    ye=Data[Data['year']==YEAR]
    ye_avg = ye[['City','AQI','year']].groupby(['City','year']).mean().sort_values(['AQI']).reset_index()
    fig = px.bar(ye_avg, x='City', y='AQI',
             hover_data=['year'], color='City',title=f'Avg AQI Level Of Cities in {YEAR}')

    return fig
