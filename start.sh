#!/bin/bash

# Script de démarrage pour Railway

echo "🚀 Démarrage de l'application Cabinet Avocat..."

# Vérifier les variables d'environnement critiques
if [ -z "$MYSQL_HOST" ]; then
    echo "⚠️  Variable MYSQL_HOST non définie"
fi

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données..."
python manage.py check --database default

# Exécuter les migrations
echo "📊 Exécution des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superutilisateur si nécessaire (optionnel)
echo "👤 Vérification du superutilisateur..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Création du superutilisateur admin...')
    User.objects.create_superuser('admin', 'admin@cabinet.com', 'admin123')
    print('Superutilisateur créé: admin/admin123')
else:
    print('Superutilisateur déjà existant')
"

echo "✅ Application prête à démarrer!"

# Démarrer l'application avec Gunicorn optimisé pour Railway
exec gunicorn CabinetAvocat.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile -