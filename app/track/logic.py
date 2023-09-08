import geopandas as geopandas
import gpxpy
import gpxpy.gpx

import app.track.osm_service as osm_service
# import app.track.graph_service
# import folium
# import matplotlib
# import mapclassify

from app.track.utils import gpx2df, extract_points_of_gpx_track, GeoPoint, GeoRoad, CALCULATED_ROAD, \
    convert_geo_point_list_to_geo_road_list

from app.track.graph_service import add_point_to_graph, add_edge_to_graph, find_nearest_point, find_shortest_path


# TODO - support also wkt files
def load_track_from_gpx_file(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx


# def add_track_to_graph(gpx, track_id):
#     points = extract_points_of_gpx_track(gpx)
#     print(f'original number of points of the file: {len(points)}')  # debug
#     # reduced_points = reduce_points_in_track_based_on_distance(points)
#     reduced_points = points
#     print(f'after reduction number of points: {len(reduced_points)}')  # debug
#     prev_point = None
#     i = 1  # debug
#     for point_to_add in reduced_points:
#         print(f'{i}/{len(reduced_points)}')  # debug
#         new_point = add_point_to_graph(point_to_add)
#         if prev_point:
#             add_edge_to_graph(prev_point, new_point, {'track_id': track_id})
#         prev_point = new_point
#         i += 1  # debug

def add_track_to_graph(file_loader):
    points = file_loader.get_geo_points_from_file()
    print(f'original number of points of the file: {len(points)}')  # debug
    # reduced_points = reduce_points_in_track_based_on_distance(points)
    reduced_points = points
    print(f'after reduction number of points: {len(reduced_points)}')  # debug
    prev_point = None
    i = 1  # debug
    for point_to_add in reduced_points:
        print(f'{i}/{len(reduced_points)}')  # debug
        new_point = add_point_to_graph(point_to_add)
        if prev_point:
            add_edge_to_graph(prev_point, new_point, {'track_id': str(file_loader.track_id)})
        prev_point = new_point
        i += 1  # debug


def convert_gpx_to_geo_df(gpx):
    df = gpx2df(gpx)
    # todo - add extra data here
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude), crs='EPSG:2039')
    return gdf


# TODO - change naming of variables and functions - too long
def calculate_route(start_lng, start_lat, end_lng, end_lat):
    # Calculate the route from the start point to the first point on track
    start_point = GeoPoint(start_lng, start_lat)
    first_point_on_track = find_nearest_point(start_point)
    route_to_the_first_point_on_track = osm_service.get_route_between_two_points(start_point, first_point_on_track)

    # Initial the route and its segments (relations)
    route = route_to_the_first_point_on_track
    relations = convert_geo_point_list_to_geo_road_list(route_to_the_first_point_on_track)

    # Get the route from the graph service
    end_point = GeoPoint(end_lng, end_lat)
    last_point_on_track = find_nearest_point(end_point)

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
