# Utiliser Python 3.11 comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système minimales
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput --settings=CabinetAvocat.settings_railway

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--env", "DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_railway", "CabinetAvocat.wsgi:application"]