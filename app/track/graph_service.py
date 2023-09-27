from app import cache
from app.track.db_service import Neo4jDB
from app.track.graph_logic import is_there_already_a_close_point_in_the_graph, distance_between_points, \
    are_the_same_point_by_coordinates, add_point_to_group_of_points
from app.track.utils import all_close_points_in_border

graph_db = Neo4jDB()


def add_point_to_graph(point_to_add, grouped_points, grouped_key_function):
    collided_point = is_there_already_a_close_point_in_the_graph(point_to_add, grouped_points)
    if collided_point:
        point_to_add = collided_point
    else:
        point_to_add = graph_db.add_point_to_db(point_to_add)
        add_point_to_group_of_points(grouped_points, point_to_add, grouped_key_function)
    return point_to_add


# todo - not used for now - was partially replaced with add_point_and_relation_to_exist_point_to_graph
def add_edge_to_graph(source_point, target_point, data=None):
    data = data if data is not None else {'track_id': None}
    if not are_the_same_point_by_coordinates(source_point, target_point):
        graph_db.add_edge_to_db(source_point, target_point, data)


def add_point_and_relation_to_exist_point_to_graph(existed_point, point_to_add, data=None, grouped_all_points=None, grouping_creation_key=None):
    data = data if data is not None else {'track_id': None}
    collided_point = is_there_already_a_close_point_in_the_graph(point_to_add, grouped_points=grouped_all_points)
    if collided_point:
        point_to_add = collided_point
        if not are_the_same_point_by_coordinates(existed_point, point_to_add):
            graph_db.add_edge_to_db(existed_point, point_to_add, data)
    else:
        point_to_add = graph_db.add_point_and_relation_to_exist_point_db(existed_point, point_to_add, data)
        add_point_to_group_of_points(grouped_all_points, point_to_add, grouping_creation_key)
    return point_to_add


def find_nearest_point(source_point, grouped_points):
    points_to_check = all_close_points_in_border(source_point, grouped_points, attribute='latitude', border=0.2)

    first_point = points_to_check.pop(0)
    min_distance = distance_between_points(source_point, first_point)
    nearset_point = first_point
    for point in points_to_check:
        distance_to_source = distance_between_points(source_point, point)
        if distance_to_source < min_distance:
            min_distance = distance_to_source
            nearset_point = point
    return nearset_point


def find_shortest_path(source_point, target_point):
    return graph_db.find_shortest_path(source_point, target_point)


@cache.cached(timeout=600, key_prefix='get_all_points_in_the_graph')
def get_all_points_in_the_graph():
    return graph_db.get_all_points_from_db()


# TODO - consider changing the terminology to roads instead of relations
@cache.cached(timeout=600, key_prefix='get_all_relations_in_the_graph')
def get_all_relations_in_the_graph():
    return graph_db.get_all_relations_from_db()


def clear_cache_of_all_points_and_relations():
    cache.delete_many('get_all_points_in_the_graph', 'get_all_relations_in_the_graph')
