import dash

# app.scripts.config.serve_locally = False
# app.css.config.serve_locally = False

external_scripts = ["https://code.jquery.com/jquery-3.2.1.min.js",
                    "https://codepen.io/bcd/pen/YaXojL.js"]

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "https://codepen.io/bcd/pen/KQrXdb.css",
                        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                        "https://codepen.io/dmcomfort/pen/JzdzEZ.css",
                        "//fonts.googleapis.com/css?family=Raleway:400,300,600"]


app = dash.Dash(__name__, url_base_pathname='/sentiment_line_chart/', external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
# import dash_auth
# # Keep this out of source code repository - save in a file or a database
# VALID_USERNAME_PASSWORD_PAIRS = [
#     ['[username]', '[password']
# ]
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )