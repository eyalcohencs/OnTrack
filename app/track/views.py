from flask_jwt_extended import jwt_required
from flask_login import login_required
import logging

from app.main import bp
from flask import request, make_response, jsonify, current_app

from app.track.graph_service import get_all_points_in_the_graph, get_all_relations_in_the_graph
from app.track.logic import calculate_route
from app.track.utils import jsonify_geo_points_list, jsonify_geo_roads_list


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
        # current_app.logger.setLevel(logging.INFO)

        current_app.logger.info('get_all_relations')
        current_app.logger.error('error get_all_relations')
        all_relations = get_all_relations_in_the_graph()
        return make_response(jsonify_geo_roads_list(all_relations), 200)
    except Exception as e:
        current_app.logger.info('get_all_relations ' + str(e))

        return make_response(jsonify(e), 405)


