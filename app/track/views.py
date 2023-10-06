import logging
import threading
from flask import request, make_response, jsonify, current_app
from flask_jwt_extended import jwt_required

from app.track import bp
from app.track.async_operations import update_graph_db
from app.track.graph_service import get_all_points_in_the_graph, get_all_roads_in_the_graph
from app.track.logic import calculate_route, TrackLoadinSource
from app.track.utils import jsonify_geo_points_list, jsonify_geo_roads_list
from app.user.logic import get_current_user_details


@bp.route('/get_route', methods=['GET'])
@jwt_required()
def get_route():
    """
    View for getting the route between user's points.
    The view gets start and end points coordinates
    and return dict with list of points and roads that describe the calculated route.
    :return: json dict with points and roads of the calculated route.
    """
    start_lat = request.args.get('start_lat')
    start_lng = request.args.get('start_lng')
    end_lat = request.args.get('end_lat')
    end_lng = request.args.get('end_lng')

    points, roads = calculate_route(start_lng, start_lat, end_lng, end_lat)
    jsonified_points = jsonify_geo_points_list(points)
    jsonified_roads = jsonify_geo_roads_list(roads)
    result = {'points': jsonified_points,
              'roads': jsonified_roads}
    return result


@bp.route('/get_all_points', methods=['GET'])
@jwt_required()
def get_all_points():
    """
    :return: 200 response and all points in graph DB
    """
    all_points = get_all_points_in_the_graph()
    return jsonify_geo_points_list(all_points)


@bp.route('/get_all_roads', methods=['GET'])
@jwt_required()
def get_all_roads():
    """
    :return: 200 response and all roads in graph DB
    """
    try:
        all_roads = get_all_roads_in_the_graph()
        return make_response(jsonify_geo_roads_list(all_roads), 200)
    except Exception as e:
        current_app.logger.error('EXCEPTION get_all_roads ' + str(e))

        return make_response(jsonify(e), 405)


@bp.route('/start_update_graph_db', methods=['POST'])
@jwt_required()
def start_update_graph_db():
    """
    The function updates and adds new tracks, from different sources, and notify it to the user via email.
    It runs on side thread.
    :return: response
    """
    loading_source = request.get_json()['loading_source']
    is_cloud_source = True if loading_source == TrackLoadinSource.CLOUD.value else False
    logging.info('Enter view of update graph process...')
    logging.error('Enter view of update graph process...')
    current_user = get_current_user_details()
    thread = threading.Thread(target=update_graph_db, args=(current_app.app_context(), current_user, is_cloud_source))
    thread.start()

    return make_response(jsonify('Update graph with new tracks started.'), 200)


