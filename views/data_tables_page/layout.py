import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from app import main_app
from views.data_tables_page.case_map_tab import create_case_map_tab
from views.data_tables_page.patient_info_tab import create_patient_info_tab
from views.routes import HOME_ROUTE

# TODO: look at not hardcoding constants

"""
Main layout for raw data page
"""
layout = html.Div([
    # Title
    html.H1('Raw Data'),
    # Tab names
    dcc.Tabs(id='data-tabs', value='patient-info-tab', children=[
        dcc.Tab(label='Patient Info', value='patient-info-tab'),
        dcc.Tab(label='Infection Cases', value='infection-cases-tab'),
        dcc.Tab(label='Patient Routes', value='patient-routes-tab'),
    ]),
    # Tab content for different data sources, wrapped in a loading component
    dcc.Loading( # TODO: need to style
        id="tab-content-loading",
        type="circle",
        children=[html.Div(id='raw-data-tab-content')]
    ),
    # Link to go home
    dcc.Link('Go to Home', href=HOME_ROUTE)
])


@main_app.callback(Output('raw-data-tab-content', 'children'),
                   [Input('data-tabs', 'value')])
def render_tab_content(tab_value):
    if tab_value == 'patient-info-tab':
        return create_patient_info_tab()
    elif tab_value == 'infection-cases-tab':
        return create_case_map_tab()
    elif tab_value == 'patient-routes-tab':
        # TODO
        return html.Div([
            html.H3('Tab content 3')
        ])
