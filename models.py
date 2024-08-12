from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialise l'extension SQLAlchemy (db est une instance de SQLAlchemy)
db = SQLAlchemy()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure_date = db.Column(db.DateTime, nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    departure_location = db.Column(db.String(255), nullable=False)
    arrival_location = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # Le poids disponible en kg

    def __repr__(self):
        return f'<Trip from {self.departure_location} to {self.arrival_location}>'
