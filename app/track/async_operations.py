import concurrent.futures
import logging
import os
import uuid
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor

import gpxpy
import gpxpy.gpx
import boto3

from app.extensions import mail
from app.track.logic import add_track_to_graph
from app.track.utils import GeoPoint, get_file_extension
from flask_mail import Message


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
        self.set_content()
        self.set_track_id()

    @abstractmethod
    def set_track_id(self):
        pass

    @abstractmethod
    def set_content(self):
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

    def set_track_id(self):
        self.track_id = uuid.uuid5(uuid.NAMESPACE_OID, str(self.content.tracks[0].segments[0].points))

    def set_content(self):
        if self.is_locale_file:
            self.content = self._load_track_from_gpx_file(self.path_to_file)
        else:
            s3 = self.s3_client if self.s3_client else get_s3_client()
            file = s3.get_object(Bucket=os.environ.get('AWS_STORAGE_BUCKET_NAME'), Key=self.path_to_file)
            self.content = gpxpy.parse(file['Body'].read())

    def get_geo_points_from_file(self):
        points = self._get_file_points()
        return self._convert_gpx_to_geo_point_list(points)

    def _get_file_points(self):
        return self.content.tracks[0].segments[0].points

    @staticmethod
    def _load_track_from_gpx_file(file_path):
        with open(file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        return gpx

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

    def set_track_id(self):
        pass

    def set_content(self):
        pass

    def get_geo_points_from_file(self):
        pass


# TODO - move to utils or dedicated service-file
def get_s3_client():
    return boto3.client('s3',
                        endpoint_url=os.environ['AWS_S3_ENDPOINT_URL'],
                        region_name=os.environ['AWS_REGION_NAME'],
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])


def create_file_loader(file_name, s3_client, is_locale_file):
    file_extension = get_file_extension(file_name)
    if file_extension is None:
        return None

    if file_extension == 'gpx':
        file_loader = GPXTrackLoader(path_to_file=file_name, s3_client=s3_client, is_locale_file=is_locale_file)
    elif file_extension == 'twl':
        file_loader = TWLTrackLoader(path_to_file=file_name, s3_client=s3_client, is_locale_file=is_locale_file)
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


def send_mail(recipients, sender, subject, message):
    msg = Message(subject=subject, sender=sender, recipients=recipients, body=message)
    mail.send(msg)


def create_file_loader_from_files_old(files_list, s3, is_locale_file, parallel_workers=10,):
    file_loaders = []
    with ThreadPoolExecutor(max_workers=parallel_workers) as executor:
        futures = [executor.submit(create_file_loader, file_name, s3, is_locale_file)
                   for file_name in files_list]
        number = 0
        for future in concurrent.futures.as_completed(futures):
            try:
                print(f'number {number}')
                result = future.result()
                file_loaders.append(result)
            except Exception as e:
                print(f'number exception {number}')

                logging.error(f'File loader worker ERROR: {e}')
            number = number + 1
    return file_loaders


def create_file_loader_from_files(files_list, s3, is_locale_file):
    file_loaders = []
    for file_name in files_list:
        print(f'create file loader for: {file_name}')
        file_loader = create_file_loader(file_name, s3, is_locale_file)
        file_loaders.append(file_loader)
    return file_loaders


def update_graph_db(app_context, current_user, load_tracks_from_bucket=True):
    try:
        with app_context:
            start_time = time.time()
            logging.info('Start update graph process...')

            if load_tracks_from_bucket:
                s3 = get_s3_client()
                is_locale_file = False
                files_list = get_list_of_tracks_from_bucket()
            else:
                s3 = None
                is_locale_file = True
                files_list = get_list_of_tracks_from_local_directory()
            logging.info(f'update-graph: {len(files_list)} candidate track files were found')

            file_loaders = create_file_loader_from_files(files_list, s3, is_locale_file)

            file_number = 1
            valid_files_loaders = [file_loader for file_loader in file_loaders if file_loader is not None]
            logging.info(f'update-graph: {len(valid_files_loaders)} file loaders available')
            for file_loader in valid_files_loaders:
                logging.info(f'load {file_number}/{len(valid_files_loaders)}: {file_loader.path_to_file}')
                add_track_to_graph(file_loader)
                # TODO - add here to save in table which files/tracks were loaded according to track_id
                file_number += 1
            end_time = time.time()
            elapsed_time = end_time - start_time
            recipient = current_user.email  # todo - pass user data from the client
            send_mail(subject='Update graph was finished',
                      sender='ontrackguide@gmail.com',
                      recipients=[recipient],
                      message=f'Process finish: {len(valid_files_loaders)} tracks were loaded successfully, '
                              f'it took {elapsed_time / 60} min for load {file_number} track files')
            logging.info('update-graph: mail was sent')
            logging.info(f'Finish update graph process!, it took {elapsed_time / 60} min')
    except Exception as e:
        logging.error(f'update-graph: error - {e}')
