import os
from enum import Enum

import openrouteservice
from flask import current_app

from app.track.utils import convert_coordinates_list_to_geo_point_list


class TypeOfDrivingProfile(Enum):
    DRIVING_CAR = 'driving-car'
    CYCLING_REGULAR = 'cycling-regular'
    CYCLING_ROAD = 'cycling-road'
    CYCLING_MOUNTAIN = 'cycling-mountain'
    FOOT_HIKING = 'foot-hiking'


def get_osm_client():
    key_api = os.environ.get('OSM_KEY_API')
    return openrouteservice.Client(key=key_api)


def get_route_between_two_points(source_point, target_point, profile=TypeOfDrivingProfile.DRIVING_CAR.value):
    client = get_osm_client()
    coords = ((source_point.longitude, source_point.latitude), (target_point.longitude, target_point.latitude))
    geometry = client.directions(coords, profile)['routes'][0]['geometry']
    coords_list = openrouteservice.convert.decode_polyline(geometry)['coordinates']
    route = convert_coordinates_list_to_geo_point_list(coords_list)
    return route
