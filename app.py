import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import requests

url = "http://10.0.1.7:8080"


# Build Dash layout
app = dash.Dash(__name__)

app.layout=html.Div([
    html.Div(id='live-thermometer', style={'color':'green', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
    html.Div([
        dcc.Interval(
            id='interval-component-graph',
            interval=900000,
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-component',
            interval=60000,
            n_intervals=0
        ),
    ]),
])

@app.callback(Output('live-thermometer', 'children'),
              Input('interval-component', 'n_intervals'))
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32

    return html.Div([
            html.H6('Current Temp', style={'text-align':'center'}),
            html.H6('{}'.format(f), style={'text-align':'center'})
        ],
            className='three columns pretty_container'
        )
        
    



if __name__ == '__main__':
    app.run_server(port=8000,debug=True)