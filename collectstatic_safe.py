#!/usr/bin/env python
"""
Script sécurisé pour collectstatic sur Railway
Évite les problèmes de connexion MySQL pendant le build
"""
import os
import sys
import django

def safe_collectstatic():
    """Collecte les fichiers statiques sans connexion MySQL"""
    print("📦 Collection sécurisée des fichiers statiques...")
    
    # Forcer le mode collectstatic
    os.environ['RAILWAY_STATIC_BUILD'] = 'true'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
    
    # Setup Django
    django.setup()
    
    # Importer et exécuter collectstatic
    from django.core.management import execute_from_command_line
    
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Fichiers statiques collectés avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la collection des fichiers statiques: {e}")
        return False

if __name__ == "__main__":
    success = safe_collectstatic()
    sys.exit(0 if success else 1)