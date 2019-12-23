import sys
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
#import mysql.connector as sqlcon
from app import app
import pandas as pd
from datetime import datetime
from datetime import date, timedelta
import platform
import dash_table
import time
import flask
from components import tweetFetch as tweet_scrapping, config
import pyodbc

# popular topics: google, olympics, trump, gun, usa, sayhername #sexforgrades

# app = dash.Dash(__name__)
#
# app.layout = html.Div(
#     [html.H2('Live Twitter Sentiment'),
#      dcc.Input(id='sentiment_term', value='NationalBoyfriendDay', type='text'),
#      html.P(id='placeholder'),
#      dcc.Graph(id='live-graph', animate=False),
#      # dcc.Interval(
#      #     id='graph-update',
#      #     interval=1 * 10
#      # ),
#
#      ]
# )

''' 
    Fix minor issue with prior_end_date and prior_start_date
'''

server = config.server
database = config.database
username = config.username
password = config.password
driver = config.driver

@app.callback(Output('sentiment-live-graph', 'data'),
              [Input(component_id='sentiment_term', component_property='value'),
               Input('my-date-picker-range-birst-category', 'start_date'),
               Input('my-date-picker-range-birst-category', 'end_date')])



# Date Picker Callback
@app.callback(Output('output-container-date-picker-range-birst-category', 'children'),
              [Input('my-date-picker-range-birst-category', 'start_date'),
               Input('my-date-picker-range-birst-category', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected '
    if start_date is not None:
        start_date=start_date.split("T")[0]
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'a Start Date of ' + start_date_string + ' | '
    if end_date is not None:
        end_date = end_date.split("T")[0]
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        end_date_string = end_date.strftime('%B %d, %Y')
        days_selected = (end_date - start_date).days
        prior_start_date = start_date - timedelta(days_selected + 1)
        prior_start_date_string = datetime.strftime(prior_start_date, '%B %d, %Y')
        prior_end_date = end_date - timedelta(days_selected + 1)
        prior_end_date_string = datetime.strftime(prior_end_date, '%B %d, %Y')
        string_prefix = string_prefix + 'End Date of ' + end_date_string + ', for a total of ' + str(days_selected + 1) + \
                        ' Days. The prior period Start Date was ' + \
                        prior_start_date_string + ' | End Date: ' + prior_end_date_string + '.'
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

# @app.callback(Output('live-graph', 'figure'),
#                [Input(component_id='sentiment_term', component_property='value')])
# def update_graph_scatter(df):
#         print(df.head())
#         df.sort_values('unix', inplace=True)
#         #df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df) / 2)).mean()
#         df['date'] = pd.to_datetime(df['unix'], unit='s')
#         df.set_index('date', inplace=True)
#
#         df = df.resample('1min').mean()
#         df.dropna(inplace=True)
#         sentiment_term = df[0, 'term']
#         X = df.index
#         #Y = df.sentiment_smoothed
#         Y = df.sentiment
#
#         data = plotly.graph_objs.Scatter(
#             x=X,
#             y=Y,
#             name='Scatter',
#             mode='lines+markers'
#         )
#         print ("X axis range is {}".format(dict(range=[min(X), max(X)])))
#         print ("Y axis is {}".format(dict(range=[min(Y), max(Y)])))
#
#         return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
#                                                     yaxis=dict(range=[min(Y), max(Y)]),
#                                                     title='Term: {}'.format(sentiment_term))}
#

# @app.callback(Output("placeholder", 'children'),
#               [Input(component_id='sentiment_term', component_property='value')])
# def return_term(sentiment_term):
#     return sentiment_term


# if __name__ == '__main__':
#     # app.run_server(debug=True)
#     if platform.system() == "Linux":
#         app.run(host='0.0.0.0', port=5000, debug=True)
#         # If the system is a windows /!\ Change  /!\ the   /!\ Port
#     elif platform.system() == "Windows":
#         app.server.run(host='127.0.0.1', port=8000, debug=True)
