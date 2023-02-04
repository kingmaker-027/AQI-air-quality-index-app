import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import numpy as np
import pandas as pd 
import plotly.express as px
from app import app

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#read data set
Data = pd.read_csv('data/City_day01.csv')
Data['Date']=pd.to_datetime(Data['Date'])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

City_dropdown2 = dcc.Dropdown(options=Data['City'].unique(),value='Ahmedabad', style={'marginBottom':10})

pol_RadioItems=dcc.Dropdown(['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO',
                             'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene'], 'PM2.5' )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sidebar = html.Div(
    [
        html.H3("AQI Dash"),#html.H3("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "This Dashboard presents both summary & detailed information regarding the Pollutants for each city"
            , className="lead"),
        html.Hr(),
        html.H4(children='Pollutants Distribution'),
        html.Hr(),
        html.P('SELECT CITY : ',style={'color' :'#E10B0B'}),
        City_dropdown2,
        html.P('SELECT POLLUTANTS : ',style={'color' :'#E10B0B'}),
        pol_RadioItems,

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
    "border":"solid black 1px"},
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
        html.H4(children='Pollutants Distribution'),
        html.P('Here we go.. '),
        dcc.Graph(id='AQI-graph2'),
        html.P(' *use mouse cursor to access the values & doble click to zoom out.',
        style={'textAlign':'left','font-style': 'italic','color' :'#b20000'})

    
    ],
    style={
    "background-color": "#F0F0E5",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",}
)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
layout = html.Div([Sidebar,header])
@app.callback(
    Output(component_id='AQI-graph2', component_property='figure'),
    [Input(component_id=City_dropdown2, component_property='value'),
      Input(component_id=pol_RadioItems, component_property='value')]
)
def update_graph(selected_City,selected_pol):
    filtered_City = Data[Data['City'] == selected_City]
    fig = px.line(filtered_City,x='Date', y=selected_pol,title=f' AQI  in {selected_City}')
    fig.update_xaxes(rangeslider_visible=True)                   
    fig.update_layout(template='plotly_dark',height=400)
    return fig
