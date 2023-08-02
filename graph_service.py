from db_service import Neo4jDB
from graph_logic import is_there_already_a_close_point_in_the_graph, distance_between_points, \
    are_the_same_point_by_coordinates

graph_db = Neo4jDB()


def add_point_to_graph(point_to_add):
    points = graph_db.get_all_points_from_db()
    collided_point = is_there_already_a_close_point_in_the_graph(point_to_add, points)
    if collided_point:
        point_to_add = collided_point
    else:
        point_to_add = graph_db.add_point_to_db(point_to_add)
    return point_to_add


def add_edge_to_graph(source_point, target_point):
    if not are_the_same_point_by_coordinates(source_point, target_point):
        graph_db.add_edge_to_db(source_point, target_point)


def find_nearest_point(source_point):
    all_points = graph_db.get_all_points_from_db()
    first_point = all_points.pop(0)
    min_distance = distance_between_points(source_point, first_point)
    nearset_point = first_point
    for point in all_points:
        distance_to_source = distance_between_points(source_point, point)
        if distance_to_source < min_distance:
            min_distance = distance_to_source
            nearset_point = point
    return nearset_point


def find_shortest_path(source_point, target_point):
    return graph_db.find_shortest_path(source_point, target_point)


def get_all_points_in_the_graph():
    return graph_db.get_all_points_from_db()
