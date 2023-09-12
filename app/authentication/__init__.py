from flask import Blueprint


bp = Blueprint('authentication', __name__, url_prefix='/api')
from app.authentication import views
