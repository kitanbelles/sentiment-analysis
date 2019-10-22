import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from app import server
from app import app
from Layout import sentiment_line_graph_layout, noPage #layout_birst_category, layout_ga_category, layout_paid_search, layout_display, layout_publishing, layout_metasearch
import callbacks

import pandas as pd
import io
#import xlsxwriter
from flask import send_file

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Twitter Sentiment Analysis</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            <script type="text/javascript" src="/sentiment_line_chart/assets/jquery.js"></script>
            {%scripts%}
            {%renderer%}
        </footer>
        <div> <h3> Twitter Sentiment Analysis </h3> </div>
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
# app.layout = sentiment_line_graph_layout
# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print("Initial Pathname is: ", pathname)
    if pathname == '/sentiment_line_chart/' or pathname == '/sentiment/':
        print("There is Pathname now so I'm rendering sentiment_line_graph_layout and my pathname is: ", pathname)
        return sentiment_line_graph_layout
    # elif pathname == '/cc-travel-report/overview-ga/':
    #     return layout_ga_category
    # elif pathname == '/cc-travel-report/paid-search/':
    #     return layout_paid_search
    # elif pathname == '/cc-travel-report/display/':
    #     return layout_display
    # elif pathname == '/cc-travel-report/publishing/':
    #     return layout_publishing
    # elif pathname == '/cc-travel-report/metasearch-and-travel-ads/':
    #     return layout_metasearch
    else:
        print("No Pathname so I'm rendering No Page. Becasue I'm Stewwweeeepeeedddd")
        return noPage


# # # # # # # # #
# detail the way that external_css and external_js work and link to alternative method locally hosted
# # # # # # # # #
# external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
#                 "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
#                 "https://codepen.io/bcd/pen/KQrXdb.css",
#                 "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
#                 "https://codepen.io/dmcomfort/pen/JzdzEZ.css",
#                 "//fonts.googleapis.com/css?family=Raleway:400,300,600"]
#
# internal_css = ["/sentiment_line_chart/assets/normalise.css",
#                  "/sentiment_line_chart/assets/skeleton.css",
#                 "/sentiment_line_chart/assets/codepen.css",
#                  "/sentiment_line_chart/assets/font_awesome.css",
#                  "/sentiment_line_chart/assets/dmcomfort.css",
#                  "/sentiment_line_chart/assets/googlefont.css"]


# for css in external_css:
    # app.css.append_css({"external_url": css})


# external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
#                "https://codepen.io/bcd/pen/YaXojL.js"]
#
# internal_js = ["/sentiment_line_chart/assets/jquery.js",
#                "/sentiment_line_chart/assets/codepen.js"]

# for js in external_js:
    # app.scripts.append_script({"external_url": js})

if __name__ == '__main__':
    app.run_server(debug=True)