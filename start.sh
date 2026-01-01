#!/bin/bash
set -e  # Arrêter en cas d'erreur

echo "🚀 Démarrage de l'application Cabinet d'Avocats"

# Test spécifique MySQL Railway
echo "🧪 Test de connexion MySQL Railway..."
python test_mysql_railway.py || echo "⚠️ Problème de connexion MySQL détecté"

echo "🔍 Variables d'environnement:"
echo "PORT: $PORT"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

# Vérifier que les variables critiques sont définies
if [ -z "$PORT" ]; then
    echo "❌ Variable PORT non définie, utilisation du port 8000 par défaut"
    export PORT=8000
fi

if [ -z "$SECRET_KEY" ]; then
    echo "❌ Variable SECRET_KEY non définie!"
    exit 1
fi

# Exécuter les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate --settings=CabinetAvocat.settings_railway || echo "⚠️ Erreur lors des migrations (ignorée)"

# Collecter les fichiers statiques avec plus de verbosité
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear --verbosity=2 --settings=CabinetAvocat.settings_railway || echo "⚠️ Erreur lors de la collecte des fichiers statiques (ignorée)"

# Corriger les fichiers statiques manquants
echo "🔧 Diagnostic et correction des fichiers statiques..."
python fix_static_files.py || echo "⚠️ Erreur lors de la correction des fichiers statiques"

# Créer les CSS manquants avec CDN comme fallback
echo "🎨 Création des CSS manquants avec CDN..."
python create_bootstrap_cdn.py || echo "⚠️ Erreur lors de la création des CSS CDN"

# Debug des fichiers statiques
echo "🔍 Debug final des fichiers statiques..."
python debug_static.py || echo "⚠️ Erreur lors du debug des fichiers statiques"

# Test de la configuration Django
echo "🧪 Test de la configuration Django..."
python manage.py check --settings=CabinetAvocat.settings_railway || echo "⚠️ Problème de configuration Django"

# Démarrer Gunicorn sur le port Railway dynamique
echo "🌐 Démarrage du serveur Gunicorn sur le port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 2 --log-level info --access-logfile - --error-logfile - --env DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_railway CabinetAvocat.wsgi:application