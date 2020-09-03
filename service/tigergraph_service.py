from typing import List, Dict

import pyTigerGraph as tg

from config import Config


def __use_default_if_none__(arg, default):
    if arg is None:
        return default
    return arg


class TigerGraphService:

    def __init__(self, config: Config):
        self.conn = tg.TigerGraphConnection(
            host=config.tg_host,
            graphname=config.tg_graph,
            username=config.tg_username,
            password=config.tg_password,
            apiToken=config.tg_api_key
        )

    """
    Vertices
    """

    def __get_vertices(
            self, type_name: str, limit: int,
            sort_by_attrs: List[str], filter_by_queries: List[str]
    ) -> List[Dict]:
        filter_by_queries = __use_default_if_none__(filter_by_queries, [])
        sort_by_attrs = __use_default_if_none__(sort_by_attrs, [])
        return self.conn.getVertices(
            vertexType=type_name,
            where=",".join(filter_by_queries),
            limit=str(limit),
            sort=",".join(sort_by_attrs)
        )

    def __get_vertices_by_id(self, type_name: str, ids: List[str]) -> List[Dict]:
        return self.conn.getVerticesById(vertexType=type_name, vertexIds=ids)

    def get_patient_vertices(
            self, limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        # TODO: Enforce existance of patient_id?
        return self.__get_vertices(
            type_name="Patient",
            limit=limit,
            sort_by_attrs=sort_by_attrs,
            filter_by_queries=filter_by_queries
        )

    def get_infection_case_vertices(
            self, limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        return self.__get_vertices(
            type_name="InfectionCase",
            limit=limit,
            sort_by_attrs=sort_by_attrs,
            filter_by_queries=filter_by_queries
        )

    def get_infection_case_vertices_by_id(self, ids: List[str]) -> List[Dict]:
        return self.__get_vertices_by_id(type_name="InfectionCase", ids=ids)

    def get_travel_event_vertices(
            self, limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        return self.__get_vertices(
            type_name="TravelEvent",
            limit=limit,
            sort_by_attrs=sort_by_attrs,
            filter_by_queries=filter_by_queries
        )

    def get_travel_event_vertices_by_id(self, ids: List[str]) -> List[Dict]:
        return self.__get_vertices_by_id(type_name="TravelEvent", ids=ids)

    """
    Edges
    """

    def __get_edges(
            self, edge_type: str, source_vertex_type: str, source_ids: List[str],
            target_vertex_type: str,
            limit: int, sort_by_attrs: List[str], filter_by_queries: List[str]
    ) -> List[Dict]:
        filter_by_queries = __use_default_if_none__(filter_by_queries, [])
        sort_by_attrs = __use_default_if_none__(sort_by_attrs, [])
        edges = []
        for source_id in source_ids:
            edges.extend(
                self.conn.getEdges(
                    sourceVertexType=source_vertex_type,
                    edgeType=edge_type,
                    sourceVertexId=source_id,
                    targetVertexType=target_vertex_type,
                    where=",".join(filter_by_queries),
                    limit=str(limit),
                    sort=",".join(sort_by_attrs)
                )
            )
        return edges

    def get_infected_by_edges(
            self, from_patient_ids: List[str], limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        return self.__get_edges(
            edge_type="INFECTED_BY",
            source_vertex_type="Patient",
            source_ids=from_patient_ids,
            target_vertex_type="Patient",
            limit=limit,
            sort_by_attrs=sort_by_attrs,
            filter_by_queries=filter_by_queries
        )

    def get_belongs_to_case_edges(
            self, from_patient_ids: List[str], limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        return self.__get_edges(
            edge_type="BELONGS_TO_CASE",
            source_vertex_type="Patient",
            source_ids=from_patient_ids,
            target_vertex_type="InfectionCase",
            limit=limit,
            sort_by_attrs=sort_by_attrs,
            filter_by_queries=filter_by_queries
        )

    def get_patient_travelled_edges(
            self, from_patient_ids: List[str], limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        return self.__get_edges(
            edge_type="PATIENT_TRAVELED",
            source_vertex_type="Patient",
            source_ids=from_patient_ids,
            target_vertex_type="TravelEvent",
            limit=limit,
            sort_by_attrs=sort_by_attrs,
            filter_by_queries=filter_by_queries
        )
