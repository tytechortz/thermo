import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import collections
import requests
import time
from datetime import datetime as dt, timedelta


url = "http://10.0.1.7:8080"


# Build Dash layout
app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

app.layout=html.Div([
    html.Div([
        html.Div(id='live-thermometer', style={'color':'green', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='daily-high', style={'color':'red', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='daily-low', style={'color':'blue', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='yest-high', style={'color':'red', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='yest-low', style={'color':'blue', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='aqi', style={'color':'black', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
    ],
        className='row'
    ),
    html.Div([
        html.Div(id='rec-high', style={'color':'red', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='rec-low', style={'color':'blue', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='year-high', style={'color':'red', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='year-low', style={'color':'blue', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='at-high', style={'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
    ],
        className='row'
    ),
    html.Div([
        dcc.Graph(id='graph')
    ],
        className='row'
    ),
    html.Div([
        html.H6('Ranks', style={'color':'white', 'text-align':'center'}),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.Div(id='daily-high-high-rank', style={'color':'red', 'text-align':'center'}), 
        ],
            className='six columns'
        ),
        html.Div([
            html.Div(id='daily-low-low-rank', style={'color':'blue', 'text-align':'center'}), 
        ],
            className='six columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.Div(id='daily-high-low-rank', style={'color':'red', 'text-align':'center'}), 
        ],
            className='six columns'
        ),
        html.Div([
            html.Div(id='daily-low-high-rank', style={'color':'blue', 'text-align':'center'}), 
        ],
            className='six columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.H6('Monthly Rank', style={'color':'white', 'text-align':'center'}),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.Div(id='monthly-high-high-rank', style={'color':'red', 'text-align':'center'}), 
        ],
            className='six columns'
        ),
        html.Div([
            html.Div(id='monthly-low-low-rank', style={'color':'blue', 'text-align':'center'}), 
        ],
            className='six columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.Div(id='monthly-high-low-rank', style={'color':'red', 'text-align':'center'}), 
        ],
            className='six columns'
        ),
        html.Div([
            html.Div(id='monthly-low-high-rank', style={'color':'blue', 'text-align':'center'}), 
        ],
            className='six columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.H6('Monthly High - Low', style={'color':'white', 'text-align':'center'}),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.Div(id='monthly-high', style={'color':'red', 'text-align':'center'}),
        ],
            className='five columns'
        ),
        html.Div([
            html.Div(id='monthly-high-date', style={'color':'red', 'text-align':'center'}),
        ],
            className='seven columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.Div(id='monthly-low', style={'color':'blue', 'text-align':'center'}),
        ],
            className='five columns'
        ),
        html.Div([
            html.Div(id='monthly-low-date', style={'color':'blue', 'text-align':'center'}),
        ],
            className='seven columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.H6('Monthly Records', style={'color':'white', 'text-align':'center'}),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.Div(id='monthly-record-high', style={'color':'red', 'text-align':'center'}),
        ],
            className='six columns'
        ),
        html.Div([
            html.Div(id='monthly-record-low', style={'color':'blue', 'text-align':'center'}),
        ],
            className='six columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div(id='avg-high', style={'color':'red', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='avg-low', style={'color':'blue', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='avg', style={'color':'black', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='rec-high-count', style={'color':'red', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
        html.Div(id='rec-low-count', style={'color':'blue', 'font-size': 25, 'font-family':'sans-serif', 'text-align':'center'}),
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
    dcc.Store(id='y2024', storage_type='session'),
    dcc.Store(id='last-year', storage_type='session'),
    dcc.Store(id='yest', storage_type='session'),
])

@app.callback([
    Output('monthly-record-high', 'children'),
    Output('monthly-record-low', 'children'),
    Output('monthly-high', 'children'),
    Output('monthly-low', 'children'),
    Output('monthly-high-date', 'children'),
    Output('monthly-low-date', 'children')],
    [Input('interval-component', 'n_intervals'),
    Input('raw-data', 'data')])
def update_graph(n, raw_data):  
    df = pd.read_json(raw_data)
    # print(df)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    # highs = df.resample('M').max()
    # print(highs)
    tm = dt.now().month
    ty = dt.now().year
    dfm = df[df.index.month == tm]
    dfm = dfm.drop(0, axis=1)
    # print(dfm)
    mrh_date = dfm.groupby(dfm.index.month).idxmax()
    # print(mrh_date)
    mrh_date = mrh_date.iloc[0][1].strftime('%m-%d-%Y')
    mrh = dfm.groupby(dfm.index.month).max()
    # print(mrh)
    mrh = mrh.iloc[0][1]
    # print(mrh)
    mrl = dfm.groupby(dfm.index.month).min()
    mrl_date = dfm.groupby(dfm.index.month).idxmin()
    mrl_date = mrl_date.iloc[0][1].strftime('%m-%d-%Y')
    mrl = mrl.iloc[0][1]

    dfmy = dfm[dfm.index.year == ty]
    # print(dfmy)
    monthly_high = dfmy.groupby(dfmy.index.month).max()
    monthly_high = monthly_high.iloc[0][1]
    monthly_high_date = dfmy.groupby(dfmy.index.month).idxmax()
    monthly_high_date = monthly_high_date.iloc[0][1].strftime('%m-%d-%Y %H:%M:%S')
    monthly_low = dfmy.groupby(dfmy.index.month).min()
    monthly_low = monthly_low.iloc[0][1]
    monthly_low_date = dfmy.groupby(dfmy.index.month).idxmin()
    monthly_low_date = monthly_low_date.iloc[0][1].strftime('%m-%d-%Y %H:%M:%S')
    # print(monthly_low_date)
    # df90 = highs.loc[highs[1] >= 90]
    # df95 = highs.loc[highs[1] >= 95]
    # df100 = highs.loc[highs[1] >= 100]

    # ndds = df90.groupby(df90.index.year).count()
    # nfdds = df95.groupby(df95.index.year).count()
    # hdds = df100.groupby(df100.index.year).count()
    # print(nfdds, hdds)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also

    #     print(df90, df95, nfdds)
    # df22dh = df22.resample('D').max()
    
    
    return html.H6('High: {:.1f} : {}'.format(mrh, mrh_date)), html.H6('Low: {:.1f} : {}'.format(mrl, mrl_date)), html.H6('High: {:.1f}'.format(monthly_high)), html.H6('Low: {:.1f}'.format(monthly_low)), html.H6('{}'.format(monthly_high_date)), html.H6('{}'.format(monthly_low_date))

@app.callback([
    Output('monthly-high-high-rank', 'children'),
    Output('monthly-high-low-rank', 'children'),
    Output('monthly-low-high-rank', 'children'),
    Output('monthly-low-low-rank', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('raw-data', 'data')])
def update_daily_stats(n, data):
    today = time.strftime("%Y-%m-%d")
    df = pd.read_json(data)
    df_s = df
    df_s['date'] = pd.to_datetime(df_s[0])
    df_s = df_s.set_index('date')
    current_month = dt.now().month
    # print(current_month)
    
    daily_highs = df_s.resample('D').max()
    dfmh = daily_highs[daily_highs.index.month == current_month]
    # print(dfmh)
    # print(daily_highs)
    highest_monthly_highs = dfmh.sort_values(1, ascending=False)
    # print(highest_monthly_highs.head(50))
    monthly_high_high_rank = highest_monthly_highs.index.get_loc(today)+1

    august_days = len(dfmh)
    # print(august_days)
    # daily_high = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).idxmax()
    # highest_daily_highs = daily_highs.sort_values(1, ascending=False)
    lowest_monthly_highs = dfmh.sort_values(1, ascending=True)
    # print(lowest_monthly_highs.head(50))
    # high_high_rank = highest_daily_highs.index.get_loc(today)+1
    monthly_low_high_rank = lowest_monthly_highs.index.get_loc(today)+1
        
    daily_lows = df_s.resample('D').min()
    dfml = daily_lows[daily_lows.index.month == current_month]
    highest_monthly_lows = dfml.sort_values(1, ascending=True)
    # print(highest_monthly_lows.tail(50))
    lowest_monthly_lows = dfml.sort_values(1, ascending=False)
    # print(lowest_monthly_lows.tail(50))
    monthly_low_low_rank = highest_monthly_lows.index.get_loc(today)+1
    monthly_high_low_rank = lowest_monthly_lows.index.get_loc(today)+1

    # daily_low = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).idxmin()
    # highest_monthly_lows = dfml.sort_values(1, ascending=True)
    # lowest_monthly_lows = dfml.sort_values(1, ascending=False)
    # print(lowest_daily_lows.head(30))
    # monthly_high_low_rank = lowest_monthly_lows.index.get_loc(today)+1




    return html.H6('HH-{}'.format(monthly_high_high_rank)), html.H6('HL-{}'.format(monthly_high_low_rank)), html.H6('LH-{}'.format(monthly_low_high_rank)), html.H6('LL-{}'.format(monthly_low_low_rank))

@app.callback(
    Output('daily-high-high-rank', 'children'),
    Output('daily-high-low-rank', 'children'),
    Output('daily-low-high-rank', 'children'),
    Output('daily-low-low-rank', 'children'),
    Input('interval-component-graph', 'n_intervals'),
    Input('raw-data', 'data'))
def update_daily_stats(n, data):
    today = time.strftime("%Y-%m-%d")
    df = pd.read_json(data)
    df_s = df
    df_s['date'] = pd.to_datetime(df_s[0])
    df_s = df_s.set_index('date')
    
    daily_highs = df_s.resample('D').max()



    total_days = len(daily_highs)
    # print(total_days)
    # daily_high = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).idxmax()
    highest_daily_highs = daily_highs.sort_values(1, ascending=False)
    lowest_daily_highs = daily_highs.sort_values(1, ascending=True)
    high_high_rank = highest_daily_highs.index.get_loc(today)+1
    low_high_rank = lowest_daily_highs.index.get_loc(today)+1
        
    daily_lows = df_s.resample('D').min()
    # daily_low = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).idxmin()
    highest_daily_lows = daily_lows.sort_values(1, ascending=True)
    lowest_daily_lows = daily_lows.sort_values(1, ascending=False)
    # print(lowest_daily_lows.head(30))
    low_low_rank = highest_daily_lows.index.get_loc(today)+1
    high_low_rank = lowest_daily_lows.index.get_loc(today)+1
    # print(high_high_rank)
    # print(low_low_rank)



    return html.H6('HH-{}'.format(high_high_rank)), html.H6('HL-{}'.format(high_low_rank)), html.H6('LH-{}'.format(low_high_rank)), html.H6('LL-{}'.format(low_low_rank))


@app.callback(
        Output('aqi', 'children'),
        Input('interval-component-graph', 'n_intervals')
)
def updata_aqi(n):
    print(n)
    ct = dt.now().strftime('%Y-%m-%d')
    ch = dt.now().hour
    chs = str(ch)
    cte = ch + 5
    ctes = str(cte)
    cteend = cte + 1
    cts = str(cteend)
    # air_df = pd.read_csv('https://www.airnowapi.org/aq/data/?startDate=2023-05-20T17&endDate=2023-05-20T18&parameters=PM25&BBOX=-104.948260,39.733721,-104.931780,39.744545&dataType=A&format=text/csv&verbose=0&monitorType=0&includerawconcentrations=0&API_KEY=1A91F885-CD4E-4EBC-9AFF-1AC398A78966')
    air_df = pd.read_csv('https://www.airnowapi.org/aq/data/?startDate=' + ct + 'T' + ctes + '&endDate=' + ct + 'T' + cts + '&parameters=PM25&BBOX=-104.948260,39.733721,-104.931780,39.744545&dataType=A&format=text/csv&verbose=0&monitorType=0&includerawconcentrations=0&API_KEY=1A91F885-CD4E-4EBC-9AFF-1AC398A78966')
    # print(air_df)
    aqi = air_df.columns[4]
    tme = air_df.columns[2][-5:]

    return html.Div([
                html.H6('AQI'),
                html.H6('{}'.format(aqi)),
            ],
                className= 'two columns pretty_container'
            )


@app.callback([
    Output('yest-high', 'children'),
    Output('yest-low', 'children')],
    Input('interval-component-graph', 'n_intervals'),
    Input('yest', 'data'))
def update_daily_stats(n, yest):
    
    yest = pd.read_json(yest)
    yest_max = yest[1].max()
    yest_min = yest[1].min()

    return (html.Div([
                html.H6('Yest-High'),
                html.H6('{:.1f}'.format(yest_max))
            ],
                className='two columns pretty_container'
            ),
            html.Div([
                html.H6('Yest-Low'),
                html.H6('{:.1f}'.format(yest_min))
            ],
                className='two columns pretty_container'
            ))


@app.callback(
    Output('year-high', 'children'),
    Output('year-low', 'children'),
    Input('raw-data', 'data'))
def update_daily_stats(data):
    df = pd.read_json(data)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    ty = dt.now().year
    dfy = df[df.index.year == ty]
    yearly_high = dfy[1].max()
    yearly_high_date = dfy[1].idxmax()
    # print(yearly_high)
    yearly_low = dfy[1].min()
    yearly_low_date = dfy[1].idxmin()

    return (html.Div([
            html.H6('Annual High', style={'text-align':'center'}),
            html.H6('{:.1f} : {}'.format(yearly_high, yearly_high_date.strftime('%m-%d')), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        ),
        html.Div([
            html.H6('Annual Low', style={'text-align':'center'}),
            html.H6('{:.1f} : {}'.format(yearly_low, yearly_low_date.strftime('%m-%d')), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        ))

@app.callback(
    Output('at-high', 'children'),
    Input('raw-data', 'data'))
def update_daily_stats(data):
    df = pd.read_json(data)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    # ty = dt.now().year
    # dfy = df[df.index.year == ty]
    at_high = df[1].max()
    at_high_date = df[1].idxmax()
    # print(yearly_high)
    at_low = df[1].min()
    at_low_date = df[1].idxmin()

    return (html.Div([
            html.H6('Rec Max : {:.1f} : {}'.format(at_high, at_high_date.strftime('%m-%d-%Y')), style={'color':'red','text-align':'center'}),
            html.H6('Rec Min : {:.1f} : {}'.format(at_low, at_low_date.strftime('%m-%d-%Y')), style={'color':'blue','text-align':'center'}),
            # html.H6('{:.1f} : {}'.format(at_high, at_high_date.strftime('%m-%d-%Y')), style={'text-align':'center'})
        ],
            className='four columns pretty_container'
        ))


@app.callback(
    Output('avg-high', 'children'),
    Output('avg-low', 'children'),
    Output('avg', 'children'),
    Output('rec-high-count', 'children'),
    Output('rec-low-count', 'children'),
    Input('interval-component-graph', 'n_intervals'))
def averages(n):
    # day_of_year = dt.now().timetuple().tm_yday
    day_of_year = 2
    # print(day_of_year)
    today = time.strftime("%Y-%m-%d")
 
    # df = pd.read_csv('../../tempjan19.csv', header=None)
    df = pd.read_csv('/Users/jamesswank/Downloads/tempjan19.csv', header=None)
    # print(df)
    df_s = df
    df_s['date'] = pd.to_datetime(df_s[0])
    df_s = df_s.set_index('date')


    daily_highs = df_s.resample('D').max()
    daily_high = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).idxmax(numeric_only=True)

    rh_tot = daily_high[1]
    rh_doy = rh_tot.head(day_of_year)
    # print(rh_tot)

    highs_2018 = daily_highs[daily_highs.index.year == 2018]
    highs_to_date_2018 = highs_2018.head(day_of_year)
    avg_high_to_date_2018 = highs_to_date_2018[1].mean()

    highs_2019 = daily_highs[daily_highs.index.year == 2019]
    highs_to_date_2019 = highs_2019.head(day_of_year)
    avg_high_to_date_2019 = highs_to_date_2019[1].mean()

    highs_2020 = daily_highs[daily_highs.index.year == 2020]
    highs_to_date_2020 = highs_2020.head(day_of_year)
    avg_high_to_date_2020 = highs_to_date_2020[1].mean()

    highs_2021 = daily_highs[daily_highs.index.year == 2021]
    highs_to_date_2021 = highs_2021.head(day_of_year)
    avg_high_to_date_2021 = highs_to_date_2021[1].mean()

    highs_2022 = daily_highs[daily_highs.index.year == 2022]
    highs_to_date_2022 = highs_2022.head(day_of_year)
    avg_high_to_date_2022 = highs_to_date_2022[1].mean()
    # print(highs_to_date_2020)
    highs_2023 = daily_highs[daily_highs.index.year == 2023]
    highs_to_date_2023 = highs_2023.head(day_of_year)
    avg_high_to_date_2023 = highs_to_date_2023[1].mean()

    highs_2024 = daily_highs[daily_highs.index.year == 2024]
    highs_to_date_2024 = highs_2024.head(day_of_year)
    avg_high_to_date_2024 = highs_to_date_2024[1].mean()

    daily_lows = df_s.resample('D').min()
    daily_low = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).idxmin(numeric_only=True)

    rl_tot =daily_low[1]
    rl_doy = rl_tot.head(day_of_year)



    lows_2018 = daily_lows[daily_lows.index.year == 2018]
    lows_to_date_2018 = lows_2018.head(day_of_year)
    avg_low_to_date_2018 = lows_to_date_2018[1].mean()

    lows_2019 = daily_lows[daily_lows.index.year == 2019]
    lows_to_date_2019 = lows_2019.head(day_of_year)
    avg_low_to_date_2019 = lows_to_date_2019[1].mean()

    lows_2020 = daily_lows[daily_lows.index.year == 2020]
    lows_to_date_2020 = lows_2020.head(day_of_year)
    avg_low_to_date_2020 = lows_to_date_2020[1].mean()

    lows_2021 = daily_lows[daily_lows.index.year == 2021]
    lows_to_date_2021 = lows_2021.head(day_of_year)
    avg_low_to_date_2021 = lows_to_date_2021[1].mean()

    lows_2022 = daily_lows[daily_lows.index.year == 2022]
    lows_to_date_2022 = lows_2022.head(day_of_year)
    avg_low_to_date_2022 = lows_to_date_2022[1].mean()

    lows_2023 = daily_lows[daily_lows.index.year == 2023]
    lows_to_date_2023 = lows_2023.head(day_of_year)
    avg_low_to_date_2023 = lows_to_date_2023[1].mean()

    lows_2024 = daily_lows[daily_lows.index.year == 2024]
    lows_to_date_2024 = lows_2024.head(day_of_year)
    avg_low_to_date_2024 = lows_to_date_2024[1].mean()

    avg_2018 = (avg_high_to_date_2018 + avg_low_to_date_2018) / 2
    avg_2019 = (avg_high_to_date_2019 + avg_low_to_date_2019) / 2
    avg_2020 = (avg_high_to_date_2020 + avg_low_to_date_2020) / 2
    avg_2021 = (avg_high_to_date_2021 + avg_low_to_date_2021) / 2
    avg_2022 = (avg_high_to_date_2022 + avg_low_to_date_2022) / 2
    avg_2023 = (avg_high_to_date_2023 + avg_low_to_date_2023) / 2
    avg_2024 = (avg_high_to_date_2024 + avg_low_to_date_2024) / 2

    
    h_years = rh_doy.tolist()
    l_years = rl_doy.tolist()

    h_year_list = []
    for x in h_years:
        h_year_list.append(x.year)


    l_year_list = []
    for x in l_years:
        l_year_list.append(x.year)

    h_counts = collections.Counter(h_year_list)
    l_counts = collections.Counter(l_year_list)

    # print(h_counts)

  

    return [html.Div([
        html.H6('Avg High'),
        html.H6('2018: {:.1f}'.format(avg_high_to_date_2018)),
        html.H6('2019: {:.1f}'.format(avg_high_to_date_2019)),
        html.H6('2020: {:.1f}'.format(avg_high_to_date_2020)),
        html.H6('2021: {:.1f}'.format(avg_high_to_date_2021)),
        html.H6('2022: {:.1f}'.format(avg_high_to_date_2022)),
        html.H6('2023: {:.1f}'.format(avg_high_to_date_2023)),
        html.H6('2024: {:.1f}'.format(avg_high_to_date_2024)),
        ],
            className='two columns pretty_container'
        ),
    html.Div([
        html.H6('Avg Low'),
        html.H6('2018: {:.1f}'.format(avg_low_to_date_2018)),
        html.H6('2019: {:.1f}'.format(avg_low_to_date_2019)),
        html.H6('2020: {:.1f}'.format(avg_low_to_date_2020)),
        html.H6('2021: {:.1f}'.format(avg_low_to_date_2021)),
        html.H6('2022: {:.1f}'.format(avg_low_to_date_2022)),
        html.H6('2023: {:.1f}'.format(avg_low_to_date_2023)),
        html.H6('2024: {:.1f}'.format(avg_low_to_date_2024)),
        ],
            className='two columns pretty_container'
        ),
    (html.Div([
            html.H6('Avg'),
            html.H6('2018: {:.1f}'.format(avg_2018)),
            html.H6('2019: {:.1f}'.format(avg_2019)),
            html.H6('2020: {:.1f}'.format(avg_2020)),
            html.H6('2021: {:.1f}'.format(avg_2021)),
            html.H6('2022: {:.1f}'.format(avg_2022)),
            html.H6('2023: {:.1f}'.format(avg_2023)),
            html.H6('2024: {:.1f}'.format(avg_2024)),
        ],
            className='two columns pretty_container'
        )),
    html.Div([
            html.H6('Rec H'),
            html.H6('2018: {}'.format(h_counts[2018])), 
            html.H6('2019: {}'.format(h_counts[2019])),
            html.H6('2020: {}'.format(h_counts[2020])),
            html.H6('2021: {}'.format(h_counts[2021])), 
            html.H6('2022: {}'.format(h_counts[2022])),
            html.H6('2023: {}'.format(h_counts[2023])),
            html.H6('2024: {}'.format(h_counts[2024])),
        ],
            className='two columns pretty_container'
        ), 
    html.Div([
        html.H6('Rec L'),
        html.H6('2018: {}'.format(l_counts[2018])), 
        html.H6('2019: {}'.format(l_counts[2019])),
        html.H6('2020: {}'.format(l_counts[2020])),
        html.H6('2021: {}'.format(l_counts[2021])), 
        html.H6('2022: {}'.format(l_counts[2022])),
        html.H6('2023: {}'.format(l_counts[2023])),
        html.H6('2024: {}'.format(l_counts[2024])),
    ],
        className='two columns pretty_container'
    ), 
    # (html.Div([
    #         html.P('2018: {}'.format(l_counts[2018])), 
    #         html.P('2019: {}'.format(l_counts[2019])),
    #         html.P('2020: {}'.format(l_counts[2020])),
    #     ]))
    ]

    
    

@app.callback(
    Output('rec-high', 'children'),
    Output('rec-low', 'children'),
    Input('raw-data', 'data'))
def update_daily_stats(data):
    df = pd.read_json(data)
    df_stats = df
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    df_stats = df_stats.set_index('datetime')

    td = dt.now().day
    tm = dt.now().month
    ty = dt.now().year
    ly = ty-1

    today = time.strftime("%m-%d")

    record_high_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()
    record_high = record_high_temps.loc[record_high_temps.index == today]
    record_highs = df_stats.resample('D').max()
    daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmax(numeric_only=True)
    rec_high_date = daily_highs_date.loc[(tm,td), 1].year
 

    record_low_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).min()
    record_low = record_low_temps.loc[record_low_temps.index == today]
    record_lows = df_stats.resample('D').min()
    daily_lows_date = record_lows.groupby([record_lows.index.month, record_lows.index.day]).idxmin(numeric_only=True)
    rec_low_date = daily_lows_date.loc[(tm,td), 1].year

    

    return (html.Div([
            html.H6('Record High', style={'text-align':'center'}),
            html.H6('{:.1f} - {}'.format(record_high.iloc[0,1], rec_high_date), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        ),
        html.Div([
            html.H6('Record Low', style={'text-align':'center'}),
            html.H6('{:.1f} - {}'.format(record_low.iloc[0,1], rec_low_date), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        ))


@app.callback(
    Output('daily-high', 'children'),
    Output('daily-low', 'children'),
    Input('daily-data', 'data'))
def update_daily_stats(daily_data):
    daily_df = pd.read_json(daily_data)
    # print(daily_df)
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
            html.H2('{:.1f}'.format(f), style={'text-align':'center'}),
            # html.H4('{:.1f}'.format(f), style={'text-align':'center'})
        ],
            className='two columns pretty_container'
        )
        
@app.callback(Output('raw-data', 'data'),
              Input('interval-component', 'n_intervals'))
def update_layout(n):
    # df = pd.read_csv('../../tempjan19.csv', header=None)
    df = pd.read_csv('/Users/jamesswank/Downloads/tempjan19.csv', header=None)
    # print(df)
    return df.to_json()

@app.callback(
    Output('daily-data', 'data'),
    Output('y2018', 'data'),
    Output('y2019', 'data'),
    Output('y2020', 'data'),
    Output('y2021', 'data'),
    Output('y2022', 'data'),
    Output('y2023', 'data'),
    Output('y2024', 'data'),
    Output('last-year', 'data'),
    Output('yest', 'data'),
    Input('raw-data', 'data'))
def process_df_daily(data):
    df = pd.read_json(data)
    # print(df)
    df_stats = df
    
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    
    df_stats = df_stats.set_index('datetime')
    today = time.strftime("%m-%d")
    

    # td = dt.now().day
    td = 2
    # print(td)
    tm = dt.now().month
    ty = dt.now().year
    ly = ty-1
   

    dfd = df_stats[df_stats.index.day == td]
    # print(dfd)
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]
    # print(dfdmy)

    dfly = dfdm[dfdm.index.year == ly]
    # print(dfly)
    df2018 = dfdm[dfdm.index.year == 2018]
    df2019 = dfdm[dfdm.index.year == 2019]
    df2020 = dfdm[dfdm.index.year == 2020]
    df2021 = dfdm[dfdm.index.year == 2021]
    df2022 = dfdm[dfdm.index.year == 2022]
    df2023 = dfdm[dfdm.index.year == 2023]
    df2024 = dfdm[dfdm.index.year == 2024]
    # print(df2022)

    # record_high_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()
    # print(record_high_temps)
    # record_highs = df_stats.resample('D').max()
    # daily_highs = record_highs.groupby([record_highs.index.month, record_highs.index.day]).max()
    # low_daily_highs = record_highs.groupby([record_highs.index.month, record_highs.index.day]).min()
    # low_daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmin()
    # daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmax()

    # rec_high_date = daily_highs_date.loc[(tm,td), 1].year

    # rec_low_high = low_daily_highs.loc[(tm,td), 1]
    # rec_low_high_date = low_daily_highs_date.loc[(tm,td), 1].year

    # record_low_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).min()
    # record_lows = df_stats.resample('D').min()
    # daily_lows = record_lows.groupby([record_lows.index.month, record_lows.index.day]).min()
    # high_daily_lows = record_lows.groupby([record_lows.index.month, record_lows.index.day]).max()
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
    # print(df_yest)

    return (dfdmy.to_json(), df2018.to_json(), df2019.to_json(), df2020.to_json(), df2021.to_json(), df2022.to_json(), df2023.to_json(), df2024.to_json(), dfly.to_json(), df_yest.to_json())
    
@app.callback(
    Output('graph', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('daily-data', 'data'),
    Input('last-year', 'data'),
    Input('y2018', 'data'),
    Input('y2019', 'data'),
    Input('y2020', 'data'),
    Input('y2021', 'data'),
    Input('y2022', 'data'),
    Input('y2023', 'data'),
    Input('yest', 'data')
    )
def update_graph(n, daily_data, last_year, y2018, y2019, y2020, y2021, y2022, y2023, yest):
    dfdmy = pd.read_json(daily_data)
    dfdmy['time'] = pd.to_datetime(dfdmy[0])
    dfdmy['time'] = dfdmy['time'].dt.strftime('%H:%M')
    # print(dfdmy)
    yest = pd.read_json(yest)
    yest['time'] = pd.to_datetime(yest[0])
    yest['time'] = yest['time'].dt.strftime('%H:%M')

    dfly = pd.read_json(last_year)
    dfly['time'] = pd.to_datetime(dfly[0])
    dfly['time'] = dfly['time'].dt.strftime('%H:%M')
    # print(dfly)
    # df_list=[]

    df2018 = pd.read_json(y2018)
    df2018['time'] = pd.to_datetime(df2018[0])
    df2018['time'] = df2018['time'].dt.strftime('%H:%M')
    # df_list.append(df2018)

    df2019 = pd.read_json(y2019)
    df2019['time'] = pd.to_datetime(df2019[0])
    df2019['time'] = df2019['time'].dt.strftime('%H:%M')
    # df_list.append(df2019)

    df2020 = pd.read_json(y2020)
    df2020['time'] = pd.to_datetime(df2020[0])
    df2020['time'] = df2020['time'].dt.strftime('%H:%M')
    # df_list.append(df2020)

    df2021 = pd.read_json(y2021)
    df2021['time'] = pd.to_datetime(df2021[0])
    df2021['time'] = df2021['time'].dt.strftime('%H:%M')
    # df_list.append(df2021)

    df2022 = pd.read_json(y2022)
    df2022['time'] = pd.to_datetime(df2022[0])
    df2022['time'] = df2022['time'].dt.strftime('%H:%M')

    df2023 = pd.read_json(y2023)
    df2023['time'] = pd.to_datetime(df2023[0])
    df2023['time'] = df2023['time'].dt.strftime('%H:%M')
    # df_list.append(df2022)
    # print(df_list)
    # if selected_date == ''
    # data = []
    # years = [2018,2023]
    # for df, y in zip(df_list,years):
    #     data.append(go.Scatter(
    #         x = df_list[df['time']],
    #         y = df_list[1],
    #         mode = 'markers+lines',
    #         marker = dict(
    #             color = 'black',
    #         ),
    #         name='{}'.format(y)
    #     ))

    # print(data)

    fig  = go.Figure()

    fig.add_trace(go.Scatter(
            x = df2018['time'],
            y = df2018[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'yellow',
            ),
            name='2018'
        ),)
    
    fig.add_trace(go.Scatter(
            x = df2019['time'],
            y = df2019[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'blue',
            ),
            name='2019'
        ),)
    fig.add_trace(go.Scatter(
            x = df2020['time'],
            y = df2020[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'red',
            ),
            name='2020'
        ),)
    fig.add_trace(go.Scatter(
            x = df2021['time'],
            y = df2021[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'orange',
            ),
            name='2021'
        ),)
    fig.add_trace(go.Scatter(
            x = df2022['time'],
            y = df2022[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'green',
            ),
            name='2022'
        ),)
    fig.add_trace(go.Scatter(
            x = df2023['time'],
            y = df2023[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'turquoise',
            ),
            name='2023'
        ),)
    fig.add_trace(go.Scatter(
            x = yest['time'],
            y = yest[1],
            mode = 'lines',
            marker = dict(
                color = 'tan',
            ),
            name='yesterday'
        ),)
    fig.add_trace(go.Scatter(
            x = dfdmy['time'],
            y = dfdmy[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'white',
            ),
            name='today'
        ),)
    

    fig.update_layout(
        go.Layout(
        xaxis=dict(tickformat='%H%M'),
        height=500,
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        hovermode='x',

    ))

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    
    return fig

    


if __name__ == '__main__':
    app.run_server(port=8000,debug=True)