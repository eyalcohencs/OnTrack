from enum import Enum
from itertools import chain

import numpy as np

CALCULATED_ROAD = 'CALCULATED_ROAD'


class SearchPointBorder(Enum):
    NEAR = 0.01
    CLOSE = 0.2
    FAR = 0.5


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


def create_key_for_point_grouping(element, attribute='latitude'):
    """ The given function for grouping points """
    return str(getattr(element, attribute))[0:5]


def create_range_of_keys_for_points_grouping(element, attribute='latitude', border=SearchPointBorder.NEAR.value):
    element_key = create_key_for_point_grouping(element, attribute)
    min_border = float(element_key)-border
    max_border = float(element_key)+border
    return [str(key)[0:5] for key in np.arange(min_border, max_border, SearchPointBorder.NEAR.value)]


def all_close_points_in_border(source_point, grouped_points, attribute='latitude', border=SearchPointBorder.NEAR.value):
    """ The function grouping points together in order for making "close point" search more efficient -
    we don't really need to check all points in the graph. """
    grouping_keys = create_range_of_keys_for_points_grouping(source_point, attribute, border)
    close_points = list(chain.from_iterable(
        map(lambda key: grouped_points[key] if key in grouped_points else [], grouping_keys)))
    return close_points
