from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_migrate import Migrate

from models import db, Trip, User  # Importation de db, Trip et User depuis models.py
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

    


if __name__ == '__main__':        
    app.run(debug=True)
