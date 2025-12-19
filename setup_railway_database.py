#!/usr/bin/env python
"""
Script de setup initial pour Railway
Crée les tables et un superutilisateur si nécessaire
"""
import os
import sys
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import connection

def check_database():
    """Vérifie la connexion à la base de données"""
    print("🔍 Vérification de la connexion à la base de données...")
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            print("✅ Connexion à la base de données réussie")
            return True
        else:
            print("❌ Test de connexion échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def run_migrations():
    """Exécute les migrations"""
    print("📊 Exécution des migrations...")
    
    try:
        # Créer les migrations si nécessaire
        print("🔧 Création des migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', '--noinput'])
        
        # Appliquer les migrations
        print("🔄 Application des migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput', '--run-syncdb'])
        
        print("✅ Migrations appliquées avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False

def check_tables():
    """Vérifie que les tables principales existent"""
    print("🗄️ Vérification des tables...")
    
    try:
        cursor = connection.cursor()
        
        # Vérifier quelques tables critiques
        tables_to_check = [
            'auth_user',
            'django_migrations',
        ]
        
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✅ {table}: {count} enregistrement(s)")
            except Exception as e:
                print(f"❌ {table}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification tables: {e}")
        return False

def create_superuser_if_needed():
    """Crée un superutilisateur si aucun n'existe"""
    print("👤 Vérification des utilisateurs...")
    
    try:
        User = get_user_model()
        
        user_count = User.objects.count()
        admin_count = User.objects.filter(is_superuser=True).count()
        
        print(f"📊 Utilisateurs existants: {user_count}")
        print(f"📊 Administrateurs: {admin_count}")
        
        if admin_count == 0:
            print("🔧 Création d'un superutilisateur par défaut...")
            User.objects.create_superuser(
                username='admin',
                email='admin@cabinet.com',
                password='Admin123!'
            )
            print("✅ Superutilisateur créé: admin / Admin123!")
            print("⚠️ Changez le mot de passe après la première connexion!")
        else:
            print("✅ Administrateur(s) déjà existant(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur gestion utilisateurs: {e}")
        return False

def main():
    """Fonction principale de setup"""
    print("🚀 Setup Initial Railway - Cabinet Avocat")
    print("=" * 60)
    
    # Étapes de setup
    steps = [
        ("Connexion base de données", check_database),
        ("Migrations Django", run_migrations),
        ("Vérification tables", check_tables),
        ("Gestion utilisateurs", create_superuser_if_needed),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 Étape: {step_name}")
        print("-" * 40)
        
        if not step_func():
            print(f"\n❌ Échec à l'étape: {step_name}")
            return False
    
    print("\n" + "=" * 60)
    print("🎉 SETUP RAILWAY TERMINÉ AVEC SUCCÈS!")
    print("=" * 60)
    print("✅ Base de données initialisée")
    print("✅ Tables créées")
    print("✅ Utilisateurs configurés")
    print("✅ Application prête à fonctionner")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)