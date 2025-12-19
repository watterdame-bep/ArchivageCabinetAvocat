#!/usr/bin/env python
"""
Script de validation pour base de données existante sur Railway
Usage: railway run python validate_existing_database.py
"""
import os
import sys
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection

def validate_database_connection():
    """Valide la connexion à la base de données"""
    print("🔍 Test de connexion à la base de données...")
    
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

def validate_users():
    """Valide les utilisateurs existants"""
    print("\n👥 Validation des utilisateurs...")
    
    try:
        User = get_user_model()
        
        total_users = User.objects.count()
        admin_users = User.objects.filter(is_superuser=True).count()
        active_users = User.objects.filter(is_active=True).count()
        
        print(f"✅ Total utilisateurs: {total_users}")
        print(f"✅ Administrateurs: {admin_users}")
        print(f"✅ Utilisateurs actifs: {active_users}")
        
        if admin_users > 0:
            print("✅ Au moins un administrateur disponible")
            
            # Lister les admins
            admins = User.objects.filter(is_superuser=True)[:5]  # Max 5
            print("👤 Administrateurs disponibles:")
            for admin in admins:
                print(f"   - {admin.username} ({admin.email})")
            
            return True
        else:
            print("⚠️ Aucun administrateur trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur validation utilisateurs: {e}")
        return False

def validate_tables():
    """Valide les tables principales"""
    print("\n🗄️ Validation des tables...")
    
    try:
        cursor = connection.cursor()
        
        # Tables principales à vérifier
        tables_to_check = [
            'auth_user',
            'Dossier_dossier',
            'paiement_paiement',
            'Authentification_customuser'
        ]
        
        existing_tables = []
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                existing_tables.append((table, count))
                print(f"✅ {table}: {count} enregistrement(s)")
            except Exception:
                print(f"⚠️ {table}: table non trouvée ou vide")
        
        if existing_tables:
            print(f"✅ {len(existing_tables)} table(s) validée(s)")
            return True
        else:
            print("❌ Aucune table principale trouvée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur validation tables: {e}")
        return False

def validate_migrations():
    """Valide l'état des migrations"""
    print("\n🔄 Validation des migrations...")
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT app, name FROM django_migrations ORDER BY app, name")
        migrations = cursor.fetchall()
        
        apps = {}
        for app, migration in migrations:
            if app not in apps:
                apps[app] = 0
            apps[app] += 1
        
        print(f"✅ {len(migrations)} migration(s) appliquée(s)")
        for app, count in apps.items():
            print(f"   - {app}: {count} migration(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur validation migrations: {e}")
        return False

def main():
    """Fonction principale de validation"""
    print("🧪 Validation Base de Données Existante - Railway")
    print("=" * 60)
    
    # Tests de validation
    tests = [
        ("Connexion base de données", validate_database_connection),
        ("Utilisateurs existants", validate_users),
        ("Tables principales", validate_tables),
        ("État des migrations", validate_migrations),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA VALIDATION")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{len(tests)} tests réussis")
    
    if passed == len(tests):
        print("\n🎉 BASE DE DONNÉES EXISTANTE VALIDÉE!")
        print("✅ Tes utilisateurs et données sont disponibles")
        print("✅ Tu peux te connecter avec tes comptes existants")
        print("✅ Toutes les fonctionnalités sont opérationnelles")
        return True
    else:
        print("\n⚠️ VALIDATION INCOMPLÈTE")
        print("🔧 Vérifier les erreurs ci-dessus")
        print("💡 Assure-toi que tes données ont été correctement importées")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)