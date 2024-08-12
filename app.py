from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from modeles import Trip

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure_date = db.Column(db.DateTime, nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    departure_location = db.Column(db.String(255), nullable=False)
    arrival_location = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # Le poids disponible en kg

    def __repr__(self):
        return f'<Trip from {self.departure_location} to {self.arrival_location}>'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_travel', methods=['POST'])
def ajouter_voyage():
    # Récupérer les données du formulaire
    departure = request.form.get('departure')
    arrival = request.form.get('arrival')

    departure_date = request.form.get('departure-date')
    departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
    arrival_date = request.form.get('arrival-date')
    arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()

    weight = float(request.form['weight'])

    # Créer un nouvel objet Trip
    trip = Trip(departure_location=departure, arrival_location=arrival, departure_date=departure_date, arrival_date=arrival_date, weight=weight)

    # Ajouter l'objet à la base de données
    db.session.add(trip)
    db.session.commit()

    # Traiter les données
    print(departure, arrival, departure_date, arrival_date, weight)

    trips = Trip.query.all()  # Récupère tous les voyages de la base de données
    return render_template('trips.html', trips=trips)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
        
    app.run(debug=True)