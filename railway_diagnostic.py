#!/usr/bin/env python
"""
Script de diagnostic complet pour Railway
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

def check_environment():
    """Vérifier les variables d'environnement"""
    print("🔍 Vérification des variables d'environnement...")
    
    required_vars = {
        'SECRET_KEY': os.environ.get('SECRET_KEY'),
        'DEBUG': os.environ.get('DEBUG'),
        'DJANGO_SETTINGS_MODULE': os.environ.get('DJANGO_SETTINGS_MODULE'),
        'MYSQLHOST': os.environ.get('MYSQLHOST'),
        'MYSQLPORT': os.environ.get('MYSQLPORT'),
        'MYSQLUSERNAME': os.environ.get('MYSQLUSERNAME'),
        'MYSQLPASSWORD': os.environ.get('MYSQLPASSWORD'),
        'MYSQLDATABASE': os.environ.get('MYSQLDATABASE'),
        'PORT': os.environ.get('PORT'),
    }
    
    missing = []
    for var, value in required_vars.items():
        if value is None:
            missing.append(var)
            print(f"❌ {var}: Non définie")
        else:
            if 'PASSWORD' in var or 'SECRET' in var:
                print(f"✅ {var}: {'*' * min(len(str(value)), 10)}")
            else:
                print(f"✅ {var}: {value}")
    
    return len(missing) == 0, missing

def check_django_setup():
    """Vérifier la configuration Django"""
    print("\n🔧 Vérification de Django...")
    
    try:
        # Configurer Django
        settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        django.setup()
        
        from django.conf import settings
        print(f"✅ Django configuré avec: {settings_module}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        return False

def check_database():
    """Vérifier la connexion à la base de données"""
    print("\n🗄️ Vérification de la base de données...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Connexion MySQL réussie")
            print(f"✅ Version MySQL: {version[0]}")
            
            cursor.execute("SELECT DATABASE()")
            database = cursor.fetchone()
            print(f"✅ Base de données: {database[0]}")
            
        return True
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def check_apps():
    """Vérifier les applications Django"""
    print("\n📱 Vérification des applications...")
    
    try:
        from django.conf import settings
        from django.apps import apps
        
        for app_name in settings.INSTALLED_APPS:
            try:
                app = apps.get_app_config(app_name.split('.')[-1])
                print(f"✅ {app_name}: OK")
            except Exception as e:
                print(f"⚠️ {app_name}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur applications: {e}")
        return False

def check_urls():
    """Vérifier les URLs"""
    print("\n🌐 Vérification des URLs...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Test du health check
        client = Client()
        response = client.get('/health/')
        print(f"✅ Health check: Status {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur URLs: {e}")
        return False

def main():
    print("🚀 Diagnostic Railway - Cabinet d'Avocats")
    print("=" * 50)
    
    checks = [
        ("Variables d'environnement", check_environment),
        ("Configuration Django", check_django_setup),
        ("Base de données", check_database),
        ("Applications Django", check_apps),
        ("URLs et routes", check_urls),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur critique dans {check_name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    
    if all(results):
        print("🎉 Tous les tests sont passés!")
        print("✅ Votre application devrait fonctionner sur Railway")
    else:
        print("❌ Certains tests ont échoué")
        print("💡 Vérifiez les erreurs ci-dessus et corrigez-les")
        
        failed_checks = [checks[i][0] for i, result in enumerate(results) if not result]
        print(f"🔍 Tests échoués: {', '.join(failed_checks)}")

if __name__ == '__main__':
    main()