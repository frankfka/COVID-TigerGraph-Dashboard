import dash_core_components as dcc
import dash_html_components as html

from views.routes import HOME_ROUTE

layout = html.Div([
    html.H3('Data Tables'),
    dcc.Link('Go to Home', href=HOME_ROUTE)
])
