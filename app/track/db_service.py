import os
from abc import ABC, abstractmethod
import uuid as uuid
from neo4j import GraphDatabase
import dotenv


from app.track.utils import GeoPoint, GeoRoad
# from flask import current_app


class GraphDB(ABC):
    @abstractmethod
    def _initial_db_client(self):
        pass

    @abstractmethod
    def add_point_to_db(self, point1):
        pass

    @abstractmethod
    def add_edge_to_db(self, point1, point2, data):
        pass

    @abstractmethod
    def add_point_and_relation_to_exist_point_db(self, existed_point, new_point, relation_data):
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
    def get_all_roads_from_db(self):
        pass

    @abstractmethod
    def find_shortest_path(self, source_point, target_point):
        pass


class Neo4jDB(GraphDB):

    def _initial_db_client(self):
        dotenv.load_dotenv()
        uri = os.environ['NEO4J_URI']
        username = os.environ['NEO4J_USERNAME']
        password = os.environ['NEO4J_PASSWORD']
        driver = GraphDatabase.driver(uri, auth=(username, password))
        return driver

    def add_point_to_db(self, new_point):
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

    def add_edge_to_db(self, point1, point2, data):
        start_uuid = point1.uuid
        end_uuid = point2.uuid
        # print(f'adding edge {point1}-{point2}')
        with self._initial_db_client() as client:
            with client.session() as session:
                session.run(f'''MATCH (point1:GeoPoint {{ uuid: '{start_uuid}' }}), (point2:GeoPoint {{ uuid: '{end_uuid}' }})
                    MERGE (point1)-[:ROAD {{ track_id: '{str(data['track_id'])}' }} ]->(point2)''')

    def add_point_and_relation_to_exist_point_db(self, existed_point, new_point, relation_data):
        with self._initial_db_client() as client:
            with client.session() as session:
                result = session.run(f'''
                MATCH(existed_point: GeoPoint {{uuid: "{existed_point.uuid}"}})
                CREATE (new_point:GeoPoint {{ point_data: "{new_point}", 
                uuid: "{uuid.uuid4()}",
                longitude:"{new_point.longitude}", 
                latitude:"{new_point.latitude}", 
                altitude:"{new_point.altitude}", 
                time:"{new_point.time}" }} )
                MERGE (existed_point)-[:ROAD {{ track_id: '{str(relation_data['track_id'])}' }} ]->(new_point)
                RETURN new_point''')

                node = result.single()[0]
                return GeoPoint(node['longitude'], node['latitude'], node['altitude'], node['time'], node['uuid'])
            
    def get_point_from_db(self, point1):
        pass

    def get_edge_from_db(self, point1, point2):
        pass

    def get_all_points_from_db(self):
        with self._initial_db_client() as client:
            with client.session() as session:
                result = session.run("MATCH (n:GeoPoint) RETURN n")
                converted_result = self._convert_neo4j_db_nodes_to_geo_point_list(result)
                return converted_result

    def get_all_roads_from_db(self):
        with self._initial_db_client() as client:
            with client.session() as session:
                result = session.run('''
                MATCH (source:GeoPoint)-[relation:ROAD]->(target:GeoPoint)
                RETURN  relation.track_id, source.uuid, source.longitude, source.latitude, source.altitude, source.time,
                target.uuid, target.longitude, target.latitude, target.altitude, target.time''')
                converted_result = self._convert_neo4j_db_relations_to_geo_roads(result)
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
    def _convert_neo4j_db_nodes_to_geo_point_list(result):
        geo_points = []
        for record in result:
            point = record[0]
            geo_points.append(
                GeoPoint(point['longitude'], point['latitude'], point['altitude'], point['time'], point['uuid']))
        return geo_points

    @staticmethod
    def _convert_neo4j_db_relations_to_geo_roads(result):
        geo_roads = []
        for record in result:
            geo_road = GeoRoad(
                GeoPoint(record['source.longitude'], record['source.latitude'], record['source.altitude'],
                         record['source.time'], record['source.uuid']),
                GeoPoint(record['target.longitude'], record['target.latitude'], record['target.altitude'],
                         record['target.time'], record['target.uuid']),
                record['relation.track_id']
            )
            geo_roads.append(geo_road)
        return geo_roads

    def _convert_neo4j_gds_result_to_geo_point_list(self, result):
        gds_result = result.single()
        if gds_result is None:
            return [], []
        nodes_on_path = gds_result['nodes_on_path']
        relationships_on_path = gds_result['relationships_on_path']
        geo_points_on_path = [
            GeoPoint(point['longitude'], point['latitude'], point['altitude'], point['time'], point['uuid'])
            for point in nodes_on_path]
        geo_roads = self._convert_neo4j_relations_to_geo_roads(relationships_on_path)
        return geo_points_on_path, geo_roads

    @staticmethod
    def _convert_neo4j_relations_to_geo_roads(relations):
        geo_roads = []
        for relation in relations:
            source = relation.start_node
            source_point = GeoPoint(source['longitude'], source['latitude'], source['altitude'], source['time'], source['uuid'])
            target = relation.end_node
            target_point = GeoPoint(target['longitude'], target['latitude'], target['altitude'], target['time'], target['uuid'])
            geo_roads.append(GeoRoad(source_point, target_point))
        return geo_roads
