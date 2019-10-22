import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from components import Header, printButton, twitterLive
from datetime import datetime as dt, timedelta
#from datetime import date, timedelta
import pandas as pd
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="otaladesuyi",
  passwd="phanmium",
    database="twitterdb"
)
mycursor = mydb.cursor()

term = "MondayMotivation"
df = twitterLive.fetch_initial_tweets()
temp_df=df.copy()
plot_df=twitterLive.format_df(temp_df)
# df = pd.read_sql("SELECT * FROM sentiment WHERE term LIKE %s ORDER BY date DESC LIMIT 500", mydb,
#                          params=('%' + term + '%',))

print(df.head())
current_year = df['date'].max().year



######################## START Birst Category Layout ########################


sentiment_line_graph_layout = html.Div([
    html.Div([
        # CC Header
        Header.Header(),
        # Date Picker
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range-birst-category',
                # with_portal=True,
                min_date_allowed=dt(2018, 1, 1),
                max_date_allowed=df['date'].max().to_pydatetime(),
                initial_visible_month=dt(current_year, df['date'].max().to_pydatetime().month, 1),
                start_date=(df['date'].max() - timedelta(6)).to_pydatetime(),
                end_date=df['date'].max().to_pydatetime(),
            ),
            html.Div(id='output-container-date-picker-range-birst-category')
        ], className="row ", style={'marginTop': 30, 'marginBottom': 15}),
        # Header Bar. Value set once, no need for id
        html.Div([
            html.H6(["Live Twitter Sentiment Analysis on: {}".format(term)], className="gs-header gs-text-header padded", style={'marginTop': 15})
        ]),
        dcc.Input(id='sentiment_term', value='NationalBoyfriendDay', type='text'),
        dcc.Graph(id='sentiment_live-graph', figure=go.Figure(
            data=[
                go.Scatter(
                    x=plot_df.index,
                    y=plot_df.sentiment,
                    name='Scatter',
                   mode='lines+markers'
                )
            ]
        ),
                  )

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

######################## END Birst Category Layout ########################

######################## 404 Page ########################
noPage = html.Div([
    # CC Header
    Header.Header(),
    html.P(["404 Page not found"])
    ], className="no-page")
