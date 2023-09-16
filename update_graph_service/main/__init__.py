from flask import Blueprint


bp = Blueprint('main', __name__)

from update_graph_service.main import views
