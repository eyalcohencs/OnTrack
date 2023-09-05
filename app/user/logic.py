from flask_jwt_extended import get_jwt_identity

from app.models.user import User, UserTypeEnum


def get_current_user_details():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return user


def is_current_user_is_system_user():
    current_user = get_current_user_details()
    return current_user and current_user.user_type == UserTypeEnum.SYSTEM
