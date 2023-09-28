from flask import make_response, current_app, jsonify
import threading

from flask_jwt_extended import jwt_required

from update_graph_service.async_operations import update_graph_db
from update_graph_service.main import bp


@bp.route('/start_update_graph_db', methods=['POST'])
@jwt_required()
def start_update_graph_db():
    # current_user = get_jwt_identity()
    # thread = threading.Thread(target=update_graph_db, args=(current_app._get_current_object(), True))
    thread = threading.Thread(target=update_graph_db, args=(current_app.app_context(), True))
    thread.start()

    return make_response(jsonify('good'), 200)


@bp.route('/status')
def status():
    current_app.logger.debug('Site status: OK')
    return make_response('Status: OK', 200)
