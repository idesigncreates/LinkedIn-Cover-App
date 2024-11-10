# app/models.py
from flask_login import UserMixin
from app import db  # Import db after it has been initialized in create_app

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
