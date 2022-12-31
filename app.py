import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State


# Build Dash layout
app = dash.Dash(__name__)

app.layout=html.Div([
    html.Div([
        html.H2('Sup')
    ],
        className='three columns pretty_container'
    ),
])



if __name__ == '__main__':
    app.run_server(port=8000,debug=True)