from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from utils.security import generate_user_id, generate_account_number, generate_transaction_id, is_valid_email, is_valid_password, is_valid_name
import datetime
import json
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000 
app.secret_key = 'msk'

# Définition du chemin vers la base SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'Bank.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

with app.app_context():
    db.create_all()


#Route de la page d'acceuil
@app.route('/')
def home():
    return render_template('index.html')


# Route pour rechercher une transaction précise
@app.route('/search_transaction')
def search_transaction():
    user_id = session.get('user_id')
    if not user_id:
        return {"found": False}

    transaction_id = request.args.get('id')
    transaction = Transaction.query.filter_by(account_id=user_id, transaction_id=transaction_id).first()

    if transaction:
        return {
            "found": True,
            "transaction": {
                "type": transaction.type,
                "amount": transaction.amount,
                "recipient": transaction.recipient,
                "date": transaction.date.strftime('%Y-%m-%d %H:%M')
            }
        }
    return {"found": False}


# Route de connexion
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pin = request.form['pin']

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email inconnu. Veuillez vous inscrire !", "danger")
            return redirect(url_for('register'))
        
        if not check_password_hash(user.password, password):
            flash("Mot de passe incorrect.", "danger")
            return redirect(url_for('login'))
        
        if not check_password_hash(user.pin, pin):
            flash("Code PIN incorrect.", "danger")
            return redirect(url_for('login'))

        # Connexion réussie → stockage de l'ID utilisateur dans la session
        session['user_id'] = user.id
        flash(f"Bienvenue {user.first_name} !", "success")
        return redirect(url_for('dashboard'))

    return render_template('login.html')


# Route pour la création d'un nouvel utilisateur
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        # Récupère les pays depuis le fichier JSON
        with open('data/countries.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        return render_template('register.html', countries=countries)
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        pin = request.form['pin']
        confirm_pin = request.form['confirm_pin']
        nationality = request.form['nationality']
        phone = request.form['phone']

        # Vérification des contraintes
        if not is_valid_name(first_name):
            flash("Le nom ne doit contenir que des lettres, espaces ou tirets.", "danger")
            return redirect(url_for('register'))
        
        if not is_valid_name(last_name):
            flash("Le prénom ne doit contenir que des lettres, espaces ou tirets.")
            return redirect(url_for('register'))

        if not is_valid_email(email):
            flash("Adresse email invalide.", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for('register'))

        if not is_valid_password(password):
            flash("Le mot de passe doit contenir au moins 12 caractères, avec une majuscule, une minuscule, un chiffre et un caractère spécial.", "danger")
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Le mots de passe ne sont pas identiques ! Réessayez !", "danger")
            return redirect(url_for('register'))
        
        if pin != confirm_pin:
            flash("Les codes PIN ne sont pas indentiques !")
            return redirect(url_for('register'))

        # Hashage du mot de passe et du PIN
        hashed_password = generate_password_hash(password)
        hashed_pin = generate_password_hash(pin)

        # Création du nouvel utilisateur
        new_user = User(
            user_id = generate_user_id(),
            account_number = generate_account_number(),
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = hashed_password,
            pin = hashed_pin,
            nationality = nationality,
            phone = phone,
            balance = 0.0
        )

        db.session.add(new_user)
        db.session.commit()

        # Création de la session utilisateur
        session['user_id'] = new_user.id
        flash("Compte créé avec succès !", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')


# Route du tableau de bord
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Veuillez vous connecter d'abord !", "warning")
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    transactions = Transaction.query.filter_by(account_id=user.id).order_by(Transaction.date.desc()).all()
    return render_template('dashboard.html', user=user, transactions=transactions)


# Page de virement
@app.route('/transfer_page')
def transfer_page():
    if 'user_id' not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for('login'))
    return render_template('transfer.html')


# Page de paiement de facture
@app.route('/pay_bill_page')
def pay_bill_page():
    if 'user_id' not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for('login'))
    return render_template('pay_bill.html')


# Commencer un virement
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user_id' not in session:
        flash("Veuillez vous connecter !", "warning")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        amount = request.form.get('amount')
        recipient_account = request.form.get('recipient_account')

        if not amount or not recipient_account:
            flash("Veuillez remplir tous les champs.", "danger")
            return redirect(url_for('transfer'))
        
        try:
            amount = float(amount)
        except ValueError:
            flash("Montant invalide.", "danger")
            return redirect(url_for('transfer'))

        recipient = User.query.filter_by(account_number=recipient_account).first()

        if not recipient:
            flash("Compte destinataire introuvable.", "danger")
            return redirect(url_for('transfer'))

        if amount > user.balance:
            flash("Solde insuffisant.", "danger")
            return redirect(url_for('dashboard'))

        if amount <= 0:
            flash("Le montant doit être supérieur à zéro.", "danger")
            return redirect(url_for('dashboard'))
        
        session['pending_transfer'] = {
            'amount': amount,
            'recipient_account': recipient_account,
            'recipient_name': recipient.first_name + " " + recipient.last_name
        }
        
        return redirect(url_for('confirm_transfer'))
    
    return render_template("transfer.html")


# Confirmation de virement
@app.route('/confirm_transfer', methods=['GET', 'POST'])
def confirm_transfer():
    if 'user_id' not in session:
        flash("Veuillez vous connecter !", "warning")
        return redirect(url_for('login'))
    
    pending = session.get('pending_transfer')
    if not pending:
        flash("Aucune opération à confirmer !", "danger")
        return redirect(url_for('dashboard'))

    if 'pin_attempts' not in session:
        session['pin_attempts'] = 0
    
    if request.method == 'POST':
        action = request.form['action']

        if action == 'cancel':
            session.pop('pending_transfer', None)
            session.pop('pin_attempts', None)
            flash("Transaction annulée")
            return redirect(url_for('dashboard'))
        
        elif action == 'confirm':
            entered_pin = request.form['pin']
            user = User.query.get(session['user_id'])

            if not check_password_hash(user.pin, entered_pin):
                session['pin_attempts'] += 1
                remaining = 3 - session['pin_attempts']

                if remaining <= 0:
                    session.pop('pending_transfer', None)
                    session.pop('pin_attempts', None)
                    flash("Nombre de tentatives dépassé. Transaction annulée.", "danger")
                    return redirect(url_for('dashboard'))
                else:
                    flash(f"PIN incorrect. Il vous reste {remaining} tentative(s).", "danger")
                    return redirect(url_for('confirm_transfer'))
            
            session.pop('pin_attempts', None)
            recipient = User.query.filter_by(account_number=pending['recipient_account']).first()

            amount = float(pending['amount'])
            user.balance -= amount
            recipient.balance += amount

            trx = Transaction(
                transaction_id=generate_transaction_id(),
                account_id=user.id,
                type="Virement",
                amount=amount,
                date=datetime.datetime.now(),
                recipient=recipient.account_number
            )

            db.session.add(trx)
            db.session.commit()

            session.pop('pending_transfer', None)
            session.pop('pin_attempts', None)

            flash(f"Virement de {amount} € effectué vers {pending['recipient_name']} {recipient.last_name}.", "success")
            return redirect(url_for('dashboard'))
    
    return render_template('confirm_transfer.html', pending=pending)


# Commencer un paiement de facture
@app.route('/pay_bill', methods=['GET', 'POST'])
def pay_bill():
    if 'user_id' not in session:
        flash("Veuillez vous connecter !", "warning")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    amount = float(request.form['amount'])
    recipient = request.form['recipient']

    if amount <= 0:
        flash("Le montant doit être supérieur à zéro.", "danger")
        return redirect(url_for('deposit_page'))

    if amount > user.balance:
        flash("Solde insuffisant !", "danger")
        return redirect(url_for('dashboard'))
    
    session['pending_pay_bill'] = {
        'amount': amount,
        'recipient': recipient
    }

    return redirect(url_for('confirm_pay_bill'))


# Confirmation paiement de facture
@app.route('/confirm_pay_bill', methods=['GET', 'POST'])
def confirm_pay_bill():
    if 'user_id' not in session:
        flash("Veuillez vous connecter !", "warning")
        return redirect(url_for('login'))
    
    pending = session.get('pending_pay_bill')
    if not pending:
        flash("Aucune opération à confirmer !", "danger")
        return redirect(url_for('dashboard'))
    
    if 'pin_attempts' not in session:
        session['pin_attempts'] = 0
    
    if request.method == "POST":
        action = request.form['action']

        if action == 'cancel':
            session.pop('pending_pay_bill', None)
            session.pop('pin_attempts', None)
            flash("Transaction annulée")
            return redirect(url_for('dashboard'))
        
        if action == 'confirm':
            entered_pin = request.form['pin']
            user = User.query.get(session['user_id'])

            if not check_password_hash(user.pin, entered_pin):
                session['pin_attempts'] += 1
                remaining = 3 - session['pin_attempts']

                if remaining <= 0:
                    session.pop('pending_pay_bill', None)
                    session.pop('pin_attempts', None)
                    flash("Nombre de tentatives dépassé. Transaction annulée.", "danger")
                    return redirect(url_for('dashboard')) 
                else:
                    flash(f"PIN incorrect. Il vous reste {remaining} tentative(s).", "danger")
                    return redirect(url_for('confirm_pay_bill'))
            
            session.pop('pin_attempts', None)
            recipient = pending['recipient']
            amount = float(pending['amount'])
            user.balance -= amount

            trx = Transaction(
                transaction_id=generate_transaction_id(),
                account_id=user.id,
                type="Facture",
                amount=amount,
                date=datetime.datetime.now(),
                recipient=recipient
            )

            db.session.add(trx)
            db.session.commit()
            flash(f"Paiement de {amount} FCFA à {recipient} effectué avec succès !", "success")
            return redirect(url_for('dashboard'))
    return render_template('confirm_pay_bill.html', pending=pending)


# Page de dépôt
@app.route('/deposit_page')
def deposit_page():
    if 'user_id' not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for('login'))
    return render_template('deposit.html')


# Effectuer un dépôt
@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        flash("Veuillez vous connecter !", "warning")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    try:
        amount = float(request.form['amount'])
    except ValueError:
        flash("Montant invalide !", "danger")
        return redirect(url_for('deposit_page'))

    if amount <= 0:
        flash("Le montant doit être supérieur à zéro.", "danger")
        return redirect(url_for('deposit_page'))

    user.balance += amount

    trx = Transaction(
        transaction_id=generate_transaction_id(),
        account_id=user.id,
        type="Dépôt",
        amount=amount,
        date=datetime.datetime.now(),
        recipient=None
    )

    db.session.add(trx)
    db.session.commit()
    flash(f"Dépôt de {amount} FCFA effectué avec succès !", "success")
    return redirect(url_for('dashboard'))


# Déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for('login'))


# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
