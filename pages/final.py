import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd 
import plotly.express as px
import base64
import io
import tensorflow 
from sklearn import preprocessing
from tensorflow.keras.models import load_model
import plotly.express as px

from sklearn import preprocessing
Scaler = preprocessing.MinMaxScaler()
model = load_model("Delhi.h5")

from app import app



def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df




upload = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '200px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            
        },
        # Allow multiple files to be uploaded
        multiple=True
    )

result = dcc.Graph(id='output')
table = html.Div(id='output-data-upload')

Sidebar = html.Div(
    [
        html.H3("AQI Dash"),#html.H3("Sidebar", className="display-4"),
        html.Hr(),
        html.P("This model capable to forecast 30 days in future based on 60 days past data", className="lead"),
        html.Hr(),
        html.H6(children='Input data here :'),
        upload,
        html.Hr(),
        html.P("*Only csv,execl file support",style={'textAlign':'left','font-style': 'italic','color' :'#b20000'})
    ],
     style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#B6D7A8",
    "margin-top": "5rem",
    "margin-left": "1rem",
    "border":"solid black 1px"},
    )


header= html.Div([
        html.H1(children='Air Quality Index Forecasting',
        style={'textAlign':'center','font-weight': 'bold','marginTop':10,'marginBottom':10}),
        html.Hr(),
        table,
        html.Hr(),
        result,

              ],style={
                         "background-color": "#F0F0E5",
                        "margin-left": "20rem",
                        "margin-right": "2rem",
                        "padding": "2rem 1rem"}
)

layout = html.Div([Sidebar,header])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_contents(contents, filename)

        table = html.Div(
            [
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_action='none',
                    fixed_rows={'headers': True},
                    style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white'},
                    style_table={'height': '200px', 'overflowY': 'auto' }
                ),
                
                
            ]
        )

    return table


@app.callback(Output('output', 'figure'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))

           
def update_pred(contents, filename):

    if contents:
            contents = contents[0]
            filename = filename[0]
            data = parse_contents(contents, filename)
            past_dates = pd.to_datetime(data['Date']) 
            n_days_for_prediction=31  
            predict_period_dates =  pd.date_range(list(past_dates)[59], periods=n_days_for_prediction, freq="D").tolist()  
            forecast_dates = []
            for time_i in predict_period_dates:
                forecast_dates.append(time_i.date())

            data.index= pd.to_datetime(data['Date'])
            data = data.drop(['Date'],axis = 1) 
            for i in data.columns:
                data[[i]] = Scaler.fit_transform(data[[i]])   
            test = data.drop(['AQI'],axis = 1)
            test = test.to_numpy()
            test = test.reshape(1,test.shape[0],test.shape[1])
            y_pred = model.predict(test)
            y_pred_inv = Scaler.inverse_transform(y_pred)
            y_pred_inv = y_pred_inv.ravel()  
            
            df_forecast = pd.DataFrame({'Date':np.array(forecast_dates[1:]),'AQI':y_pred_inv})

            
            
            fig = px.line(df_forecast,x='Date', y='AQI',title=f'30 day forecasting')
            fig.update_xaxes(rangeslider_visible=True)
            fig.update_layout(template='plotly_dark')
    return fig
        



