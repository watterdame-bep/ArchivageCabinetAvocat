#!/bin/bash
set -e  # Arrêter en cas d'erreur

echo "🚀 Démarrage de l'application Cabinet d'Avocats"

# Test rapide de la configuration
echo "🧪 Test de configuration..."
python test_config.py || echo "⚠️ Problème de configuration détecté"

echo "🔍 Variables d'environnement:"
echo "PORT: $PORT"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "MYSQLHOST: $MYSQLHOST"
echo "MYSQLDATABASE: $MYSQLDATABASE"

# Vérifier que les variables critiques sont définies
if [ -z "$PORT" ]; then
    echo "❌ Variable PORT non définie, utilisation du port 8000 par défaut"
    export PORT=8000
fi

if [ -z "$SECRET_KEY" ]; then
    echo "❌ Variable SECRET_KEY non définie!"
    exit 1
fi

# Collecter les fichiers statiques (ignorer les erreurs)
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=CabinetAvocat.settings_railway --clear || echo "⚠️ Erreur lors de la collecte des fichiers statiques (ignorée)"

# Test de la configuration Django
echo "🧪 Test de la configuration Django..."
python manage.py check --settings=CabinetAvocat.settings_railway || echo "⚠️ Problème de configuration Django"

# Démarrer Gunicorn sur le port Railway dynamique
echo "🌐 Démarrage du serveur Gunicorn sur le port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 2 --log-level info --access-logfile - --error-logfile - --env DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_railway CabinetAvocat.wsgi:application