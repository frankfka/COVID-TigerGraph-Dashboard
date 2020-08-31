from typing import List, Dict

import pyTigerGraph as tg

from config import Config


def __use_default__(arg, default):
    if arg is None:
        return default
    return arg

# TODO: Secrets management
class TigerGraphService:

    def __init__(self, config: Config):
        self.conn = tg.TigerGraphConnection(
            host="https://4ae36dd5a5d24279b34e62925a4a6ce1.i.tgcloud.io",
            graphname="MyGraph",
            username=config.tg_username,
            password=config.tg_password,
            apiToken=config.tg_api_key
        )

    def get_infection_case_vertices(
            self, limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        filter_by_queries = __use_default__(filter_by_queries, [])
        sort_by_attrs = __use_default__(sort_by_attrs, [])
        return self.conn.getVertices(
            vertexType="InfectionCase",
            where=",".join(filter_by_queries),
            limit=str(limit),
            sort=",".join(sort_by_attrs)
        )

    def get_patient_vertices(
            self, limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        # TODO: Enforce existance of patient_id?
        filter_by_queries = __use_default__(filter_by_queries, [])
        sort_by_attrs = __use_default__(sort_by_attrs, [])
        return self.conn.getVertices(
            vertexType="Patient",
            where=",".join(filter_by_queries),
            limit=str(limit),
            sort=",".join(sort_by_attrs)
        )

    def get_infected_by_edges(
            self, source_ids: List[str], limit: int = 50,
            sort_by_attrs: List[str] = None, filter_by_queries: List[str] = None
    ) -> List[Dict]:
        filter_by_queries = __use_default__(filter_by_queries, [])
        sort_by_attrs = __use_default__(sort_by_attrs, [])
        edges = []
        for source_id in source_ids:
            edges.extend(
                self.conn.getEdges(
                    sourceVertexType="Patient",
                    edgeType="INFECTED_BY",
                    sourceVertexId=source_id,
                    where=",".join(filter_by_queries),
                    limit=str(limit),
                    sort=",".join(sort_by_attrs)
                )
            )
        return edges
