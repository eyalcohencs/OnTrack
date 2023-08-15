from geopy import distance

# import gpxpy.geo

GAP_BETWEEN_POINTS_IN_METERS_FOR_CALCULATE_ROUTE = 30


def are_two_points_too_close(point1, point2, gap=GAP_BETWEEN_POINTS_IN_METERS_FOR_CALCULATE_ROUTE):
    points_distance = distance_between_points(point1, point2)
    return points_distance.meters <= gap


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


def is_there_already_a_close_point_in_the_graph(point_to_add, points_in_graph):
    close_point = None
    for point in points_in_graph:
        if are_the_same_point_by_coordinates(point_to_add, point) \
                or are_two_points_too_close(point_to_add, point):
            close_point = point
            break
    return close_point


# def create_track(start_lat, start_lng, end_lat, end_lng):
