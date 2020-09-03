import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def create_displayed_vertex_types_multiselect() -> dbc.FormGroup:
    return dbc.FormGroup(
        [
            dbc.Label("Display Vertex Types"),
            dbc.Checklist(
                options=[
                    {"label": "Infection Case", "value": "infection_case"},
                    {"label": "Travel Event", "value": "travel_event"},
                ],
                value=[],
                id="displayed_vertex_types_multiselect",
                inline=True,
            ),
        ]
    )
