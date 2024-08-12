from flask import Flask, render_template, request
from models import db, Trip  # Importation de db et Trip depuis models.py
from datetime import datetime

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy avec l'application Flask
db.init_app(app)

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
