from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Hospital(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    hospital_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Hospital('{self.username}', '{self.hospital_name}')"