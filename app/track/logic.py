import geopandas as geopandas
import gpxpy
import gpxpy.gpx

# import app.track.graph_service
# import folium
# import matplotlib
# import mapclassify

from app.track.utils import gpx2df, extract_points_of_gpx_track, GeoPoint, GeoRoad

from app.track.graph_service import add_point_to_graph, add_edge_to_graph, find_nearest_point, find_shortest_path


# TODO - support also wkt files
def load_track_from_gpx_file(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx


def add_track_to_graph(gpx, file_number):
    points = extract_points_of_gpx_track(gpx)
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
            add_edge_to_graph(prev_point, new_point, {'color': file_number})
        prev_point = new_point
        i += 1  # debug


def convert_gpx_to_geo_df(gpx):
    df = gpx2df(gpx)
    # todo - add extra data here
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude), crs='EPSG:2039')
    return gdf


def calculate_route(start_lng, start_lat, end_lng, end_lat):
    start_point = GeoPoint(start_lng, start_lat)
    first_point_on_track = find_nearest_point(start_point)
    end_point = GeoPoint(end_lng, end_lat)
    last_point_on_track = find_nearest_point(end_point)
    first_road_on_track = GeoRoad(start_point, first_point_on_track)
    last_road_on_track = GeoRoad(end_point, last_point_on_track)

    route = [start_point]
    relations = [first_road_on_track]
    if first_point_on_track.uuid != last_point_on_track.uuid:
        points_on_track, relations_on_track = find_shortest_path(first_point_on_track, last_point_on_track)
        route = route + points_on_track
        relations = relations + relations_on_track
    route.append(end_point)
    relations.append(last_road_on_track)
    return route, relations
