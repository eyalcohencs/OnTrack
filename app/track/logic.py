import os
from enum import Enum

import app.track.osm_service as osm_service
from app.track.graph_logic import get_all_points_in_graph_by_grouping_of_attribute, are_the_same_point_by_coordinates, \
    are_two_points_too_close

from app.track.utils import GeoPoint, convert_geo_point_list_to_geo_road_list, create_key_for_point_grouping, \
    SearchPointBorder

from app.track.graph_service import add_point_to_graph, find_nearest_point, find_shortest_path, \
    get_all_points_in_the_graph, add_point_and_relation_to_exist_point_to_graph


class TrackLoadinSource(Enum):
    CLOUD = 'cloud'
    SERVER = 'server'


def add_track_to_graph(file_loader):
    points = file_loader.get_geo_points_from_file()
    print(f'original number of points of the file: {len(points)}')  # debug
    reduced_points = reduce_points_in_track_based_on_distance(points)  # reduced_points = points
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
        # Check if they are the same is little faster than calculate distance
        if not are_the_same_point_by_coordinates(anchor_point, checked_point) \
                and not are_two_points_too_close(
                anchor_point, checked_point, int(gap_between_points_in_meters_for_reduction)):
            reduced_points.append(checked_point)
            anchor_index = index
        index = index + 1

    return reduced_points


def calculate_route(start_lng, start_lat, end_lng, end_lat):
    """
    This function gets the user first and last position of the track
    and the function retrieve a list of coords and routes of the track.
    The function first try to find close point to start with, but if it fails it tries to enlarge the search area.
    The reason for making two searches, is that the search is pretty heavy, so under the assumption that most of the
    places we could find a close point, going to search in large area will be less common.

    @:param start_lng, start_lat - coordinates of the user start point
    @:param end_lng, end_lat - coordinates of the user end point
    @:return route - list of GeoPoint of the calculated track
    @:return roads - list of roads of the calculated track
    """
    all_points = get_all_points_in_the_graph()
    grouped_points = get_all_points_in_graph_by_grouping_of_attribute(all_points, create_key_for_point_grouping)
    start_point = GeoPoint(start_lng, start_lat)
    end_point = GeoPoint(end_lng, end_lat)

    # Get the closest point on track to start point
    first_point_on_track = find_nearest_point(start_point, grouped_points)
    if first_point_on_track is None:  # if no close point is found, search in larger area
        first_point_on_track = find_nearest_point(start_point, grouped_points, border=SearchPointBorder.FAR.value)
        if first_point_on_track is None:  # if no close point is found, calculate route straight to the end point
            try:
                route = osm_service.get_route_between_two_points(
                    start_point, end_point, profile=osm_service.TypeOfDrivingProfile.CYCLING_MOUNTAIN.value)
                roads = convert_geo_point_list_to_geo_road_list(route)
            except Exception as e:
                route = roads = []
            return route, roads

    # Get the closest point on track to end point
    last_point_on_track = find_nearest_point(end_point, grouped_points)
    if last_point_on_track is None:  # if no close point is found, search in larger area
        last_point_on_track = find_nearest_point(end_point, grouped_points, border=SearchPointBorder.FAR.value)
        if last_point_on_track is None:  # if no close point is found, calculate route straight to the end point
            try:
                route = osm_service.get_route_between_two_points(
                    first_point_on_track, end_point, profile=osm_service.TypeOfDrivingProfile.CYCLING_MOUNTAIN.value)
                roads = convert_geo_point_list_to_geo_road_list(route)
            except Exception as e:
                route = roads = []
            return route, roads

    # Get route from the graph service
    if first_point_on_track.uuid != last_point_on_track.uuid:
        track_route, roads_on_track = find_shortest_path(first_point_on_track, last_point_on_track)
        if not track_route:
            track_route = osm_service.get_route_between_two_points(first_point_on_track, last_point_on_track)
    else:
        track_route = []

    # Calculate route
    try:
        route_to_the_first_point_on_track = osm_service.get_route_between_two_points(start_point, first_point_on_track)
        route_to_the_end_point_from_last_point_on_track = osm_service.get_route_between_two_points(last_point_on_track, end_point)
    except Exception as e:
        route_to_the_first_point_on_track = route_to_the_end_point_from_last_point_on_track = []
    route = route_to_the_first_point_on_track + track_route + route_to_the_end_point_from_last_point_on_track
    roads = convert_geo_point_list_to_geo_road_list(route)

    return route, roads
