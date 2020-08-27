"""
Entrypoint for Dash app
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import main_app
from views import pages

main_app.layout = html.Div([
    # No-render core-component that gives access to the page path
    dcc.Location(id='url', refresh=False),
    # Main page content
    html.Div(id='page-content')
])


@main_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    layout = pages.get(pathname, None)
    if layout:
        return layout
    else:
        return '404'


if __name__ == '__main__':
    main_app.run_server(debug=True)
