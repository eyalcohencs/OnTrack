import os

from app.track.graph_logic import are_the_same_point_by_coordinates, are_two_points_too_close

CALCULATED_ROAD = 'CALCULATED_ROAD'


class GeoPoint:
    def __init__(self, longitude, latitude, altitude=None, time=None, uuid=None):
        self.uuid = uuid
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.time = time

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'altitude': self.altitude,
            'time': self.time
        }

    def __str__(self):
        return f'{self.longitude} <> {self.latitude} | {self.altitude} | {self.time}'


class GeoRoad:
    def __init__(self, source_geo_point, target_geo_point, track_id=None):
        self.uuid = (source_geo_point.uuid or 'None') + '::' + (target_geo_point.uuid or 'None')
        self.source_geo_point = source_geo_point
        self.target_geo_point = target_geo_point
        # TODO - change color name to track_index
        self.track_id = track_id

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'source_geo_point': self.source_geo_point.to_dict(),
            'target_geo_point': self.target_geo_point.to_dict(),
            'track_id': self.track_id
        }

    def to_list_of_coordinates(self):
        return [[self.source_geo_point.latitude, self.source_geo_point.longitude],
                [self.target_geo_point.latitude, self.target_geo_point.longitude]]

    def __str__(self):
        return f'{self.uuid} | {self.track_id}'


# todo - check if the function is in the right file, maybe graph_logic
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


def convert_coordinates_list_to_geo_point_list(coords_list):
    return [GeoPoint(coord[0], coord[1]) for coord in coords_list]


def convert_geo_point_list_to_geo_road_list(geo_point_list):
    geo_road_list = []
    for i in range(0, len(geo_point_list) - 1):
        geo_road_list.append(GeoRoad(geo_point_list[i], geo_point_list[i+1], track_id=CALCULATED_ROAD))
    return geo_road_list


def jsonify_geo_points_list(geo_point_list):
    return [point.to_dict() for point in geo_point_list]


def jsonify_geo_roads_list(geo_road_list):
    return [road.to_dict() for road in geo_road_list]


def get_file_extension(file_name):
    parts = file_name.split(".")
    if len(parts) > 1:
        extension = parts[-1]
        return extension
    else:
        return None
