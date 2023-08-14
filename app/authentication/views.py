from flask import request, redirect, jsonify, make_response
from flask_login import login_user, logout_user

from app import login_manager, db
from app.authentication import bp
from app.models.user import User


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # exist_user =  # todo - check existed user

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        username=data["username"],
        password=data["password"],
    )
    # todo - validate user, return {code: , 'name': 'REGISTRATION_FAILED', 'message': 'Invalid f'{errors}''
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'is_created': True}), 201)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # TODO - move to separate function
    # TODO - use hash for password
    user = User.query.filter_by(username=username).first()
    if user.password == password:
        login_user(user)
        return make_response(user.to_dict(), 200)
    else:
        return make_response({'name': 'LOGIN_FAILED', 'message': 'Invalid username or password'}, 403)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(location='login', code=302)


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)
