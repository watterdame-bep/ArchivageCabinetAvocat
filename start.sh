#!/bin/bash

# Script de démarrage optimisé pour Railway - Base de données existante

echo "🚀 Démarrage Cabinet Avocat - Railway Production"

# 1️⃣ Vérifier les variables d'environnement critiques
if [ -z "$MYSQLHOST" ]; then
    echo "❌ Variables MySQL manquantes - Service MySQL non connecté!"
    echo "💡 Connectez le service MySQL au service Django dans Railway Dashboard"
    exit 1
fi

# 2️⃣ Attendre que MySQL soit prêt
echo "⏳ Attente de MySQL Railway..."
python wait_for_mysql.py

if [ $? -ne 0 ]; then
    echo "❌ MySQL Railway non accessible"
    exit 1
fi

echo "✅ MySQL Railway connecté!"

# 3️⃣ Test détaillé de la connexion MySQL
echo "🔍 Step 1: Test détaillé de la connexion MySQL..."
python test_mysql_connection.py

if [ $? -ne 0 ]; then
    echo "❌ Test de connexion MySQL échoué"
    exit 1
fi

# 4️⃣ Vérifier la connexion à la base de données existante via Django
echo "🔍 Step 2: Vérification de la base de données existante via Django..."
python manage.py shell -c "
from Authentification.models import CompteUtilisateur
try:
    user_count = CompteUtilisateur.objects.count()
    admin_count = CompteUtilisateur.objects.filter(is_superuser=True).count()
    print(f'✅ Base de données connectée!')
    print(f'👥 Utilisateurs existants: {user_count}')
    print(f'👤 Administrateurs: {admin_count}')
except Exception as e:
    print(f'❌ Erreur de connexion à la base: {e}')
    exit(1)
"

# 5️⃣ Appliquer uniquement les nouvelles migrations (sans --run-syncdb)
echo "🔧 Step 3: Application des nouvelles migrations seulement..."
python manage.py migrate --noinput

# 6️⃣ Collecter les fichiers statiques
echo "📦 Step 4: Collection des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🚀 Step 5: Lancement du serveur Gunicorn..."
echo "✅ Toutes les étapes terminées - Application prête!"

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