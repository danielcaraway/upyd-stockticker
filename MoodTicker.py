import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
from datetime import datetime
# data from my personal google forms
df = pd.read_csv('./data/form_moodetc.csv')

df['just_day'] = df.apply(lambda x: x['Timestamp'].split(' ')[0], axis=1)
df['datetime_day'] = df.apply(
    lambda x: datetime.strptime(x['just_day'], '%m/%d/%Y'), axis=1)
df['month_str'] = df.apply(lambda x: x['datetime_day'].strftime('%b'), axis=1)

# ONLY NOVEMBER
# df = df[df['month_str'] == 'Oct']

x_values = df['datetime_day']
y_values = df['Today was a good day']
y_values2 = df['On a scale of 1 to 5, how hungry were you?']
y_values3 = df['How much alcohol was consumed?']


trace = go.Scatter(x=x_values, y=y_values, mode='markers', name='mood')
trace2 = go.Scatter(x=x_values, y=y_values2,
                    mode='markers', name='hunger')
trace3 = go.Scatter(x=x_values, y=y_values3,
                    mode='lines+markers', name='alcohol')

data = [trace, trace2, trace3]

layout = go.Layout(title='Line Charts')

fig = go.Figure(data=data, layout=layout)

pyo.plot(fig)
