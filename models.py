
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialisation de l'instance SQLAlchemy
db = SQLAlchemy()

# Modèle User (Utilisateur)
class User(db.Model):
    __tablename__ = "users"  # Nom de la table dans la base de données

    # Clé primaire auto-incrémentée
    id = db.Column(db.Integer, primary_key=True)

    # Identifiant unique généré pour l'utilisateur
    user_id = db.Column(db.String(20), unique=True, nullable=False)

    # Informations personnelles
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Informations de sécurité
    password = db.Column(db.String(200), nullable=False)  # Mot de passe hashé
    pin = db.Column(db.String(200), nullable=False)       # PIN hashé

    # Numéro de compte unique
    account_number = db.Column(db.String(34), unique=True, nullable=False)

    # Contact et nationalité
    phone = db.Column(db.String(30), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)

    # Solde du compte (par défaut 0.0)
    balance = db.Column(db.Float, default=0.0)

    # Relation avec les transactions (un utilisateur peut avoir plusieurs transactions)
    transactions = db.relationship('Transaction', backref='user', lazy=True)


# Modèle Transaction
class Transaction(db.Model):
    __tablename__ = "transactions"  # Nom de la table dans la base de données

    # Clé primaire auto-incrémentée
    id = db.Column(db.Integer, primary_key=True)

    # Identifiant unique de la transaction
    transaction_id = db.Column(db.String(20), unique=True, nullable=False)

    # Référence à l'utilisateur (clé étrangère vers users.id)
    account_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Type de transaction : Dépôt, Virement, Facture, etc.
    type = db.Column(db.String(20), nullable=False)

    # Montant de la transaction
    amount = db.Column(db.String(20), nullable=False)

    # Date et heure de la transaction (par défaut UTC actuel)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Destinataire (numéro de compte ou nom selon le type de transaction)
    recipient = db.Column(db.String(34))
