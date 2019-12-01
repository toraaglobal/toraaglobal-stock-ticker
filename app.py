# Import packages
import pandas as pd
import numpy as np
import dash_core_components as dcc 
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
import pandas_datareader as web
from datetime import datetime
import dash_auth 

USERNAME_PASSWORD_PAIRS = [['admin','aotasa99'], ['toraaglobal','Test2019']]

app = dash.Dash()
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server
# Read nasdaq stock list from csv
nsdq = pd.read_csv('./NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    mydict = {}
    mydict['label'] = nsdq.loc[tic]['Name'] + ' ' + tic
    mydict['value'] = tic
    options.append(mydict)

app.layout = html.Div([
    html.H1("Stock Ticker Dashboard"),
    html.Div([
        html.H3("Enter a stock symbol:", style={'paddingRight':'30px'}),
        dcc.Dropdown(
            id='stock_picker',
            options=options,
            multi=True,
            value= ['TSLA'])
    ], style={
         'display':'inline-block', 'verticalAlign':'top', 'width':'30%'
    }),

    html.Div([
        html.H3('Select a start and end date'),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=datetime(2000,1,1),
            max_date_allowed=datetime.today(),
            start_date = datetime(2018,1,1),
            end_date = datetime.today()

        )
    ],style={
        'display':'inline-block'
    }),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={
                'fontSize':24, 'marginLeft':'30px'
            }
        )
    ],style={
        'display':'inline-block'
    }),
    dcc.Graph(
        id='stock_graph',
        figure={
            'data': [
                {'x': [1,2,3], 'y':[2,4,6]}
            ],
            'layout':{'title': "default title"}
        }
    )
    
])


@app.callback(Output('stock_graph','figure'),
                [Input('submit-button', 'n_clicks')],
                [State('stock_picker', 'value'),
                State('date-picker', 'start_date'),
                State('date-picker','end_date')])

def update_graph (n_clicks, stock_picker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_picker:
        df = web.DataReader(tic,'iex',start,end, api_key='sk_e2ea722e117649cc9d8dc8bb36791dc3')
        traces.append({'x': df.index, 'y': df['close'], 'name':tic })

    fig = {
        'data': traces,
        'layout': {'title': stock_picker}
    }
    return fig 


if __name__ == '__main__':
    app.run_server()
