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

# 3️⃣ Vérifier la connexion à la base de données existante
echo "🔍 Step 1: Vérification de la base de données existante..."
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

# 4️⃣ Appliquer uniquement les nouvelles migrations (sans --run-syncdb)
echo "🔧 Step 2: Application des nouvelles migrations seulement..."
python manage.py migrate --noinput

# 5️⃣ Collecter les fichiers statiques
echo "📦 Step 3: Collection des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🚀 Step 4: Lancement du serveur Gunicorn..."
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