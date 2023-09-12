from flask import Blueprint


bp = Blueprint('track', __name__, url_prefix='/api')
from app.track import views
