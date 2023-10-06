import logging
import time

from app.extensions import mail
from app.track.file_loader_service import get_s3_client, get_list_of_tracks_from_bucket, \
    get_list_of_tracks_from_local_directory, create_file_loader_from_files
from app.track.logic import add_track_to_graph
from flask_mail import Message


def send_mail(recipients, sender, subject, message):
    msg = Message(subject=subject, sender=sender, recipients=recipients, body=message)
    mail.send(msg)


def update_graph_db(app_context, current_user, load_tracks_from_bucket=True):
    """
    The function loads tracks files from bucket or locally and updating the DB with all the coordinates (points) and
    roads (relations). The function is called by separate thread, there for it needs the app context.
    :param app_context: Flask app object context
    :param current_user: The user who run the operation
    :param load_tracks_from_bucket: True for loading files from bucket, False for locally
    :return: Void, but send mail to the current_user at completion with some statistics.
    """
    try:
        with app_context:
            start_time = time.time()
            logging.info('Start update graph process...')
            logging.error('Start update graph process...')  # todo - debug remove

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
                file_number += 1
            end_time = time.time()
            elapsed_time = end_time - start_time
            recipient = current_user.email
            send_mail(subject='Update graph was finished',
                      sender='ontrackguide@gmail.com',
                      recipients=[recipient],
                      message=f'Process finish: {len(valid_files_loaders)} tracks were loaded successfully, '
                              f'it took {elapsed_time / 60} min for load {file_number} track files')
            logging.info('update-graph: mail was sent')
            logging.info(f'Finish update graph process!, it took {elapsed_time / 60} min')
    except Exception as e:
        logging.error(f'update-graph: error - {e}')
