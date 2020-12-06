import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime
import pandas as pd
# For TIINGO API key
from dotenv import load_dotenv
import os

load_dotenv()
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

# make the dash app
app = dash.Dash()
# read csv file of stonks
# make a dataframe
# build list of dropdown options
nsdq = pd.read_csv('./data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Select stock symbols:', style={'paddingRight':'30px'}),
        # replace dcc.Input with dcc.Options 
        # set options=options
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value=['AAPL'],
            multi=True
        )
    # adjust div to fit multiple inputs
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ], style={'display':'inline-block', 'marginLeft':'30px'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24, 'marginLeft':'30px'}
        ),
    ], style={'display':'inline-block'}),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])
@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    #  stock_ticker is now a list of symbols
    #  We must create a list of traces for our figure
    traces = []
    # use string formatting to include all symbols in the chart title
    title = ', '.join(stock_ticker)+' Closing Prices'
    for tic in stock_ticker:
        try:
            df = web.get_data_tiingo(tic, start, end, api_key=TIINGO_API_KEY)
            # testing our exception works
            # df = web.get_data_tiingo(tic, start, end, api_key='NOPE')
            df.index = df.index.get_level_values('date') 
            # testing our data
            # df.to_csv('tiingo.csv')
            # traces.append({'x':df.index, 'y': df.close, 'name':tic})
            # adjClose appears to be more accurate
            traces.append({'x':df.index, 'y': df.adjClose, 'name':tic})
        except:
            try: 
                # Because stock APIs change all the time this is a backup where 
                # we are downloading the data from yahoo instead of using an API
                start = pd.to_datetime([start]).astype(int)[0]//10**9 # convert to unix timestamp.
                end = pd.to_datetime([end]).astype(int)[0]//10**9 # convert to unix timestamp.
                url = 'https://query1.finance.yahoo.com/v7/finance/download/' + tic + '?period1=' + str(start) + '&period2=' + str(end) + '&interval=1d&events=history'
                df = pd.read_csv(url)
                # testing our data
                # df.to_csv('yahoo.csv')
                traces.append({'x':df.Date, 'y': df.Close, 'name':tic})
            except:
                # Throw a warning if both API and workaround stop working 
                title = "OH NO!! Unfortunately some APIs change over time!! Tweet @yesthisiskendra to let her know!!"
    fig = {
        # set data equal to traces
        'data': traces,
        'layout': {'title': title}
    }
    return fig

if __name__ == '__main__':
    app.run_server()