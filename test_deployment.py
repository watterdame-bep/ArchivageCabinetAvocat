#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration de déploiement
"""

import os
import sys
import django
from pathlib import Path

def test_settings():
    """Test des settings de production"""
    print("🔍 Test des settings de production...")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    django.setup()
    
    from django.conf import settings
    
    # Tests de base
    assert not settings.DEBUG, "DEBUG doit être False en production"
    assert 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE, "WhiteNoise middleware manquant"
    assert settings.STATIC_URL == '/static/', "STATIC_URL incorrect"
    assert str(settings.STATIC_ROOT).endswith('staticfiles'), "STATIC_ROOT incorrect"
    
    print("✅ Settings de production OK")

def test_static_files():
    """Test de la collecte des fichiers statiques"""
    print("🔍 Test des fichiers statiques...")
    
    from django.core.management import execute_from_command_line
    
    # Collecter les fichiers statiques
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--settings=CabinetAvocat.settings_production'])
    
    # Vérifier les fichiers critiques
    staticfiles_dir = Path('staticfiles')
    critical_files = [
        'css/vendors_css.css',
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'assets/vendor_components/select2/dist/css/select2.min.css'
    ]
    
    for file_path in critical_files:
        full_path = staticfiles_dir / file_path
        assert full_path.exists(), f"Fichier critique manquant: {file_path}"
    
    print("✅ Fichiers statiques OK")

def test_jsreport_config():
    """Test de la configuration JSReport"""
    print("🔍 Test de la configuration JSReport...")
    
    from django.conf import settings
    
    assert hasattr(settings, 'JSREPORT_CONFIG'), "Configuration JSReport manquante"
    assert 'templates' in settings.JSREPORT_CONFIG, "Templates JSReport manquants"
    
    # Vérifier les templates essentiels
    templates = settings.JSREPORT_CONFIG['templates']
    essential_templates = ['rapport_agent', 'rapport_client', 'rapport_dossier']
    
    for template in essential_templates:
        assert template in templates, f"Template JSReport manquant: {template}"
    
    print("✅ Configuration JSReport OK")

def main():
    """Fonction principale"""
    print("🚀 Test de la configuration de déploiement Railway")
    print("=" * 50)
    
    try:
        test_settings()
        test_static_files()
        test_jsreport_config()
        
        print("=" * 50)
        print("✅ Tous les tests passés ! Configuration prête pour Railway")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()