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
df= Data[['Date','City','AQI']]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def categorise_AQI(row):  
    if row['AQI'] >= 0 and row['AQI'] < 51:
        return 'GOOD'
    elif row['AQI'] >= 51 and row['AQI'] < 101:
        return 'SATISFACTORY'
    elif row['AQI'] >= 101 and row['AQI'] < 201:
        return 'MODERATEIY'
    elif row['AQI'] >= 201 and row['AQI'] < 301:
        return 'POOR'
    elif row['AQI'] >= 301 and row['AQI'] < 401:
        return 'VERY_POOR'
    elif row['AQI'] >= 401 :
        return 'SEVERE'
    
df['AQI_category'] = df.apply(lambda row: categorise_AQI(row), axis=1)
df['AQI_category'] = df['AQI_category'].astype('object')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

City_dropdown3 = dcc.Dropdown(options=Data['City'].unique(),value='Ahmedabad', style={'marginBottom':10})


Sidebar = html.Div(
    [
        html.H3("AQI Dash"),#html.H3("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "This Dashboard presents both summary & detailed information regarding the AQI Category for each city"
            , className="lead"),
        html.Hr(),
        html.H4(children='AQI Category'),
        html.P('SELECT CITY : ',style={'color' :'#E10B0B'}),
        City_dropdown3,
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
        html.H4(children='AQI Category'),
        html.P('Here we go.. '),
        dcc.Graph(id='AQI-graph3'),
        html.P(' *use mouse cursor to access the values & doble click to zoom out.',
        style={'textAlign':'left','font-style': 'italic','color' :'#b20000'})
],
style={
    "background-color": "#F0F0E5",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
)
layout = html.Div([Sidebar,header])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.callback(
    Output(component_id='AQI-graph3', component_property='figure'),
    Input(component_id=City_dropdown3, component_property='value')
)

def update_graph(selected_City):
    
    filtered_City = df[df['City'] == selected_City]
    fig = px.pie(filtered_City,  names='AQI_category',hole=.5, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(
        title_text=f"{selected_City} AQI Categor 2015-2020",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text=f' {selected_City}', x=0.5, y=0.5, font_size=15, showarrow=False)])
    
    return fig
