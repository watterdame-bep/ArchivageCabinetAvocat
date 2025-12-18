#!/usr/bin/env python
"""
Script de validation du déploiement Railway
Vérifie que tous les composants sont correctement configurés
"""
import os
import sys
import requests
from django.core.management.base import BaseCommand
import django
from django.conf import settings

def check_environment():
    """Vérifie les variables d'environnement"""
    print("🔍 Vérification des variables d'environnement...")
    
    required_vars = [
        'MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_DATABASE', 
        'MYSQL_USER', 'MYSQL_PASSWORD', 'SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables manquantes: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Toutes les variables d'environnement sont définies")
        return True

def check_database():
    """Vérifie la connexion à la base de données"""
    print("🔍 Vérification de la base de données...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Connexion à la base de données réussie")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def check_jsreport():
    """Vérifie la connexion à JSReport"""
    print("🔍 Vérification de JSReport...")
    
    jsreport_url = os.environ.get('JSREPORT_URL')
    if not jsreport_url:
        print("⚠️ JSREPORT_URL non définie - JSReport pas encore configuré")
        return False
    
    try:
        # Test de ping
        response = requests.get(f"{jsreport_url}/api/ping", timeout=10)
        if response.status_code == 200:
            print("✅ JSReport service accessible")
            
            # Test d'authentification
            username = os.environ.get('JSREPORT_USERNAME', 'admin')
            password = os.environ.get('JSREPORT_PASSWORD')
            
            if password:
                auth_response = requests.get(
                    f"{jsreport_url}/odata/templates",
                    auth=(username, password),
                    timeout=10
                )
                if auth_response.status_code == 200:
                    templates = auth_response.json().get('value', [])
                    print(f"✅ Authentification JSReport réussie - {len(templates)} template(s) trouvé(s)")
                    return True
                else:
                    print("❌ Erreur d'authentification JSReport")
                    return False
            else:
                print("⚠️ JSREPORT_PASSWORD non définie")
                return False
        else:
            print(f"❌ JSReport service non accessible (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion JSReport: {e}")
        return False

def check_django_config():
    """Vérifie la configuration Django"""
    print("🔍 Vérification de la configuration Django...")
    
    try:
        # Vérifier les settings
        print(f"📋 Settings module: {settings.SETTINGS_MODULE}")
        print(f"📋 Debug mode: {settings.DEBUG}")
        print(f"📋 Allowed hosts: {settings.ALLOWED_HOSTS}")
        print(f"📋 Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        # Vérifier les apps installées critiques
        critical_apps = ['Authentification', 'Dossier', 'paiement', 'rapport']
        for app in critical_apps:
            if app in settings.INSTALLED_APPS:
                print(f"✅ App {app} installée")
            else:
                print(f"❌ App {app} manquante")
                return False
        
        print("✅ Configuration Django valide")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False

def check_static_files():
    """Vérifie la configuration des fichiers statiques"""
    print("🔍 Vérification des fichiers statiques...")
    
    try:
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root and os.path.exists(static_root):
            static_files = len([f for f in os.listdir(static_root) if os.path.isfile(os.path.join(static_root, f))])
            print(f"✅ Fichiers statiques collectés: {static_files} fichiers dans {static_root}")
            return True
        else:
            print("⚠️ STATIC_ROOT non défini ou dossier inexistant")
            return False
    except Exception as e:
        print(f"❌ Erreur fichiers statiques: {e}")
        return False

def main():
    """Fonction principale de validation"""
    print("🚀 Validation du Déploiement Railway - Cabinet Avocat")
    print("=" * 60)
    
    # Configurer Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    django.setup()
    
    # Tests de validation
    tests = [
        ("Variables d'environnement", check_environment),
        ("Configuration Django", check_django_config),
        ("Base de données", check_database),
        ("Fichiers statiques", check_static_files),
        ("Service JSReport", check_jsreport),
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
        print("🎉 DÉPLOIEMENT VALIDÉ - Application prête pour la production!")
        return True
    else:
        print("⚠️ DÉPLOIEMENT INCOMPLET - Corriger les erreurs ci-dessus")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)