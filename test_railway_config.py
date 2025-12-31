#!/usr/bin/env python3
"""
Script pour tester la configuration Railway et diagnostiquer les problèmes
"""

import os
import sys
import django
from pathlib import Path

def setup_django():
    """Configure Django pour les tests"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    django.setup()

def test_allowed_hosts():
    """Test de la configuration ALLOWED_HOSTS"""
    print("🔍 Test ALLOWED_HOSTS...")
    
    from django.conf import settings
    
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"DEBUG: {settings.DEBUG}")
    
    # Simuler différents hosts
    test_hosts = [
        'localhost',
        '127.0.0.1',
        'test.railway.app',
        'test.up.railway.app',
        'archivagecabinetavocat-production.up.railway.app'
    ]
    
    for host in test_hosts:
        if any(
            host == allowed or 
            (allowed.startswith('.') and host.endswith(allowed[1:])) or
            allowed == '*'
            for allowed in settings.ALLOWED_HOSTS
        ):
            print(f"✅ {host} - Autorisé")
        else:
            print(f"❌ {host} - Refusé")

def test_database_config():
    """Test de la configuration base de données"""
    print("\n🔍 Test Configuration Base de Données...")
    
    from django.conf import settings
    
    db_config = settings.DATABASES['default']
    
    required_vars = ['NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']
    
    for var in required_vars:
        value = db_config.get(var)
        if value:
            if var == 'PASSWORD':
                print(f"✅ {var}: ***")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Non configuré")

def test_static_config():
    """Test de la configuration des fichiers statiques"""
    print("\n🔍 Test Configuration Fichiers Statiques...")
    
    from django.conf import settings
    
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    
    # Vérifier WhiteNoise
    if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
        print("✅ WhiteNoise middleware configuré")
    else:
        print("❌ WhiteNoise middleware manquant")

def test_jsreport_config():
    """Test de la configuration JSReport"""
    print("\n🔍 Test Configuration JSReport...")
    
    from django.conf import settings
    
    if hasattr(settings, 'JSREPORT_CONFIG'):
        config = settings.JSREPORT_CONFIG
        print(f"✅ JSREPORT_URL: {config.get('url')}")
        print(f"✅ JSREPORT_USERNAME: {config.get('username')}")
        print(f"✅ Templates: {len(config.get('templates', {}))}")
    else:
        print("❌ Configuration JSReport manquante")

def test_environment_vars():
    """Test des variables d'environnement"""
    print("\n🔍 Test Variables d'Environnement...")
    
    important_vars = [
        'DJANGO_SETTINGS_MODULE',
        'SECRET_KEY',
        'RAILWAY_ENVIRONMENT',
        'RAILWAY_PUBLIC_DOMAIN',
        'MYSQLDATABASE',
        'MYSQLHOST',
        'JSREPORT_SERVICE_URL'
    ]
    
    for var in important_vars:
        value = os.environ.get(var)
        if value:
            if 'SECRET' in var or 'PASSWORD' in var:
                print(f"✅ {var}: ***")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Non défini")

def main():
    """Fonction principale"""
    print("🚀 Test de Configuration Railway")
    print("=" * 50)
    
    try:
        setup_django()
        
        test_environment_vars()
        test_allowed_hosts()
        test_database_config()
        test_static_config()
        test_jsreport_config()
        
        print("=" * 50)
        print("✅ Tests terminés")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()