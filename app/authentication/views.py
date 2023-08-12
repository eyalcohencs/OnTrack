from flask import request

from app.authentication import bp


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')