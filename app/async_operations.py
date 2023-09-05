import os
import uuid

from app.track.logic import load_track_from_gpx_file, add_track_to_graph

TRACKS_DIRECTORY_PATH = '../data/tracks/'


# TODO - should be asynchronicity script, use bucket to get the gpx files
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
        gpx = load_track_from_gpx_file(file_path)
        track_id = uuid.uuid5(uuid.NAMESPACE_X500, gpx)
        add_track_to_graph(gpx, track_id)
        file_number += 1


# LOAD TRACKS FROM FILES
update_graph_db()
