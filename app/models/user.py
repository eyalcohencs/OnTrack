from datetime import datetime

from flask_login import UserMixin

from app.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
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
