#!/bin/bash

# Script de démarrage optimisé pour Railway - Base de données existante

echo "🚀 Démarrage Cabinet Avocat - Railway Production"

# 0️⃣ Diagnostic complet de l'environnement Railway
echo "🔍 Diagnostic complet de l'environnement Railway..."
python debug_railway_env.py

if [ $? -ne 0 ]; then
    echo "❌ Problème de configuration détecté - Arrêt du déploiement"
    exit 1
fi

# 0️⃣bis Forcer la configuration production
echo "🔧 Forçage de la configuration production..."
python force_production_settings.py

if [ $? -ne 0 ]; then
    echo "❌ Impossible de forcer la configuration production"
    exit 1
fi

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

# 4️⃣ Vérifier si les tables existent, sinon les créer
echo "🔍 Step 2: Vérification de l'état de la base de données..."
python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SHOW TABLES LIKE \\'%Authentification%\\'')
        tables = cursor.fetchall()
        if not tables:
            print('⚠️ Tables manquantes - Base de données vide détectée')
            print('🔧 Exécution de la migration forcée...')
            exit(2)  # Code spécial pour migration forcée
        else:
            print(f'✅ Tables existantes trouvées: {len(tables)}')
            from Authentification.models import CompteUtilisateur
            user_count = CompteUtilisateur.objects.count()
            admin_count = CompteUtilisateur.objects.filter(is_superuser=True).count()
            print(f'👥 Utilisateurs existants: {user_count}')
            print(f'👤 Administrateurs: {admin_count}')
except Exception as e:
    print(f'❌ Erreur de vérification: {e}')
    exit(1)
"

# Vérifier le code de retour
if [ $? -eq 2 ]; then
    echo "🔧 Exécution de la migration forcée pour base vide..."
    python force_migrate_railway.py
    if [ $? -ne 0 ]; then
        echo "❌ Migration forcée échouée"
        exit 1
    fi
    echo "✅ Migration forcée terminée avec succès"
fi

# 5️⃣ Appliquer les migrations normales
echo "🔧 Step 3: Application des migrations..."
python manage.py migrate --noinput

# 6️⃣ Collecter les fichiers statiques (mode sécurisé)
echo "📦 Step 4: Collection sécurisée des fichiers statiques..."
python collectstatic_safe.py

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