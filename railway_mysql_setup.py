#!/usr/bin/env python
"""
Script pour configurer la connexion MySQL Railway
"""
import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire du projet au path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def test_mysql_connection():
    """Tester la connexion MySQL"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Connexion MySQL réussie!")
            print(f"📊 Version MySQL: {version[0]}")
            
            # Afficher les informations de connexion
            db_settings = settings.DATABASES['default']
            print(f"🏠 Host: {db_settings.get('HOST', 'localhost')}")
            print(f"🔌 Port: {db_settings.get('PORT', '3306')}")
            print(f"🗄️ Database: {db_settings.get('NAME', 'N/A')}")
            print(f"👤 User: {db_settings.get('USER', 'N/A')}")
            
            return True
    except Exception as e:
        print(f"❌ Erreur de connexion MySQL: {e}")
        return False

def show_railway_variables():
    """Afficher les variables d'environnement Railway"""
    print("\n🔧 Variables d'environnement Railway:")
    railway_vars = [
        'MYSQLHOST',
        'MYSQLPORT', 
        'MYSQLUSERNAME',
        'MYSQLPASSWORD',
        'MYSQLDATABASE',
        'SECRET_KEY',
        'DEBUG',
        'RAILWAY_STATIC_URL',
        'RAILWAY_GIT_COMMIT_SHA',
        'PORT'
    ]
    
    for var in railway_vars:
        value = os.environ.get(var, 'Non définie')
        if 'PASSWORD' in var or 'SECRET' in var:
            if value != 'Non définie':
                value = '*' * len(value)  # Masquer les mots de passe
        print(f"  {var}: {value}")

if __name__ == '__main__':
    print("🚀 Configuration MySQL Railway - Cabinet d'Avocats")
    print("=" * 50)
    
    # Afficher les variables d'environnement
    show_railway_variables()
    
    print("\n🔍 Test de connexion MySQL...")
    if test_mysql_connection():
        print("\n✅ Configuration MySQL Railway réussie!")
        
        # Exécuter les migrations si demandé
        if len(sys.argv) > 1 and sys.argv[1] == '--migrate':
            print("\n📦 Exécution des migrations...")
            execute_from_command_line(['manage.py', 'migrate'])
            
        # Créer un superutilisateur si demandé
        if len(sys.argv) > 1 and sys.argv[1] == '--setup':
            print("\n👤 Configuration initiale...")
            execute_from_command_line(['manage.py', 'setup_production', '--create-superuser', '--setup-cabinet'])
    else:
        print("\n❌ Échec de la configuration MySQL")
        sys.exit(1)