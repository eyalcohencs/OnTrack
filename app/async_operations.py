import os
import uuid
from abc import ABC, abstractmethod

from app.track.logic import load_track_from_gpx_file, add_track_to_graph
from app.track.utils import GeoPoint, end_of_file_ends_with

TRACKS_DIRECTORY_PATH = '../data/tracks/'


class TrackFileLoader(ABC):
    def __init__(self, path_to_file, file_type):
        self.file_type = file_type
        self.path_to_file = path_to_file
        self._validate_file_type()
        self.content = None
        self.track_id = None
        self.set_content()
        self.set_track_id()

    @abstractmethod
    def set_track_id(self):
        pass

    @abstractmethod
    def set_content(self):
        pass

    def _validate_file_type(self):
        # if self.path_to_file[-4:] != self.file_type:
        if not end_of_file_ends_with(self.path_to_file, self.file_type):
            raise ValueError(f'file is not from type {self.file_type}')

    @abstractmethod
    def get_geo_points_from_file(self):
        pass


class GPXTrackLoader(TrackFileLoader):
    FILE_TYPE = '.gpx'

    def __init__(self, path_to_file):
        super().__init__(path_to_file=path_to_file, file_type=self.FILE_TYPE)

    def set_track_id(self):
        self.track_id = uuid.uuid5(uuid.NAMESPACE_OID, str(self.content.tracks[0].segments[0].points))

    def set_content(self):
        self.content = load_track_from_gpx_file(self.path_to_file)

    def get_geo_points_from_file(self):
        points = self._get_file_points()
        return self._convert_gpx_to_geo_point_list(points)

    def _get_file_points(self):
        return self.content.tracks[0].segments[0].points

    @staticmethod
    def _convert_gpx_to_geo_point_list(points_to_convert):
        geo_points = []
        for point in points_to_convert:
            altitude = point.elevation if hasattr(point, 'elevation') else point.altitude
            geo_points.append(GeoPoint(point.longitude, point.latitude, altitude, point.time, uuid=None))
        return geo_points


class TWLTrackLoader(TrackFileLoader):
    FILE_TYPE = '.twl'

    def __init__(self, path_to_file):
        super().__init__(path_to_file=path_to_file, file_type=self.FILE_TYPE)

    def set_track_id(self):
        pass

    def set_content(self):
        pass

    def get_geo_points_from_file(self):
        pass


# TODO - should be asynchronicity script, use bucket to get the gpx files
# def update_graph_db():
#     # Todo - for each file in track directory load the gpx file into geopandas
#     # loading file should be in a different function
#     files = [file_name for file_name in os.listdir(TRACKS_DIRECTORY_PATH)
#              if os.path.isfile(os.path.join(TRACKS_DIRECTORY_PATH, file_name))]
#     file_number = 1
#     for file_name in files:
#         if file_name[-4:] != ".gpx":
#             continue
#         print(f'files to load {file_number}/{len(files)}')  # debug
#         print(f'load: {file_name}')  # debug
#         file_path = TRACKS_DIRECTORY_PATH + file_name
#         gpx = load_track_from_gpx_file(file_path)
#         track_id = uuid.uuid5(uuid.NAMESPACE_OID, str(gpx.tracks[0].segments[0].points))
#         print('track_id: ' + str(track_id))
#         # add_track_to_graph(gpx, track_id)
#         file_number += 1

def update_graph_db():
    # Todo - for each file in track directory load the gpx file into geopandas
    # loading file should be in a different function
    files = [file_name for file_name in os.listdir(TRACKS_DIRECTORY_PATH)
             if os.path.isfile(os.path.join(TRACKS_DIRECTORY_PATH, file_name))]
    file_number = 1
    for file_name in files:
        print(f'files to load {file_number}/{len(files)}')  # debug
        print(f'load: {file_name}')  # debug
        file_path = TRACKS_DIRECTORY_PATH + file_name

        if end_of_file_ends_with(file_path, '.gpx'):
            file_loader = GPXTrackLoader(file_path)
        elif end_of_file_ends_with(file_path, '.twl'):
            file_loader = TWLTrackLoader(file_path)
        else:
            continue
        add_track_to_graph(file_loader)
        file_number += 1


# LOAD TRACKS FROM FILES
if __name__ == '__main__':
    update_graph_db()
