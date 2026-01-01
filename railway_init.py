#!/usr/bin/env python
"""
Script d'initialisation pour Railway
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')

django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import connection

def test_database_connection():
    """Tester la connexion à la base de données"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Connexion à la base de données réussie")
            return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def run_migrations():
    """Exécuter les migrations"""
    try:
        print("🔄 Exécution des migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations terminées")
        return True
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False

def create_superuser():
    """Créer un superutilisateur si nécessaire"""
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        try:
            username = os.environ.get('ADMIN_USERNAME', 'admin')
            email = os.environ.get('ADMIN_EMAIL', 'admin@cabinet.com')
            password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"✅ Superutilisateur créé: {username}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la création du superutilisateur: {e}")
            return False
    else:
        print("ℹ️ Un superutilisateur existe déjà")
        return True

def main():
    print("🚀 Initialisation Railway - Cabinet d'Avocats")
    print("=" * 50)
    
    # Test de connexion à la base de données
    if not test_database_connection():
        sys.exit(1)
    
    # Exécution des migrations
    if not run_migrations():
        sys.exit(1)
    
    # Création du superutilisateur
    create_superuser()
    
    print("✅ Initialisation terminée avec succès!")

if __name__ == '__main__':
    main()