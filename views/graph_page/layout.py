from typing import List, Dict

import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Output, Input

from models.InfectedByEdge import InfectedByEdge
from models.InfectionCaseVertex import InfectionCaseVertex
from models.PatientVertex import PatientVertex
from service.data_provider import app_data_provider
from views.routes import HOME_ROUTE


def __map_patient_vertices__(patient_vertices: List[PatientVertex]) -> List[Dict]:
    return [
        {
            "data": {
                "id": vertex.patient_id,
                "label": vertex.patient_id,
                "type": "patient_vertex",
            }
        } for vertex in patient_vertices
    ]


def __map_infection_case_vertices__(infection_case_vertices: List[InfectionCaseVertex]) -> List[Dict]:
    return [
        {
            "data": {
                "id": vertex.case_id,
                "label": vertex.case_id,
                "type": "infection_case_vertex"
            }
        } for vertex in infection_case_vertices
    ]


__infection_case_style__ = {
    "selector": '[type = "infection_case_vertex"]',
    "style": {
        "background-color": "#00FFFF",
        "shape": "circle"
    }
}

def __map_infected_by_edges__(patient_vertices: List[PatientVertex],
                              infected_by_edges: List[InfectedByEdge]) -> List[Dict]:
    # Can't have a target if the target_id is not in the set of patient_vertices that we retrieve
    source_patient_ids = set([patient.patient_id for patient in patient_vertices])
    return [
        {
            "data": {
                "source": edge.source_id,
                "target": edge.target_id
            }
        } for edge in infected_by_edges if edge.target_id in source_patient_ids
    ]


def __create_graph_visualization__():
    # Get data
    patient_vertices = app_data_provider.get_patient_vertices()
    infection_case_vertices = app_data_provider.get_infection_case_vertices()
    infected_by_edges = app_data_provider.get_infected_by_edges(patient_vertices)
    return cyto.Cytoscape(
        id='graph-visualization',
        # TODO: increase spacing: https://js.cytoscape.org/#layouts
        layout={
            'name': 'cose',
        },
        style={
            'width': '100%',
            'height': '800px'
        },
        elements=[
            # Vertices
            *__map_patient_vertices__(patient_vertices),
            *__map_infection_case_vertices__(infection_case_vertices),
            # Edges
            *__map_infected_by_edges__(patient_vertices, infected_by_edges)
        ],
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            },
            {
                "selector": '[type = "patient_vertex"]',
                "style": {
                    "background-color": "#FF4136",
                    "shape": "rectangle"
                }
            },
            __infection_case_style__
        ]
    )


"""
Main layout for graph page
"""
layout = html.Div([
    # Title
    html.H1("Graph"),
    # Graph
    __create_graph_visualization__(),
    # Link to go home
    dcc.Link("Go to Home", href=HOME_ROUTE)
])
