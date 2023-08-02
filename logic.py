import geopandas as geopandas
import gpxpy
import gpxpy.gpx

import graph_service
# import folium
# import matplotlib
# import mapclassify

from utils import gpx2df, extract_points_of_gpx_track, reduce_points_in_track_based_on_distance, GeoPoint

from graph_service import add_point_to_graph, add_edge_to_graph


# TODO - support also wkt files
def load_track_from_gpx_file(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx


def add_track_to_graph(gpx):
    points = extract_points_of_gpx_track(gpx)
    print(f'original number of points of the file: {len(points)}')  # debug
    reduced_points = reduce_points_in_track_based_on_distance(points)
    # reduced_points = points
    print(f'after reduction number of points: {len(reduced_points)}')  # debug
    prev_point = None
    i = 1  # debug
    for point_to_add in reduced_points:
        print(f'{i}/{len(reduced_points)}')  # debug
        new_point = add_point_to_graph(point_to_add)
        if prev_point:
            add_edge_to_graph(prev_point, new_point)
        prev_point = new_point
        i = i + 1  # debug


def convert_gpx_to_geo_df(gpx):
    df = gpx2df(gpx)
    # todo - add extra data here
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude), crs='EPSG:2039')
    return gdf


def calculate_route(start_lng, start_lat, end_lng, end_lat):
    # start_lng = 35.58170362041667  # uuid 	d92fdb0b-a140-46e2-affd-a7a4905ac2a9
    # start_lat = 33.168924768166036
    # end_lng = 35.59031166796374  # uuid 737c4cca-a359-45a4-ac09-f6d6ac875eb5
    # end_lat = 33.1658500175496

    start_point = GeoPoint(start_lng, start_lat)
    route = [start_point]
    first_point_on_track = graph_service.find_nearest_point(start_point)
    end_point = GeoPoint(end_lng, end_lat)
    last_point_on_track = graph_service.find_nearest_point(end_point)
    if first_point_on_track.uuid != last_point_on_track.uuid:
        track = graph_service.find_shortest_path(first_point_on_track, last_point_on_track)
        route = route + track
    route.append(end_point)
    return route
