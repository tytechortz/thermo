import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd

import requests
import time
from datetime import datetime as dt

url = "http://10.0.1.7:8080"


# Build Dash layout
app = dash.Dash(__name__)

app.layout=html.Div([
    html.Div([
        html.Div(id='live-thermometer', style={'color':'green', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='daily-high', style={'color':'red', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='daily-low', style={'color':'blue', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='rec-high', style={'color':'red', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='rec-low', style={'color':'blue', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
    ],
        className='row'
    ),
    
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
    dcc.Store(id='raw-data', storage_type='memory'),
    dcc.Store(id='daily-data', storage_type='memory'),
    dcc.Store(id='y2018', storage_type='session'),
    dcc.Store(id='y2019', storage_type='session'),
    dcc.Store(id='y2020', storage_type='session'),
    dcc.Store(id='y2021', storage_type='session'),
    dcc.Store(id='y2022', storage_type='session'),
    dcc.Store(id='y2023', storage_type='session'),
])

@app.callback(
    Output('rec-high', 'children'),
    Output('rec-low', 'children'),
    Input('raw-data', 'data'))
def update_daily_stats(data):
    df = pd.read_json(data)
    df_stats = df
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    df_stats = df_stats.set_index('datetime')

    record_highs = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()
    record_lows = df_stats.groupby(df_stats.index.strftime('%m-%d')).min()

    today = time.strftime("%m-%d")


    record_high = record_highs.loc[record_highs.index == today]
    record_low = record_lows.loc[record_lows.index == today]
    

    return (html.Div([
            html.H6('Record High', style={'text-align':'center'}),
            html.H6('{:.1f} - {}'.format(record_high.iloc[0,1], record_high.iloc[0,0][0:4]), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        ),
        html.Div([
            html.H6('Record Low', style={'text-align':'center'}),
            html.H6('{:.1f} - {}'.format(record_low.iloc[0,1], record_low.iloc[0,0][0:4]), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        ))


@app.callback(
    Output('daily-high', 'children'),
    Output('daily-low', 'children'),
    Input('daily-data', 'data'))
def update_daily_stats(daily_data):
    daily_df = pd.read_json(daily_data)
    daily_max = daily_df[1].max()
    daily_min = daily_df[1].min()

    return (html.Div([
            html.H6('Daily High', style={'text-align':'center'}),
            html.H6('{:.1f}'.format(daily_max), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        ),
        html.Div([
            html.H6('Daily Low', style={'text-align':'center'}),
            html.H6('{:.1f}'.format(daily_min), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        ))




@app.callback(Output('live-thermometer', 'children'),
              Input('interval-component', 'n_intervals'))
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32

    return html.Div([
            html.H6('Current Temp', style={'text-align':'center'}),
            html.H6('{:.1f}'.format(f), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        )
        
@app.callback(Output('raw-data', 'data'),
              Input('interval-component', 'n_intervals'))
def update_layout(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    
    return df.to_json()

@app.callback(
    Output('daily-data', 'data'),
    Output('y2018', 'data'),
    Output('y2019', 'data'),
    Output('y2020', 'data'),
    Output('y2021', 'data'),
    Output('y2022', 'data'),
    Output('y2023', 'data'),
    Input('raw-data', 'data'))
def process_df_daily(data):
    df = pd.read_json(data)

    df_stats = df
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    df_stats = df_stats.set_index('datetime')
    today = time.strftime("%m-%d")

    td = dt.now().day
    tm = dt.now().month
    ty = dt.now().year
    ly = ty-1
    # print(ly)

    dfd = df_stats[df_stats.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]
    # print(dfdmy)

    dfly = dfdm[dfdm.index.year == ly]
    df2018 = dfdm[dfdm.index.year == 2018]
    df2019 = dfdm[dfdm.index.year == 2019]
    df2020 = dfdm[dfdm.index.year == 2020]
    df2021 = dfdm[dfdm.index.year == 2021]
    df2022 = dfdm[dfdm.index.year == 2022]
    df2023 = dfdm[dfdm.index.year == 2022]
    # print(df2022)

    record_high_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()
    # print(record_high_temps)
    record_highs = df_stats.resample('D').max()
    daily_highs = record_highs.groupby([record_highs.index.month, record_highs.index.day]).max()
    low_daily_highs = record_highs.groupby([record_highs.index.month, record_highs.index.day]).min()
    # low_daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmin()
    # daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmax()

    # rec_high_date = daily_highs_date.loc[(tm,td), 1].year

    # rec_low_high = low_daily_highs.loc[(tm,td), 1]
    # rec_low_high_date = low_daily_highs_date.loc[(tm,td), 1].year

    record_low_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).min()
    record_lows = df_stats.resample('D').min()
    daily_lows = record_lows.groupby([record_lows.index.month, record_lows.index.day]).min()
    high_daily_lows = record_lows.groupby([record_lows.index.month, record_lows.index.day]).max()
    # high_daily_lows_date = record_lows.groupby([record_lows.index.month, record_lows.index.day]).idxmax()
    # daily_lows_date = record_lows.groupby([record_lows.index.month, record_lows.index.day]).idxmin()
    # rec_low_date = daily_lows_date.loc[(tm,td), 1].year
    # rec_high_low = high_daily_lows.loc[(tm,td), 1]
    # rec_high_low_date = high_daily_lows_date.loc[(tm,td), 1].year

    months = {1:31, 2:31, 3:28, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
    months_ly = {1:31, 2:31, 3:29, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}

    if td > 1:
        df_yest = df_stats[(df_stats.index.day == td-1) & (df_stats.index.month == tm) & (df_stats.index.year == ty)]
    elif td == 1:
        df_yest = df_stats[(df_stats.index.day == months.get(tm)) & (df_stats.index.month == tm-1) & (df_stats.index.year == ty)]

    return (dfdmy.to_json(), df2018.to_json(), df2019.to_json(), df2020.to_json(), df2021.to_json(), df2022.to_json(), df2023.to_json())
    



if __name__ == '__main__':
    app.run_server(port=8000,debug=True)