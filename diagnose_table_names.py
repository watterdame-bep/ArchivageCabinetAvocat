#!/usr/bin/env python
"""
Script de diagnostic pour vérifier les noms de tables Django vs MySQL
Usage: railway run python diagnose_table_names.py
"""
import os
import sys
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.db import connection
from django.apps import apps

def get_mysql_tables():
    """Récupère toutes les tables MySQL"""
    print("🔍 Tables MySQL existantes:")
    
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        for table in sorted(tables):
            print(f"   📋 {table}")
        
        return tables
        
    except Exception as e:
        print(f"❌ Erreur récupération tables MySQL: {e}")
        return []

def get_django_expected_tables():
    """Récupère les noms de tables attendus par Django"""
    print("\n🔍 Tables attendues par Django:")
    
    expected_tables = {}
    
    for app_config in apps.get_app_configs():
        app_name = app_config.label
        
        for model in app_config.get_models():
            table_name = model._meta.db_table
            expected_tables[f"{app_name}.{model.__name__}"] = table_name
            print(f"   📋 {app_name}.{model.__name__} → {table_name}")
    
    return expected_tables

def compare_tables():
    """Compare les tables MySQL vs Django"""
    print("\n🔍 Comparaison MySQL vs Django:")
    
    mysql_tables = get_mysql_tables()
    django_tables = get_django_expected_tables()
    
    missing_tables = []
    
    for model_name, expected_table in django_tables.items():
        if expected_table in mysql_tables:
            print(f"   ✅ {model_name} → {expected_table} (OK)")
        else:
            print(f"   ❌ {model_name} → {expected_table} (MANQUANTE)")
            missing_tables.append((model_name, expected_table))
    
    return missing_tables

def check_specific_table():
    """Vérifie spécifiquement la table CompteUtilisateur"""
    print("\n🔍 Diagnostic spécifique CompteUtilisateur:")
    
    from Authentification.models import CompteUtilisateur
    
    expected_table = CompteUtilisateur._meta.db_table
    print(f"   📋 Table attendue par Django: {expected_table}")
    
    try:
        cursor = connection.cursor()
        
        # Chercher des tables similaires
        cursor.execute("SHOW TABLES LIKE '%compte%'")
        similar_tables = [table[0] for table in cursor.fetchall()]
        
        cursor.execute("SHOW TABLES LIKE '%utilisateur%'")
        user_tables = [table[0] for table in cursor.fetchall()]
        
        cursor.execute("SHOW TABLES LIKE '%authentification%'")
        auth_tables = [table[0] for table in cursor.fetchall()]
        
        print(f"   📋 Tables avec 'compte': {similar_tables}")
        print(f"   📋 Tables avec 'utilisateur': {user_tables}")
        print(f"   📋 Tables avec 'authentification': {auth_tables}")
        
        # Test direct de la table
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {expected_table}")
            count = cursor.fetchone()[0]
            print(f"   ✅ Table {expected_table} existe avec {count} enregistrement(s)")
            return True
        except Exception as e:
            print(f"   ❌ Table {expected_table} inaccessible: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur diagnostic: {e}")
        return False

def suggest_solutions(missing_tables):
    """Suggère des solutions pour les tables manquantes"""
    print("\n💡 Solutions Suggérées:")
    
    if missing_tables:
        print("🔧 Option 1: Créer les tables manquantes")
        print("   railway run python manage.py migrate --run-syncdb")
        
        print("\n🔧 Option 2: Forcer les migrations")
        print("   railway run python manage.py makemigrations --empty Authentification")
        print("   railway run python manage.py migrate")
        
        print("\n🔧 Option 3: Reset et recréation")
        print("   railway run python manage.py flush --noinput")
        print("   railway run python setup_railway_database.py")
        
        print("\n🔧 Option 4: Vérifier les noms de tables")
        for model_name, table_name in missing_tables:
            print(f"   Vérifier si {table_name} existe sous un autre nom")
    else:
        print("✅ Toutes les tables semblent correctes")

def main():
    """Fonction principale de diagnostic"""
    print("🔍 Diagnostic Tables Django vs MySQL - Railway")
    print("=" * 60)
    
    # Tests de diagnostic
    mysql_tables = get_mysql_tables()
    django_tables = get_django_expected_tables()
    missing_tables = compare_tables()
    
    # Diagnostic spécifique
    compte_ok = check_specific_table()
    
    # Suggestions
    suggest_solutions(missing_tables)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 60)
    
    print(f"📋 Tables MySQL trouvées: {len(mysql_tables)}")
    print(f"📋 Tables Django attendues: {len(django_tables)}")
    print(f"❌ Tables manquantes: {len(missing_tables)}")
    
    if missing_tables:
        print("\n⚠️ TABLES MANQUANTES DÉTECTÉES")
        for model_name, table_name in missing_tables:
            print(f"   - {model_name} → {table_name}")
        return False
    else:
        print("\n✅ TOUTES LES TABLES SONT PRÉSENTES")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)