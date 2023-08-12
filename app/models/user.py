from datetime import datetime

from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    date_created = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'
