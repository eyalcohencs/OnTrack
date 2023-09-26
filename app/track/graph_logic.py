import os

from geopy import distance


def are_two_points_too_close(point1, point2, gap=None):
    gap = os.environ['GAP_BETWEEN_POINTS_IN_METERS_FOR_CALCULATE_ROUTE'] if gap is None else gap
    points_distance = distance_between_points(point1, point2)
    return points_distance.meters <= int(gap)


def are_the_same_point_by_coordinates(point1, point2):
    return point1.latitude == point2.latitude and point1.longitude == point2.longitude


def distance_between_points(geo_point1, geo_point2):
    # TODO - delete comment when you are sure that this is the best option to measure distance
    # point1_lat = point1.latitude
    # point1_long = point1.longitude
    # point1_elv = point1.altitude
    # point2_lat = point2.latitude
    # point2_long = point2.longitude
    # point2_elv = point2.altitude
    # distance = gpxpy.geo.distance(point1_lat, point1_long, point1_elv, point2_lat, point2_long, point2_elv)
    return distance.geodesic((geo_point1.latitude, geo_point1.longitude), (geo_point2.latitude, geo_point2.longitude))


def is_there_already_a_close_point_in_the_graph(point_to_add, grouped_points, create_key):
    key = create_key(point_to_add)
    prev_section_key = str(float(key) - 0.01)[0:5]
    next_section_key = str(float(key) + 0.01)[0:5]
    points_to_check = grouped_points[key][:]  # shallow copy
    if prev_section_key in grouped_points:
        points_to_check += grouped_points[prev_section_key]
    if next_section_key in grouped_points:
        points_to_check += grouped_points[next_section_key]
    close_point = None
    for point in points_to_check:
        if are_the_same_point_by_coordinates(point_to_add, point) \
                or are_two_points_too_close(point_to_add, point):
            close_point = point
            break
    return close_point


def get_all_points_in_graph_by_grouping_of_attribute(points_to_group, create_key, attribute='longitude'):
    grouped_points = {}
    for point in points_to_group:
        add_point_to_group_of_points(grouped_points, point, create_key, attribute)
    return grouped_points


def add_point_to_group_of_points(grouped_points, point_to_add, creation_key_function, attribute_to_grouped_by='longitude'):
    key = creation_key_function(point_to_add, attribute_to_grouped_by)
    if key not in grouped_points:
        grouped_points[key] = []
    grouped_points[key].append(point_to_add)
