from typing import List, Dict

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Output, Input, State

from app import main_app
from models.PatientTravelledEdge import PatientTravelledEdge
from models.BelongsToCaseEdge import BelongsToCaseEdge
from models.InfectedByEdge import InfectedByEdge
from models.InfectionCaseVertex import InfectionCaseVertex
from models.PatientVertex import PatientVertex
from models.TravelEventVertex import TravelEventVertex
from service.data_provider import app_data_provider
from views.graph_page.displayed_vertex_types_multiselect import create_displayed_vertex_types_multiselect
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


__patient_style__ = {
    "selector": '[type = "patient_vertex"]',
    "style": {
        "background-color": "#FF4136",
        "shape": "rectangle"
    }
}


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


def __map_travel_event_vertices__(travel_event_vertices: List[TravelEventVertex]) -> List[Dict]:
    return [
        {
            "data": {
                "id": vertex.event_id,
                "label": vertex.event_id,
                "type": "travel_event_vertex"
            }
        } for vertex in travel_event_vertices
    ]


__travel_event_style__ = {
    "selector": '[type = "travel_event_vertex"]',
    "style": {
        "background-color": "#008000",
        "shape": "triangle"
    }
}


def __map_infected_by_edges__(infected_by_edges: List[InfectedByEdge]) -> List[Dict]:
    return [
        {
            "data": {
                # Flip the source and target to show infection relationship
                "source": edge.infector_id,
                "target": edge.victim_patient_id,
                "type": "infected_by_edge"
            }
        } for edge in infected_by_edges
    ]


__infected_by_style__ = {
    "selector": '[type = "infected_by_edge"]',
    "style": {
        'line-color': 'black',
        'mid-target-arrow-color': 'black',
        'mid-target-arrow-shape': 'triangle',
    }
}


def __map_belongs_to_case_edges__(belongs_to_case_edges: List[BelongsToCaseEdge]) -> List[Dict]:
    return [
        {
            "data": {
                "source": edge.patient_id,
                "target": edge.infection_case_id,
                "type": "belongs_to_case_edge"
            }
        } for edge in belongs_to_case_edges
    ]


__belongs_to_case_style__ = {
    "selector": '[type = "belongs_to_case_edge"]',
    "style": {
        'line-color': 'blue'
    }
}


def __map_patient_travelled_edges__(patient_travelled_edges: List[PatientTravelledEdge]) -> List[Dict]:
    return [
        {
            "data": {
                "source": edge.patient_id,
                "target": edge.travel_event_id,
                "type": "patient_travelled_edge"
            }
        } for edge in patient_travelled_edges
    ]


__patient_travelled_edge_style__ = {
    "selector": '[type = "patient_travelled_edge"]',
    "style": {
        'line-color': 'yellow'
    }
}


def __expand_infection_case_vertices__(patient_vertices: List[PatientVertex], elements: List[Dict]):
    belongs_to_case_edges, infection_case_vertices \
        = app_data_provider.expand_infection_case_vertices(patient_vertices=patient_vertices)
    elements.extend([
        *__map_infection_case_vertices__(infection_case_vertices),
        *__map_belongs_to_case_edges__(belongs_to_case_edges),
    ])


def __expand_travel_event_vertices__(patient_vertices: List[PatientVertex], elements: List[Dict]):
    patient_travelled_edges, travel_event_vertices \
        = app_data_provider.expand_travel_event_vertices(patient_vertices=patient_vertices)
    elements.extend([
        *__map_travel_event_vertices__(travel_event_vertices),
        *__map_patient_travelled_edges__(patient_travelled_edges)
    ])


# TODO: Node interactivity
def __create_graph_visualization__():
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
        elements=[],
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            },
            __patient_style__,
            __infection_case_style__,
            __infected_by_style__,
            __belongs_to_case_style__,
            __patient_travelled_edge_style__,
            __travel_event_style__
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
    # Select displayed vertex types
    create_displayed_vertex_types_multiselect(),
    # Link to go home
    dcc.Link("Go to Home", href=HOME_ROUTE)
])


@main_app.callback(
    Output('graph-visualization', 'elements'),
    [Input('displayed_vertex_types_multiselect', 'value')],
    [State('graph-visualization', 'elements')])
def update_displayed_vertex_types(requested_vertex_types, _):
    patient_vertices = app_data_provider.get_patient_vertices()
    infected_by_edges = app_data_provider.get_infected_by_edges(patient_vertices)
    new_elements = [
        *__map_patient_vertices__(patient_vertices),
        *__map_infected_by_edges__(infected_by_edges),
    ]
    if 'infection_case' in requested_vertex_types:
        __expand_infection_case_vertices__(patient_vertices, new_elements)
    if 'travel_event' in requested_vertex_types:
        __expand_travel_event_vertices__(patient_vertices, new_elements)
    return new_elements
