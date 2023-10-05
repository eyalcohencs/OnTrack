import re
from datetime import timedelta
from enum import Enum

from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import login_user, logout_user, login_required
import bcrypt

from app import login_manager, db
from app.authentication import bp
from app.models.user import User
from app.user.logic import get_current_user_details

# TODO - a good improvement is to break down the monolithic app to microservices and
#  Authentication service should be one of them


class AuthenticationResponseCode(Enum):
    SUCCEED = 'succeed'
    USERNAME_ALREADY_EXIST = 'username_already_exists'
    USERNAME_INVALID = 'invalid_username'
    PASSWORD_INVALID = 'invalid_password'
    EMAIL_ALREADY_EXIST = 'email_already_exist'
    EMAIL_INVALID = 'invalid_email'
    FIRST_LAST_NAME_TOO_SHORT = 'first_last_name_too_short'


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate username
    username = data["username"]
    try:
        existed_user = User.query.filter_by(username=username).first()
        if existed_user:
            return make_response(jsonify(
                {'is_created': False, 'auth_response_code': AuthenticationResponseCode.USERNAME_ALREADY_EXIST.value,
                 'error': None}), 403)
    except Exception as e:
        return make_response(jsonify(
            {'is_created': False, 'auth_response_code': AuthenticationResponseCode.USERNAME_ALREADY_EXIST.value, 'error': e}), 403)

    if len(username) < 4 or not re.match(r"^[a-zA-Z]+$", username):
        return make_response(jsonify(
            {'is_created': False, 'auth_response_code': AuthenticationResponseCode.USERNAME_INVALID.value, 'error': None}), 403)

    # Validate password
    password = data['password']
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{4,}$"
    if not re.match(pattern, password):
        return make_response(jsonify(
            {'is_created': False, 'auth_response_code': AuthenticationResponseCode.PASSWORD_INVALID.value, 'error': None}), 403)

    # Validate email
    email = data['email']
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        return make_response(jsonify(
            {'is_created': False, 'auth_response_code': AuthenticationResponseCode.EMAIL_INVALID.value, 'error': None}), 403)
    try:
        User.query.filter_by(email=email).first()
    except Exception as e:
        return make_response(jsonify(
            {'is_created': False, 'auth_response_code': AuthenticationResponseCode.EMAIL_ALREADY_EXIST.value, 'error': e}), 403)

    # Validate name
    first_name = data["first_name"],
    last_name = data["last_name"]
    if len(first_name) < 1 or len(last_name) < 1:
        return make_response(jsonify(
            {'is_created': False, 'auth_response_code': AuthenticationResponseCode.FIRST_LAST_NAME_TOO_SHORT.value, 'error': None}), 403)

    # Create new user
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password=password,
    )
    db.session.add(user)
    db.session.commit()

    return make_response(jsonify({'is_created': True, 'auth_response_code': AuthenticationResponseCode.SUCCEED.value}), 201)


@bp.route('/login', methods=['POST'])
def login():
    # Get user credentials
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate user
    user = User.query.filter_by(username=username).first()
    if user is None:
        return make_response({'name': 'LOGIN_FAILED', 'message': 'Invalid username or password'}, 403)

    # Validate password
    is_same_password = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    if not is_same_password:
        return make_response({'name': 'LOGIN_FAILED', 'message': 'Invalid username or password'}, 403)

    # Create session token
    access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))

    # Mark user as logged in
    # login_user(user)  # todo - is it necessary?

    # Serialize data
    serialized_data = jsonify({'username': user.username, 'token': access_token, 'user': user.to_dict()})

    return make_response(serialized_data, 200)


@bp.route("/logout", methods=['POST'])
# @login_required
@jwt_required()
def logout():
    logout_user()
    return make_response(jsonify({'is_logged_out': True}), 200)


@login_manager.request_loader
def loader_request(client_request):
    if 'username' in client_request.cookies:
        username = client_request.cookies['username']
        return User.query.filter_by(username=username).first()
    return None


@bp.route("/get_user_details", methods=['GET'])
# @login_required
@jwt_required()
def get_user_details():
    user = get_current_user_details()
    return make_response(jsonify(user.to_dict()), 200)
