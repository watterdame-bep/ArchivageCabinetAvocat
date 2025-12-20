#!/usr/bin/env python3
"""
Script pour forcer la création des tables sur Railway MySQL
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Forcer l'utilisation des settings de production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')

# Initialiser Django
django.setup()

from django.db import connection
from django.core.management.commands.migrate import Command as MigrateCommand

def check_database_connection():
    """Vérifier la connexion à la base"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Connexion MySQL OK")
            return True
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False

def list_tables():
    """Lister les tables existantes"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Tables existantes ({len(tables)}):")
            for table in tables:
                print(f"  - {table[0]}")
            return [table[0] for table in tables]
    except Exception as e:
        print(f"❌ Erreur listage tables: {e}")
        return []

def force_migrations():
    """Forcer l'exécution des migrations"""
    print("\n🔄 Exécution des migrations forcées...")
    
    # 1. Créer les tables de migration Django
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    # 2. Marquer toutes les migrations comme appliquées
    execute_from_command_line(['manage.py', 'migrate', '--fake-initial'])
    
    # 3. Appliquer les vraies migrations
    execute_from_command_line(['manage.py', 'migrate'])

def create_superuser():
    """Créer un superutilisateur si nécessaire"""
    from django.contrib.auth.models import User
    
    try:
        if not User.objects.filter(is_superuser=True).exists():
            print("\n👤 Création d'un superutilisateur...")
            User.objects.create_superuser(
                username='admin',
                email='admin@cabinet.com',
                password='admin123'  # À changer !
            )
            print("✅ Superutilisateur créé: admin/admin123")
        else:
            print("✅ Superutilisateur existe déjà")
    except Exception as e:
        print(f"❌ Erreur création superuser: {e}")

if __name__ == '__main__':
    print("🚀 Script de migration forcée Railway MySQL")
    print("=" * 50)
    
    # Vérifications
    if not check_database_connection():
        sys.exit(1)
    
    # État initial
    print("\n📊 État initial de la base:")
    initial_tables = list_tables()
    
    # Migrations forcées
    try:
        force_migrations()
        print("\n✅ Migrations terminées avec succès")
        
        # État final
        print("\n📊 État final de la base:")
        final_tables = list_tables()
        
        new_tables = set(final_tables) - set(initial_tables)
        if new_tables:
            print(f"\n🆕 Nouvelles tables créées ({len(new_tables)}):")
            for table in sorted(new_tables):
                print(f"  + {table}")
        
        # Créer superuser
        create_superuser()
        
        print("\n🎉 Migration Railway terminée avec succès !")
        print("🔗 Vous pouvez maintenant vous connecter à l'application")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant les migrations: {e}")
        sys.exit(1)