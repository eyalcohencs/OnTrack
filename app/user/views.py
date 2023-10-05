from flask import make_response
from flask_jwt_extended import jwt_required
from app.user import bp
from app.models.user import User
from app.user.logic import is_current_user_is_system_user


@bp.route('/get_all_users', methods=['GET'])
@jwt_required()
def get_all_users():
    if is_current_user_is_system_user:
        users = User.query.all()
        users_jsons = [user.to_dict() for user in users]
        return make_response(users_jsons, 200)
    else:
        return make_response('Only system users has access', 403)
