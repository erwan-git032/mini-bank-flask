# Étape 1 : choisir l'image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port que Flask utilise
EXPOSE 5000

# Définir la commande pour lancer l'application
CMD ["python", "app.py"]
