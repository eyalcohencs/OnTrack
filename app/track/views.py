from flask_login import login_required

from app.main import bp
from flask import request

from app.track.graph_service import get_all_points_in_the_graph, get_all_relations_in_the_graph
from app.track.logic import calculate_route
from app.track.utils import jsonify_geo_points_list, jsonify_geo_roads_list


# TODO - guard with user login
@bp.route('/get_route', methods=['GET'])
@login_required
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
def get_all_points():
    all_points = get_all_points_in_the_graph()
    return jsonify_geo_points_list(all_points)


@bp.route('/get_all_relations', methods=['GET'])
def get_all_relations():
    all_relations = get_all_relations_in_the_graph()
    return jsonify_geo_roads_list(all_relations)

