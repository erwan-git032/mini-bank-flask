Voici ton README **modifié et complet**, incluant les instructions pour `init_db.py` et le scénario de test avec les utilisateurs, adapté à ta structure de projet et à ton workflow Windows/VS Code :

````markdown
# Mini Banque Flask

Application web de gestion bancaire simple et sécurisée avec Flask.  
Permet de créer un compte, se connecter, consulter solde/historique, et gérer virements, dépôts, paiements – interface responsive et propre.

## Table des matières
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Initialisation de la base de données](#initialisation-de-la-base-de-données)
- [Structure du projet](#structure-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Contribuer](#contribuer)
- [Licence](#licence)
- [Auteur](#auteur)

## Prérequis
- Python 3.11  
- Git  

## Installation

1. Cloner le projet :

```bash
git clone https://github.com/AXELATAYI/mini-banque-flask.git
cd mini-banque-flask
````

2. Créer un environnement virtuel :

```bash
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate # Linux/macOS
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Lancer l’application :

```bash
python app.py
```

Accès à l’application : [http://localhost:5000](http://localhost:5000)

## Initialisation de la base de données

Pour tester l'application facilement, un script `init_db.py` est fourni. Il permet de créer la base de données avec des utilisateurs de test.

### Étapes d'utilisation

1. Initialiser la base de données :

```bash
python init_db.py
```

> ⚠️ Attention : relancer le script peut écraser la base existante.

2. Se connecter avec les utilisateurs créés :

   * Chaque utilisateur possède un **email**, un **mot de passe** et un **code PIN**.
   * Une fois connecté, vous pourrez voir le **numéro de compte** sur le tableau de bord.

3. Scénario de test conseillé :

   * Créez un utilisateur et notez ses identifiants (email, mot de passe, PIN).
   * Déconnectez-vous et créez un deuxième compte pour pouvoir tester les virements et paiements entre comptes.
   * Le solde initial est **0**, pensez à effectuer un dépôt avant de tester les transactions.

## Structure du projet

```
.
├── app.py                  # Entrée Flask
├── models.py               # Modèles SQLAlchemy
├── init_db.py              # Script pour initialiser la base de données avec utilisateurs test
├── utils/
│   └── security.py         # Sécurité (hash mots de passe) et fonctions utiles
├── templates/              # Templates HTML
├── static/                 # CSS/JS/images
├── data/
│   └── countries.json      # Données JSON
├── requirements.txt
└── README.md
```

## Fonctionnalités

* Compte utilisateur sécurisé (email + mot de passe + PIN)
* Consultation du solde et historique des transactions
* Virements, dépôts et paiements de factures
* Interface moderne et responsive

## Technologies utilisées

* Python 3.11
* Flask
* SQLAlchemy
* Jinja2 (templates HTML)
* HTML, CSS, JS

## Auteur

Axel ATAYI
GitHub : [https://github.com/AXELATAYI](https://github.com/AXELATAYI)

```
