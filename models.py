from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialise l'extension SQLAlchemy (db est une instance de SQLAlchemy)
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    departure_location = db.Column(db.String(255), nullable=False)
    arrival_location = db.Column(db.String(255), nullable=False)
    available_weight = db.Column(db.Float, nullable=False)  # Le poids disponible en kg

    def __repr__(self):
        return f'<Trip from {self.departure_location} to {self.arrival_location}>'
