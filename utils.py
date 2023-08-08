import pandas as pd

from graph_logic import are_the_same_point_by_coordinates, are_two_points_too_close

GAP_BETWEEN_POINTS_IN_METERS_FOR_REDUCTION = 50


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
    def __init__(self, source_geo_point, target_geo_point, color=None):
        self.uuid = (source_geo_point.uuid or 'None') + '::' + (target_geo_point.uuid or 'None')
        self.source_geo_point = source_geo_point
        self.target_geo_point = target_geo_point
        self.color = color

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'source_geo_point': self.source_geo_point.to_dict(),
            'target_geo_point': self.target_geo_point.to_dict(),
            'color': self.color
        }

    def to_list_of_coordinates(self):
        return [[self.source_geo_point.latitude, self.source_geo_point.longitude],
                [self.target_geo_point.latitude, self.target_geo_point.longitude]]

    def __str__(self):
        return f'{self.uuid} | {self.color}'


def gpx2df(gpx):
    data = gpx.tracks[0].segments[0].points

    df = pd.DataFrame(columns=['longitude', 'latitude', 'altitude', 'time'])
    for point in data:
        df = pd.concat([df, pd.DataFrame([
            {'longitude': point.longitude,
             'latitude': point.latitude,
             'altitude': point.altitude,
             'time': point.time}])
                        ], ignore_index=True)

    # df['time'] = df['time'].astype(str)
    df['time'] = pd.to_datetime(df['time'], dayfirst=True)
    return df


def extract_points_of_gpx_track(gpx_track_data):
    gpx_points = gpx_track_data.tracks[0].segments[0].points
    # Todo - This is the place to add additional data like track difficulty
    return create_geo_point_list(gpx_points)


def reduce_points_in_track_based_on_distance(geo_points):
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
                anchor_point, checked_point, GAP_BETWEEN_POINTS_IN_METERS_FOR_REDUCTION):
            reduced_points.append(checked_point)
            anchor_index = index
        index = index + 1

    return reduced_points


def create_geo_point_list(points_to_convert):
    geo_points = []
    for point in points_to_convert:
        altitude = point.elevation if hasattr(point, 'elevation') else point.altitude
        geo_points.append(GeoPoint(point.longitude, point.latitude, altitude, point.time, uuid=None))
    return geo_points


def jsonify_geo_points_list(geo_point_list):
    return [point.to_dict() for point in geo_point_list]


def jsonify_geo_roads_list(geo_road_list):
    return [road.to_dict() for road in geo_road_list]
