import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web # requires v0.6.0 or later
from datetime import datetime
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
import os
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

app = dash.Dash()


app.layout = html.Div([
  html.H1('Stock Ticker Dashboard'),
  html.H3('Enter a stock symbol:'),
  dcc.Input(id='my_ticker_symbol',value='TSLA'),
  dcc.Graph(id='my_graph', figure={'data': [{'x':[1,2], 'y': [3.4]}]})
])

@app.callback(
  Output('my_graph', 'figure'), 
  [Input('my_ticker_symbol', 'value')])

def update_graph(stock_ticker):
  start = datetime(2017, 1, 1)
  end = datetime(2020, 10, 10)
  df = web.get_data_tiingo(stock_ticker, start, end, api_key=TIINGO_API_KEY)
  df.index = df.index.get_level_values('date') 
  fig = {'data':[{'x':df.index, 'y':df['close']}], 'layout':{'title':stock_ticker}}

  return fig


if __name__ == '__main__':
  app.run_server()