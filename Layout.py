import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import sys
from components import Header, printButton, tweetFetch, config
from datetime import datetime as dt, timedelta
#from datetime import date, timedelta
import pandas as pd
# import mysql.connector
import pyodbc


# '''
#
#     Initial file to create table sentiment in db and scrape tweets into db for initial graph
#     Should be run only once ever
#
# '''


df_termlist, df = tweetFetch.fetch_initial_tweets()
if df.empty:
   sys.exit(1)

print(df.head())
termlist = df_termlist.Term.unique()
term = termlist[0]
plot_df = tweetFetch.format_df(df)
donut_values = df['Category'].value_counts()
labels = ['good', 'neutral', 'bad'] #donut_values.index
# df = pd.read_sql("SELECT * FROM sentiment WHERE term LIKE %s ORDER BY date DESC LIMIT 500", mydb,
#                          params=('%' + term + '%',))

print("Head of plot_df after formatting is : ", plot_df.head())
print("Head of original df after formatting is : ", df.head())
print("plot_df shape is: ", plot_df.shape)
print("original df shape is: ", df.shape)
current_year = plot_df['Date'].max().year



######################## START Line chart Layout ########################


sentiment_line_graph_layout = html.Div([
    html.Div([
        # CC Header
        Header.Header(),
        # Date Picker
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range-birst-category',
                # with_portal=True,
                min_date_allowed=(plot_df['Date'].min() - timedelta(6)).to_pydatetime(), #dt(2018, 1, 1),
                max_date_allowed=plot_df['Date'].max().to_pydatetime(),
                initial_visible_month=dt(current_year, plot_df['Date'].max().to_pydatetime().month, 1),
                start_date=(plot_df['Date'].min() - timedelta(6)).to_pydatetime(),
                end_date=plot_df['Date'].max().to_pydatetime(),
            ),
            html.Div([
                dcc.Dropdown(
                    id="terms",
                    options=[{
                        'label': i,
                        'value': i
                    } for i in termlist],
                    value='All terms'),
                ],
                style={'width': '25%',
                       'display': 'inline-block'}),
            html.Div(id='output-container-date-picker-range-birst-category')
        ], className="row ", style={'marginTop': 30, 'marginBottom': 40}),
        # Header Bar. Value set once, no need for id
        html.Div([
            html.H6(["Live Twitter Sentiment Analysis on: {}".format(term)], className="gs-header gs-text-header padded", style={'marginTop': 15})
        ]),
        html.Div([
            dcc.Input(id='sentiment_term', value=term, type='text'),
            dcc.Graph(id='sentiment_live-graph', figure=go.Figure(
                data=[
                    go.Scatter(
                        x=plot_df.Date,
                        y=plot_df.Sentiment,
                        name='Scatter',
                       mode='lines+markers'
                    )
                ],
                layout={
                'title': 'Tweets Sentiment chart'}
            ),
                      )
            ]),
        html.Div([
            # Use `hole` to create a donut-like pie chart
            dcc.Graph(id='donut-chart', figure=go.Figure(
            data=[
                go.Pie(
                    labels=labels, values=donut_values, hole=.6)
            ],
                layout={
                'title': 'Number of tweets per category'}
            )
                      )
        ]),
        html.Div([
            # Use `hole` to create a donut-like pie chart
            dcc.Graph(id='bar-chart', figure=go.Figure(
                data=[
                    go.Bar(
                        x=donut_values, y=labels, orientation='h')
                ],
                layout={
                'title': 'Top 4 Locations'}
            )
                      )
        ]),

    # html.H2('Live Twitter Sentiment'),
    #  dcc.Input(id='sentiment_term', value='NationalBoyfriendDay', type='text'),
    #  html.P(id='placeholder'),
    #  dcc.Graph(id='live-graph', animate=False),
     # dcc.Interval(
     #     id='graph-update',
     #     interval=1 * 10
     # ),

     ], className="subpage")
],  className="page")

# layout_birst_category = html.Div([
#
#     #    print_button(),
#
#     html.Div([
#         # CC Header
#         Header(),
#         # Date Picker
#         html.Div([
#             dcc.DatePickerRange(
#                 id='my-date-picker-range-birst-category',
#                 # with_portal=True,
#                 min_date_allowed=dt(2018, 1, 1),
#                 max_date_allowed=df['Date'].max().to_pydatetime(),
#                 initial_visible_month=dt(current_year, df['Date'].max().to_pydatetime().month, 1),
#                 start_date=(df['Date'].max() - timedelta(6)).to_pydatetime(),
#                 end_date=df['Date'].max().to_pydatetime(),
#             ),
#             html.Div(id='output-container-date-picker-range-birst-category')
#         ], className="row ", style={'marginTop': 30, 'marginBottom': 15}),
#         # Header Bar
#         html.Div([
#             html.H6(["Birst Level Metrics"], className="gs-header gs-text-header padded", style={'marginTop': 15})
#         ]),
#         # Radio Button
#         html.Div([
#             dcc.RadioItems(
#                 options=[
#                     {'label': 'Condensed Data Table', 'value': 'Condensed'},
#                     {'label': 'Complete Data Table', 'value': 'Complete'},
#                 ], value='Condensed',
#                 labelStyle={'display': 'inline-block', 'width': '20%', 'margin': 'auto', 'marginTop': 15,
#                             'paddingLeft': 15},
#                 id='radio-button-birst-category'
#             )]),
#         # First Data Table
#         html.Div([
#             dash_table.DataTable(
#                 id='datatable-birst-category',
#                 columns=[{"name": i, "id": i, 'deletable': True} for i in dt_columns],
#                 editable=True,
#                 n_fixed_columns=2,
#                 style_table={'maxWidth': '1500px'},
#                 row_selectable="multi",
#                 selected_rows=[0],
#                 style_cell={"fontFamily": "Arial", "size": 10, 'textAlign': 'left'},
#                 css=[{'selector': '.dash-cell div.dash-cell-value',
#                       'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
#                 style_cell_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#D5DBDB'}]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#EAFAF1'} for c in
#                                           ['Spend TY', 'Spend - LP', 'Spend PoP (Abs)', 'Spend PoP (%)', 'Spend LY',
#                                            'Spend YoY (%)', ]]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#D5F5E3'} for
#                                           c in
#                                           ['Spend TY', 'Spend - LP', 'Spend PoP (Abs)', 'Spend PoP (%)', 'Spend LY',
#                                            'Spend YoY (%)', ]]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#FEF9E7'} for c in
#                                           ['Sessions - TY', 'Sessions - LP', 'Sessions - LY', 'Sessions PoP (%)',
#                                            'Sessions YoY (%)', ]]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#FCF3CF'} for
#                                           c in ['Sessions - TY', 'Sessions - LP', 'Sessions - LY', 'Sessions PoP (%)',
#                                                 'Sessions YoY (%)', ]]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#EBF5FB'} for c in
#                                           ['Bookings - TY', 'Bookings - LP', 'Bookings PoP (%)', 'Bookings PoP (Abs)',
#                                            'Bookings - LY', 'Bookings YoY (%)', 'Bookings YoY (Abs)', ]]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#D6EAF8'} for
#                                           c in
#                                           ['Bookings - TY', 'Bookings - LP', 'Bookings PoP (%)', 'Bookings PoP (Abs)',
#                                            'Bookings - LY', 'Bookings YoY (%)', 'Bookings YoY (Abs)', ]]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#F4ECF7'} for c in
#                                           ['CVR - TY', 'CVR - LP', 'CVR PoP (Abs)', 'CVR - LY', 'CVR YoY (Abs)',
#                                            'CVR PoP (%)', 'CVR YoY (%)']]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#E8DAEF'} for
#                                           c in ['CVR - TY', 'CVR - LP', 'CVR PoP (Abs)', 'CVR - LY', 'CVR YoY (Abs)',
#                                                 'CVR PoP (%)', 'CVR YoY (%)']]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#FDEDEC'} for c in
#                                           ['CPA - TY', 'CPA - LP', 'CPA PoP (Abs)', 'CPA - LY', 'CPA YoY (Abs)',
#                                            'CPA PoP (%)', 'CPA YoY (%)']]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#FADBD8'} for
#                                           c in ['CPA - TY', 'CPA - LP', 'CPA PoP (Abs)', 'CPA - LY', 'CPA YoY (Abs)',
#                                                 'CPA PoP (%)', 'CPA YoY (%)']]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#F6DDCC'} for c in
#                                           ['CPS - TY', 'CPS - LP', 'CPS PoP (Abs)', 'CPS - LY', 'CPS YoY (Abs)',
#                                            'CPS PoP (%)', 'CPA YoY (%)']]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#E59866'} for
#                                           c in ['CPS - TY', 'CPS - LP', 'CPS PoP (Abs)', 'CPS - LY', 'CPS YoY (Abs)',
#                                                 'CPS PoP (%)', 'CPA YoY (%)']]
#                                        + [{'if': {'column_id': c}, 'minWidth': '0px', 'maxWidth': '80px',
#                                            'whiteSpace': 'normal'} for c in
#                                           ['Spend TY', 'Spend - LP', 'Spend PoP (Abs)', 'Spend PoP (%)', 'Spend LY',
#                                            'Spend YoY (%)', 'Sessions - TY', 'Sessions - LP', 'Sessions - LY',
#                                            'Sessions PoP (%)',
#                                            'Sessions YoY (%)', 'Bookings - TY', 'Bookings - LP', 'Bookings PoP (%)',
#                                            'Bookings PoP (Abs)', 'Bookings - LY', 'Bookings YoY (%)',
#                                            'Bookings YoY (Abs)', 'Revenue - TY', 'Revenue - LP', 'Revenue PoP (Abs)',
#                                            'Revenue PoP (%)', 'Revenue - LY', 'Revenue YoY (%)', 'Revenue YoY (Abs)', ]]
#             ),
#         ], className=" twelve columns"),
#         # Download Button
#         html.Div([
#             html.A(html.Button('Download Data', id='download-button'), id='download-link-birst-category')
#         ]),
#         # Second Data Table
#         html.Div([
#             dash_table.DataTable(
#                 id='datatable-birst-category-2',
#                 columns=[{"name": i, "id": i} for i in df_columns_calculated],
#                 editable=True,
#                 n_fixed_columns=1,
#                 style_table={'maxWidth': '1500px'},
#                 # sorting=True,
#                 # sorting_type="multi",
#                 style_cell={"fontFamily": "Arial", "size": 10, 'textAlign': 'left'},
#                 style_cell_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#D5DBDB'}]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#F4ECF7'} for c in
#                                           ['CVR - TY', 'CVR - LP', 'CVR PoP (Abs)', 'CVR - LY', 'CVR YoY (Abs)',
#                                            'CVR PoP (%)', 'CVR YoY (%)']]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#E8DAEF'} for
#                                           c in ['CVR - TY', 'CVR - LP', 'CVR PoP (Abs)', 'CVR - LY', 'CVR YoY (Abs)',
#                                                 'CVR PoP (%)', 'CVR YoY (%)']]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#FDEDEC'} for c in
#                                           ['CPA - TY', 'CPA - LP', 'CPA PoP (Abs)', 'CPA - LY', 'CPA YoY (Abs)',
#                                            'CPA PoP (%)', 'CPA YoY (%)']]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#FADBD8'} for
#                                           c in ['CPA - TY', 'CPA - LP', 'CPA PoP (Abs)', 'CPA - LY', 'CPA YoY (Abs)',
#                                                 'CPA PoP (%)', 'CPA YoY (%)']]
#                                        + [{'if': {'column_id': c}, 'backgroundColor': '#F6DDCC'} for c in
#                                           ['CPS - TY', 'CPS - LP', 'CPS PoP (Abs)', 'CPS - LY', 'CPS YoY (Abs)',
#                                            'CPS PoP (%)', 'CPS YoY (%)', ]]
#                                        + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#E59866'} for
#                                           c in ['CPS - TY', 'CPS - LP', 'CPS PoP (Abs)', 'CPS - LY', 'CPS YoY (Abs)',
#                                                 'CPS PoP (%)', 'CPS YoY (%)', ]]
#                                        + [{'if': {'column_id': c}, 'minWidth': '0px', 'maxWidth': '80px',
#                                            'whiteSpace': 'normal'} for c in
#                                           ['CPS - TY', 'CPS - LP', 'CPS PoP (Abs)', 'CPS - LY', 'CPS YoY (Abs)',
#                                            'CPS PoP (%)', 'CPS YoY (%)', 'CVR - TY', 'CVR - LP', 'CVR PoP (Abs)',
#                                            'CVR - LY', 'CVR YoY (Abs)', 'CVR PoP (%)', 'CVR YoY (%)', 'CPA - TY',
#                                            'CPA - LP', 'CPA PoP (Abs)', 'CPA - LY', 'CPA YoY (Abs)', 'CPA PoP (%)',
#                                            'CPA YoY (%)']],
#             ),
#         ], className=" twelve columns"),
#         # GRAPHS
#         html.Div([
#             html.Div(
#                 id='update_graph_1'
#             ),
#             html.Div([
#                 dcc.Graph(id='birst-category'),
#             ], className=" twelve columns"
#             ), ], className="row "
#         ),
#     ], className="subpage")
# ], className="page")

######################## END Line chart Layout ########################

######################## 404 Page ########################
noPage = html.Div([
    # CC Header
    Header.Header(),
    html.P(["404 Page not found"])
    ], className="no-page")
