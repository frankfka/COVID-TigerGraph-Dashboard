from typing import List, Dict

import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Output, Input

from service.data_provider import app_data_provider
from views.routes import HOME_ROUTE


def __get_patient_vertices__() -> List[Dict]:
    patient_vertices = app_data_provider.get_patient_vertices()
    return [
        {
            "data": {
                "id": vertex["patient_id"],
                "label": vertex["patient_id"]
            }
        } for vertex in patient_vertices
    ]


def __get_infected_by_edges__() -> List[Dict]:
    infected_by_edges = app_data_provider.get_infected_by_edges()
    return [
        {
            "data": {
                "source": edge["source"],
                "target": edge["target"]
            }
        } for edge in infected_by_edges
    ]


def __create_graph_visualization__():
    # Get data
    return cyto.Cytoscape(
        id='graph-visualization',
        layout={
            'name': 'cose'
        },
        style={
            'width': '100%', 'height': '400px'
        },
        elements=[
            # Vertices
            *__get_patient_vertices__(),
            # Edges
            *__get_infected_by_edges__()
        ],
    )


"""
Main layout for graph page
"""
layout = html.Div([
    # Title
    html.H1('Graph'),
    # Graph
    __create_graph_visualization__(),
    # Link to go home
    dcc.Link('Go to Home', href=HOME_ROUTE)
])
