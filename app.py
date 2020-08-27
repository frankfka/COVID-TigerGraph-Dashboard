import dash

main_app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = main_app.server
