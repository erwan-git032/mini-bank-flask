import random
import string
import re

# Génération d'un identifiant utilisateur unique
# Format : USR-XXXXXX (6 caractères alphanumériques)
def generate_user_id():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"USR-{suffix}"


# Génération d'un numéro de compte bancaire unique
# Format : TGXX XXXX XXXX XXXX XXXX XXXX XXX (23 chiffres espacés + code pays TG + 2 chiffres de contrôle)
def generate_account_number():
    country_code = "TG"
    check_digits = ''.join(random.choices(string.digits, k=2))
    account_digits = ''.join(random.choices(string.digits, k=23))
    # On formate les chiffres par groupes de 4 pour la lisibilité
    formatted = ' '.join([account_digits[i:i+4] for i in range(0, len(account_digits), 4)])
    return f"{country_code}{check_digits}{formatted}"


# Génération d'un identifiant unique pour les transactions
# Format : TRX-XXXXXX (6 caractères alphanumériques)
def generate_transaction_id():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"TRX-{suffix}"


# Validation d'un mot de passe sécurisé
# Doit contenir : min 12 caractères, au moins une majuscule, une minuscule, un chiffre et un caractère spécial
def is_valid_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@?!%*&!$-_])[A-Za-z\d@$!%*?&-_]{12,}$'
    return re.match(pattern, password)


# Validation d'une adresse email
# Vérifie que le format est correct (exemple : exemple@domaine.com)
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


# Validation d'un nom ou prénom
# Accepte les lettres, espaces et tirets (supporte les caractères accentués)
def is_valid_name(name):
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s-]+$'
    return re.match(pattern, name) is not None
