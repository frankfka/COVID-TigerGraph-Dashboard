import dash_core_components as dcc
import dash_html_components as html

from views.routes import DATA_TABLES_ROUTE

layout = html.Div([
    html.H3('Home Page'),
    dcc.Link('Go to Data Tables', href=DATA_TABLES_ROUTE)
])
