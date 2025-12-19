#!/usr/bin/env python
"""
Script de fix définitif pour créer toutes les tables Django sur Railway
Usage: railway run python fix_railway_tables.py
"""
import os
import sys
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.core.management import execute_from_command_line, call_command
from django.db import connection
from django.contrib.auth import get_user_model

def check_database_connection():
    """Vérifie la connexion à la base de données"""
    print("🔍 Test de connexion à la base de données...")
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            print("✅ Connexion à la base de données réussie")
            
            # Afficher les infos de connexion
            db_settings = connection.settings_dict
            print(f"📋 Base: {db_settings['NAME']}")
            print(f"📋 Host: {db_settings['HOST']}")
            print(f"📋 User: {db_settings['USER']}")
            
            return True
        else:
            print("❌ Test de connexion échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def reset_migrations():
    """Reset et recrée toutes les migrations"""
    print("\n🔄 Reset des migrations...")
    
    try:
        # Supprimer les entrées de migration existantes
        print("🗑️ Suppression des entrées de migration...")
        cursor = connection.cursor()
        
        # Créer la table django_migrations si elle n'existe pas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS django_migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                app VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                applied DATETIME NOT NULL
            )
        """)
        
        # Vider la table des migrations
        cursor.execute("DELETE FROM django_migrations")
        print("✅ Entrées de migration supprimées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur reset migrations: {e}")
        return False

def create_all_migrations():
    """Crée toutes les migrations"""
    print("\n📝 Création de toutes les migrations...")
    
    try:
        # Créer les migrations pour toutes les apps
        apps_to_migrate = [
            'Authentification',
            'Structure', 
            'Agent',
            'Adresse',
            'Dossier',
            'paiement',
            'parametre'
        ]
        
        for app in apps_to_migrate:
            try:
                print(f"📝 Création migrations pour {app}...")
                call_command('makemigrations', app, verbosity=1, interactive=False)
            except Exception as e:
                print(f"⚠️ Erreur migration {app}: {e}")
        
        # Créer les migrations générales
        print("📝 Création migrations générales...")
        call_command('makemigrations', verbosity=1, interactive=False)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création migrations: {e}")
        return False

def apply_all_migrations():
    """Applique toutes les migrations"""
    print("\n🔄 Application de toutes les migrations...")
    
    try:
        # Appliquer les migrations avec --run-syncdb pour forcer la création
        print("🔄 Application migrations avec syncdb...")
        call_command('migrate', verbosity=2, interactive=False, run_syncdb=True)
        
        print("✅ Toutes les migrations appliquées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur application migrations: {e}")
        return False

def verify_tables():
    """Vérifie que toutes les tables sont créées"""
    print("\n🔍 Vérification des tables créées...")
    
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        print(f"📋 {len(tables)} table(s) trouvée(s):")
        for table in sorted(tables):
            print(f"   ✅ {table}")
        
        # Vérifier spécifiquement la table problématique
        expected_table = "Authentification_compteutilisateur"
        if expected_table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {expected_table}")
            count = cursor.fetchone()[0]
            print(f"\n✅ Table {expected_table}: {count} enregistrement(s)")
            return True
        else:
            print(f"\n❌ Table {expected_table} toujours manquante")
            return False
            
    except Exception as e:
        print(f"❌ Erreur vérification tables: {e}")
        return False

def create_superuser():
    """Crée un superutilisateur"""
    print("\n👤 Création du superutilisateur...")
    
    try:
        User = get_user_model()
        
        # Vérifier si des utilisateurs existent
        user_count = User.objects.count()
        admin_count = User.objects.filter(is_superuser=True).count()
        
        print(f"📊 Utilisateurs existants: {user_count}")
        print(f"📊 Administrateurs: {admin_count}")
        
        if admin_count == 0:
            print("🔧 Création d'un superutilisateur...")
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
        print(f"❌ Erreur création superutilisateur: {e}")
        return False

def main():
    """Fonction principale de fix"""
    print("🔧 Fix Définitif Tables Railway - Cabinet Avocat")
    print("=" * 60)
    
    # Étapes de fix
    steps = [
        ("Connexion base de données", check_database_connection),
        ("Reset des migrations", reset_migrations),
        ("Création des migrations", create_all_migrations),
        ("Application des migrations", apply_all_migrations),
        ("Vérification des tables", verify_tables),
        ("Création superutilisateur", create_superuser),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 Étape: {step_name}")
        print("-" * 40)
        
        if not step_func():
            print(f"\n❌ Échec à l'étape: {step_name}")
            print("🔧 Essayez de corriger l'erreur et relancer le script")
            return False
    
    print("\n" + "=" * 60)
    print("🎉 FIX RAILWAY TERMINÉ AVEC SUCCÈS!")
    print("=" * 60)
    print("✅ Base de données complètement initialisée")
    print("✅ Toutes les tables créées")
    print("✅ Superutilisateur disponible")
    print("✅ Application prête à fonctionner")
    print("\n🌐 Accédez à votre site: https://votre-projet.railway.app/admin")
    print("👤 Identifiants: admin / Admin123!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)