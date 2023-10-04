import logging
import os
import uuid
from abc import ABC, abstractmethod

import boto3
import gpxpy
import pykml.parser as mkl_parser

from app.track.utils import get_file_extension, GeoPoint


class TrackFileLoader(ABC):
    def __init__(self, path_to_file, s3_client, file_type, is_locale_file=True):
        print(f'Start file loader creation: {path_to_file}')
        self.file_type = file_type
        self.path_to_file = path_to_file
        self._validate_file_type()
        self.content = None
        self.track_id = None
        self.s3_client = s3_client
        self.is_locale_file = is_locale_file
        self._set_content()
        self._set_track_id()

    def _set_content(self):
        if self.is_locale_file:
            self.content = self._get_content_from_local_file()
        else:
            s3 = self.s3_client if self.s3_client else get_s3_client()
            file = s3.get_object(Bucket=os.environ.get('AWS_STORAGE_BUCKET_NAME'), Key=self.path_to_file)
            self.content = self._parse_file_content_from_bucket(file)

    @abstractmethod
    def _get_file_points(self):
        pass

    def _set_track_id(self):
        self.track_id = uuid.uuid5(uuid.NAMESPACE_OID, str(self._get_file_points()))

    @abstractmethod
    def _get_content_from_local_file(self):
        pass

    @abstractmethod
    def _parse_file_content_from_bucket(self, file_content):
        pass

    def _validate_file_type(self):
        if not get_file_extension(self.path_to_file) == self.file_type:
            raise ValueError(f'file is not from type {self.file_type}')

    @abstractmethod
    def get_geo_points_from_file(self):
        pass


class GPXTrackLoader(TrackFileLoader):
    FILE_TYPE = 'gpx'

    def __init__(self, path_to_file, s3_client=None, is_locale_file=True):
        super().__init__(path_to_file=path_to_file, s3_client=s3_client,
                         file_type=self.FILE_TYPE,  is_locale_file=is_locale_file)

    def _get_content_from_local_file(self):
        with open(self.path_to_file, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        return gpx

    def _parse_file_content_from_bucket(self, file_content):
        return gpxpy.parse(file_content['Body'].read())

    def _get_file_points(self):
        return self.content.tracks[0].segments[0].points

    def get_geo_points_from_file(self):
        points = self._get_file_points()
        return self._convert_gpx_to_geo_point_list(points)

    @staticmethod
    def _convert_gpx_to_geo_point_list(points_to_convert):
        geo_points = []
        for point in points_to_convert:
            altitude = point.elevation if hasattr(point, 'elevation') else point.altitude
            geo_points.append(GeoPoint(point.longitude, point.latitude, altitude, point.time, uuid=None))
        return geo_points


# TODO - implement TWL file loader
class TWLTrackLoader(TrackFileLoader):
    FILE_TYPE = 'twl'

    def __init__(self, path_to_file, s3_client=None, is_locale_file=True):
        super().__init__(path_to_file=path_to_file, s3_client=s3_client,
                         file_type=self.FILE_TYPE,  is_locale_file=is_locale_file)
        logging.error(f' File {path_to_file} can not be loaded, TWL Track Loader is under construction')

    def _get_content_from_local_file(self):
        return None

    def _parse_file_content_from_bucket(self, file_content):
        return ''

    def _get_file_points(self):
        return []

    def get_geo_points_from_file(self):
        return []


class KMLTrackLoader(TrackFileLoader):
    FILE_TYPE = 'kml'

    def __init__(self, path_to_file, s3_client=None, is_locale_file=True):
        super().__init__(path_to_file=path_to_file, s3_client=s3_client,
                         file_type=self.FILE_TYPE,  is_locale_file=is_locale_file)

    def _get_content_from_local_file(self):

        with open(self.path_to_file, 'rb') as kml_file:
            content = kml_file.read()
            kml = mkl_parser.fromstring(content)
        return kml

    def _parse_file_content_from_bucket(self, file_content):
        kml = mkl_parser.fromstring(file_content['Body'].read())
        return kml

    def _get_file_points(self):
        placemarks = self.content.Document.Placemark
        points = [tuple(coords.split(',')) for coords in placemarks.LineString.coordinates.text.split()]
        return points

    def get_geo_points_from_file(self):
        points = self._get_file_points()
        return self._convert_kml_points_to_geo_points(points)

    @staticmethod
    def _convert_kml_points_to_geo_points(kml_points):
        geo_points = []
        for point in kml_points:
            geo_points.append(GeoPoint(point[1], point[0], altitude=None, time=None, uuid=None))
        return geo_points


def get_s3_client():
    return boto3.client('s3',
                        endpoint_url=os.environ['AWS_S3_ENDPOINT_URL'],
                        region_name=os.environ['AWS_REGION_NAME'],
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])


def create_file_loader(file_name, s3_client, is_locale_file):
    file_extension = get_file_extension(file_name)

    if file_extension == GPXTrackLoader.FILE_TYPE:
        file_loader = GPXTrackLoader(path_to_file=file_name, s3_client=s3_client, is_locale_file=is_locale_file)
    elif file_extension == KMLTrackLoader.FILE_TYPE:
        file_loader = KMLTrackLoader(path_to_file=file_name, s3_client=s3_client, is_locale_file=is_locale_file)
    elif file_extension == TWLTrackLoader.FILE_TYPE:
        return None  # placeholder for TWL
    else:
        return None

    return file_loader


def get_list_of_tracks_from_bucket():
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    s3 = get_s3_client()
    response = s3.list_objects(Bucket=bucket_name)
    files_list = [obj['Key'] for obj in response.get('Contents', [])]
    return files_list


def get_list_of_tracks_from_local_directory():
    locale_tracks_directory = os.environ['LOCALE_TRACKS_DIRECTORY_PATH']
    return [os.path.join(locale_tracks_directory, file_name) for file_name in os.listdir(locale_tracks_directory)
            if os.path.isfile(os.path.join(locale_tracks_directory, file_name))]


def create_file_loader_from_files(files_list, s3, is_locale_file):
    file_loaders = []
    for file_name in files_list:
        print(f'create file loader for: {file_name}')
        file_loader = create_file_loader(file_name, s3, is_locale_file)
        file_loaders.append(file_loader)
    return file_loaders
