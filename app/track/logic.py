import os
from enum import Enum

import app.track.osm_service as osm_service
from app.track.graph_logic import get_all_points_in_graph_by_grouping_of_attribute, are_the_same_point_by_coordinates, \
    are_two_points_too_close

from app.track.utils import GeoPoint, convert_geo_point_list_to_geo_road_list, create_key_for_point_grouping

from app.track.graph_service import add_point_to_graph, find_nearest_point, find_shortest_path, \
    get_all_points_in_the_graph, add_point_and_relation_to_exist_point_to_graph


class TrackLoadinSource(Enum):
    CLOUD = 'cloud'
    SERVER = 'server'


def add_track_to_graph(file_loader):
    points = file_loader.get_geo_points_from_file()
    print(f'original number of points of the file: {len(points)}')  # debug
    reduced_points = reduce_points_in_track_based_on_distance(points)  # reduced_points = points  #
    print(f'after reduction number of points: {len(reduced_points)}')  # debug

    all_points = get_all_points_in_the_graph()
    grouped_points = get_all_points_in_graph_by_grouping_of_attribute(all_points, create_key_for_point_grouping)

    prev_point = None
    point_counter = 1  # debug
    for point_to_add in reduced_points:
        print(f'{point_counter}/{len(reduced_points)}')  # debug
        if not prev_point:
            new_point = add_point_to_graph(point_to_add, grouped_points, create_key_for_point_grouping)
        else:
            new_point = add_point_and_relation_to_exist_point_to_graph(
                existed_point=prev_point,
                point_to_add=point_to_add,
                data={'track_id': str(file_loader.track_id)},
                grouped_all_points=grouped_points,
                grouping_creation_key=create_key_for_point_grouping)
        prev_point = new_point
        point_counter += 1  # debug


def reduce_points_in_track_based_on_distance(geo_points):
    gap_between_points_in_meters_for_reduction = os.environ['GAP_BETWEEN_POINTS_IN_METERS_FOR_REDUCTION']
    anchor_index = 0
    index = 1
    reduced_points = [geo_points[anchor_index]]
    final_index = len(geo_points) - 2
    while index <= final_index:
        anchor_point = geo_points[anchor_index]
        checked_point = geo_points[index]
        # Check if they are same is little faster than calculate distance
        if not are_the_same_point_by_coordinates(anchor_point, checked_point) \
                and not are_two_points_too_close(
                anchor_point, checked_point, int(gap_between_points_in_meters_for_reduction)):
            reduced_points.append(checked_point)
            anchor_index = index
        index = index + 1

    return reduced_points


# TODO - change naming of variables and functions - too long
def calculate_route(start_lng, start_lat, end_lng, end_lat):
    all_points = get_all_points_in_the_graph()
    grouped_points = get_all_points_in_graph_by_grouping_of_attribute(all_points, create_key_for_point_grouping)

    # Calculate the route from the start point to the first point on track
    start_point = GeoPoint(start_lng, start_lat)
    first_point_on_track = find_nearest_point(start_point, grouped_points)
    route_to_the_first_point_on_track = osm_service.get_route_between_two_points(start_point, first_point_on_track)

    # Initial the route and its segments (relations)
    route = route_to_the_first_point_on_track
    relations = convert_geo_point_list_to_geo_road_list(route_to_the_first_point_on_track)

    # Get the route from the graph service
    end_point = GeoPoint(end_lng, end_lat)
    last_point_on_track = find_nearest_point(end_point, grouped_points)

    if first_point_on_track.uuid != last_point_on_track.uuid:
        points_on_track, relations_on_track = find_shortest_path(first_point_on_track, last_point_on_track)
        route = route + points_on_track
        relations = relations + relations_on_track

    # Add the end point to the route and the last segments
    route_to_the_end_point_from_last_point_on_track = osm_service.get_route_between_two_points(last_point_on_track, end_point)
    relations_to_the_end_of_last_point_on_track = \
        convert_geo_point_list_to_geo_road_list(route_to_the_end_point_from_last_point_on_track)
    route = route + route_to_the_end_point_from_last_point_on_track
    relations.extend(relations_to_the_end_of_last_point_on_track)

    return route, relations
