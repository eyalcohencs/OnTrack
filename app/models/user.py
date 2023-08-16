from datetime import datetime
from enum import Enum

from flask_login import UserMixin

from app.extensions import db


class UserTypeEnum(Enum):
    SYSTEM = 'system'
    REGULAR = 'regular'
    INACTIVE = 'inactive'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    user_type = db.Column(db.Enum(UserTypeEnum,
                                  values_callable=lambda x: [str(e.value) for e in UserTypeEnum]
                                  ),
                          nullable=False,
                          default=UserTypeEnum.REGULAR)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'id: {self.id}, username: {self.username}, name: {self.first_name} {self.last_name}'

    def to_dict(self):
        return {'id': self.id,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                }
