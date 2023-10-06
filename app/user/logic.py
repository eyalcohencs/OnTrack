from flask_jwt_extended import get_jwt_identity

from app.models.user import User, UserTypeEnum


def get_current_user_details():
    """
    The function uses jwt identity for extracting the current user.
    :return: Current user details from DB.
    """
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return user


def is_current_user_is_system_user():
    """
    Verifying user is a system user.
    """
    current_user = get_current_user_details()
    return current_user and current_user.user_type == UserTypeEnum.SYSTEM
