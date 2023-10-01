import logging
import threading
from flask import request, make_response, jsonify, current_app
from flask_jwt_extended import jwt_required
from flask_login import login_required

from app.track import bp
from app.track.async_operations import update_graph_db
from app.track.graph_service import get_all_points_in_the_graph, get_all_relations_in_the_graph
from app.track.logic import calculate_route, TrackLoadinSource
from app.track.utils import jsonify_geo_points_list, jsonify_geo_roads_list
from app.user.logic import get_current_user_details


@bp.route('/get_route', methods=['GET'])
@login_required
@jwt_required()
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


@bp.route('/get_all_points', methods=['GET'])
@login_required
@jwt_required()
def get_all_points():
    all_points = get_all_points_in_the_graph()
    return jsonify_geo_points_list(all_points)


@bp.route('/get_all_relations', methods=['GET'])
@login_required
@jwt_required()
def get_all_relations():
    try:
        all_relations = get_all_relations_in_the_graph()
        return make_response(jsonify_geo_roads_list(all_relations), 200)
    except Exception as e:
        current_app.logger.error('EXCEPTION get_all_relations ' + str(e))

        return make_response(jsonify(e), 405)


@bp.route('/start_update_graph_db', methods=['POST'])
@jwt_required()
def start_update_graph_db():
    loading_source = request.get_json()['loading_source']
    is_cloud = True if loading_source == TrackLoadinSource.CLOUD.value else False
    logging.info('Enter view of update graph process...')
    logging.error('Enter view of update graph process...')
    current_user = get_current_user_details()
    thread = threading.Thread(target=update_graph_db, args=(current_app.app_context(), current_user, is_cloud))
    thread.start()

    return make_response(jsonify('good'), 200)


