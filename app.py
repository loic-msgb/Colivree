from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_migrate import Migrate

from models import db, Trip, User, Booking  # Importation de db, Trip et User depuis models.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='mysecretkey'
# Initialisation de l'extension SQLAlchemy avec l'application Flask
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Vérifier si l'utilisateur ou l'email existe déjà
        user = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user:
            flash('Ce nom d\'utilisateur est déjà pris.')
            return redirect(url_for('signup'))

        if email_exists:
            flash('Cet email est déjà utilisé.')
            return redirect(url_for('signup'))

        # Ajouter un nouvel utilisateur
        new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')  # Le nom ou l'email peut être saisi
        password = request.form.get('password')

        # Rechercher l'utilisateur soit par email, soit par nom d'utilisateur
        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

        # Vérifier les informations d'identification
        if not user or not check_password_hash(user.password, password):
            flash('Veuillez vérifier vos identifiants et réessayer.')
            return redirect(url_for('login'))

        # Stocker les informations de session
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

from flask import render_template, session, redirect, url_for

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté

    user = User.query.get(session['user_id'])  # Récupérer l'utilisateur connecté à partir de la session
    return render_template('profile.html', user=user)



@app.route('/add_trip', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        departure_date = request.form.get('departure_date')
        arrival_date = request.form.get('arrival_date')
        available_weight = request.form.get('available_weight')

        # Crée un nouvel objet Trip et ajoute-le à la base de données
        new_trip = Trip(
            departure_location=departure,
            arrival_location=arrival,
            departure_date=datetime.strptime(departure_date, '%Y-%m-%d'),
            arrival_date=datetime.strptime(arrival_date, '%Y-%m-%d'),
            available_weight=float(available_weight),
            user_id=session['user_id']  # Assurez-vous que l'utilisateur est connecté
        )
        db.session.add(new_trip)
        db.session.commit()

        flash('Voyage ajouté avec succès!')
        return redirect(url_for('index'))
    else:
        # Vérifier si l'utilisateur est connecté
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour ajouter un voyage.')
            return redirect(url_for('login'))
        return render_template('add_trip.html')    

@app.route('/see_trips', methods=['GET'] )
def see_trips():
    trips = Trip.query.all()
    return render_template('see_trips.html', trips=trips)

@app.route('/book_trip/<int:trip_id>', methods=['GET', 'POST'])
def book_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if request.method == 'POST':
        weight = request.form.get('weight')

        # Vérifier si le poids réservé est supérieur au poids disponible
        if float(weight) > trip.available_weight:
            flash('Le poids réservé est supérieur au poids disponible.')
            return redirect(url_for('book_trip', trip_id=trip_id))

        # Crée un nouvel objet Booking et ajoute-le à la base de données
        new_booking = Booking(
            weight=float(weight),
            user_id=session['user_id'],
            trip_id=trip_id
        )
        db.session.add(new_booking)
        db.session.commit()

        # Mettre à jour le poids disponible
        trip.available_weight -= float(weight)
        db.session.commit()

        flash('Réservation effectuée avec succès!')
        return redirect(url_for('index'))
    else:
        return render_template('see_trips.html', trip=trip)


if __name__ == '__main__':        
    app.run(debug=True)
