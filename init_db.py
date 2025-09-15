from models import db, User
from utils.security import generate_user_id, generate_account_number
from werkzeug.security import generate_password_hash
import os

# Chemin vers la base de données
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'Bank.db')

# Supprime la base existante si elle existe (optionnel)
if os.path.exists(db_path):
    os.remove(db_path)

from app import app  # On importe app pour initialiser SQLAlchemy avec le contexte

with app.app_context():
    # Crée toutes les tables
    db.create_all()

    # Création de 2 utilisateurs de test
    user1 = User(
        user_id=generate_user_id(),
        account_number=generate_account_number(),
        first_name="Alice",
        last_name="Dupont",
        email="alice@test.com",
        password=generate_password_hash("Alice1234!@#$"),
        pin=generate_password_hash("1234"),
        nationality="France",
        phone="0600000001",
        balance=1000.0
    )

    user2 = User(
        user_id=generate_user_id(),
        account_number=generate_account_number(),
        first_name="Bob",
        last_name="Martin",
        email="bob@test.com",
        password=generate_password_hash("Bob1234!@#$"),
        pin=generate_password_hash("5678"),
        nationality="France",
        phone="0600000002",
        balance=500.0
    )

    # Ajout des utilisateurs à la base
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print("Base de données initialisée avec succès !")
    print("Utilisateurs de test :")
    print("1️⃣ Alice - email: alice@test.com, mot de passe: Alice1234!@#$, PIN: 1234")
    print("2️⃣ Bob   - email: bob@test.com, mot de passe: Bob1234!@#$, PIN: 5678")
