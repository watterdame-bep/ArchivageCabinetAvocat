#!/bin/bash

echo "🚀 Démarrage de l'application Cabinet d'Avocats"

# Collecter les fichiers statiques (ignorer les erreurs)
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=CabinetAvocat.settings_railway --clear || echo "⚠️ Erreur lors de la collecte des fichiers statiques (ignorée)"

# Démarrer Gunicorn sur le port Railway dynamique
echo "🌐 Démarrage du serveur Gunicorn sur le port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --env DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_railway CabinetAvocat.wsgi:application