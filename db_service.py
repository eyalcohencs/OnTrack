from abc import ABC, abstractmethod
import json

import uuid as uuid
from neo4j import GraphDatabase

from utils import GeoPoint


class GraphDB(ABC):
    @abstractmethod
    def _initial_db_client(self):
        pass

    @abstractmethod
    def add_point_to_db(self, point1):
        pass

    @abstractmethod
    def add_edge_to_db(self, point1, point2):
        pass

    @abstractmethod
    def get_point_from_db(self, point1):
        pass

    @abstractmethod
    def get_edge_from_db(self, point1, point2):
        pass

    @abstractmethod
    def get_all_points_from_db(self):
        pass

    @abstractmethod
    def find_shortest_path(self, source_point, target_point):
        pass


class Neo4jDB(GraphDB):
    def __init__(self):
        super().__init__()
        details_file = "data/neo4j_locale_details"
        with open(details_file, 'r') as file:
            json_data = json.load(file)
        self.uri = json_data['uri']
        self.username = json_data['username']
        self.password = json_data['password']

    def _initial_db_client(self):
        # driver = GraphDatabase.driver(uri, auth=(username, password))
        driver = GraphDatabase.driver(self.uri)
        return driver

    def add_point_to_db(self, new_point):
        # print(f'adding point {new_point}')
        with self._initial_db_client() as client:
            with client.session() as session:
                result = session.run(f'''CREATE (point:GeoPoint {{ point_data: "{new_point}", 
                uuid: "{uuid.uuid4()}",
                longitude:"{new_point.longitude}", 
                latitude:"{new_point.latitude}", 
                altitude:"{new_point.altitude}", 
                time:"{new_point.time}" }} ) 
                RETURN point''')

                node = result.single()[0]
                return GeoPoint(node['longitude'], node['latitude'], node['altitude'], node['time'], node['uuid'])

    def add_edge_to_db(self, point1, point2):
        start_uuid = point1.uuid
        end_uuid = point2.uuid
        # print(f'adding edge {point1}-{point2}')
        with self._initial_db_client() as client:
            with client.session() as session:
                session.run(f'''MATCH (point1:GeoPoint {{ uuid: '{start_uuid}' }}), (point2:GeoPoint {{ uuid: '{end_uuid}' }})
                    MERGE (point1)-[:ROAD]->(point2)''')

    def get_point_from_db(self, point1):
        pass

    def get_edge_from_db(self, point1, point2):
        pass

    def get_all_points_from_db(self):
        with self._initial_db_client() as client:
            with client.session() as session:
                result = session.run("MATCH (n:GeoPoint) RETURN n")
                converted_result = self._convert_neo4j_db_result_to_geo_point_list(result)
                return converted_result

    def find_shortest_path(self, source_point, target_point):
        with self._initial_db_client() as client:
            with client.session() as session:
                result = session.run(
                    f'''MATCH (start:GeoPoint {{uuid: '{source_point.uuid}' }}), (end:GeoPoint {{ uuid: '{target_point.uuid}' }})
                        MATCH path = shortestPath((start)-[r:ROAD*]-(end))
                        RETURN nodes(path) AS nodes_on_path, relationships(path) AS relationships_on_path'''
                )
                return self._convert_neo4j_gds_result_to_geo_point_list(result)

    @staticmethod
    def _convert_neo4j_db_result_to_geo_point_list(result):
        geo_points = []
        for record in result:
            point = record[0]
            geo_points.append(
                GeoPoint(point['longitude'], point['latitude'], point['altitude'], point['time'], point['uuid']))
        return geo_points

    @staticmethod
    def _convert_neo4j_gds_result_to_geo_point_list(result):
        gds_result = result.single()
        nodes_on_path = gds_result['nodes_on_path']
        relationships_on_path = gds_result['relationships_on_path']
        points_on_path = [
            GeoPoint(point['longitude'], point['latitude'], point['altitude'], point['time'], point['uuid'])
            for point in nodes_on_path]
        # todo - create 'Road' object and return it
        roads_on_path = relationships_on_path
        return points_on_path
    # todo - break cache - cache the all points from db unless add or delete were made, especially for path creation
