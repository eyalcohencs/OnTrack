from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_login import login_user, logout_user
import bcrypt

from app import login_manager, db
from app.authentication import bp
from app.models.user import User


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # check if user already logged in
    # current_user is None if not make_response(jsonify({'is_created': False}), 301)

    # exist_user =  # todo - check existed user

    validate_password = data['password']
    password = bcrypt.hashpw(validate_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        username=data["username"],
        password=password,
    )
    # todo - validate user, return {code: , 'name': 'REGISTRATION_FAILED', 'message': 'Invalid f'{errors}''
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'is_created': True}), 201)


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

    # TODO - remove - login_manager handle the session
    # Create session token
    # secret_key = current_app.config['SECRET_KEY']
    # token = jwt.encode({'username': username}, secret_key, algorithm='HS256')
    access_token = create_access_token(identity=username)

    # Mark user as logged in
    login_user(user)

    return make_response(jsonify({'username': user.username, 'token': access_token}), 200)


@bp.route("/logout")
def logout():
    logout_user()
    return make_response(jsonify({'is_logged_out': True}), 201)


@login_manager.request_loader
def loader_request(client_request):
    if 'username' in client_request.cookies:
        username = client_request.cookies['username']
        return User.query.filter_by(username=username).first()
    return None
