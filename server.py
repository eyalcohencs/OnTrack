import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from graph_service import get_all_points_in_the_graph, get_all_relations_in_the_graph
from logic import load_track_from_gpx_file, add_track_to_graph, calculate_route
from utils import jsonify_geo_points_list, jsonify_geo_roads_list

app = Flask(__name__)
CORS(app)  # todo - remove before deployment

TRACKS_DIRECTORY_PATH = 'data/tracks/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_route', methods=['GET'])
def get_route():
    start_lat = request.args.get('start_lat')
    start_lng = request.args.get('start_lng')
    end_lat = request.args.get('end_lat')
    end_lng = request.args.get('end_lng')

    points, relations = calculate_route(start_lng, start_lat, end_lng, end_lat)
    jsonified_points = jsonify_geo_points_list(points)
    jsonified_roads = jsonify_geo_roads_list(relations)
    result = {'points': jsonified_points,
              'roads': jsonified_roads}
    return result


@app.route('/get_all_points', methods=['GET'])
def get_all_points():
    all_points = get_all_points_in_the_graph()
    return jsonify_geo_points_list(all_points)


@app.route('/get_all_relations', methods=['GET'])
def get_all_relations():
    all_relations = get_all_relations_in_the_graph()
    return jsonify_geo_roads_list(all_relations)


# should be asynchronicity script, use bucket to get the gpx files
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
        add_track_to_graph(gpx, file_number)
        file_number += 1


# LOAD TRACKS FROM FILES
# update_graph_db()

# RUN SERVER
if __name__ == '__main__':
    app.run(port=8001)
