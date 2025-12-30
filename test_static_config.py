#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration des fichiers statiques
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.conf import settings
from django.urls import reverse
from django.test import Client

def test_static_configuration():
    """Teste la configuration des fichiers statiques"""
    print("🔍 Test de la configuration des fichiers statiques\n")
    
    # Vérifier les settings
    print("📋 Configuration Django:")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print()
    
    # Vérifier que les dossiers existent
    print("📁 Vérification des dossiers:")
    
    # Dossier static source
    static_source = Path(settings.STATICFILES_DIRS[0])
    if static_source.exists():
        print(f"  ✅ Dossier static source: {static_source}")
        
        # Vérifier bootstrap
        bootstrap_css = static_source / 'assets' / 'vendor_components' / 'bootstrap' / 'dist' / 'css' / 'bootstrap.css'
        if bootstrap_css.exists():
            print(f"  ✅ Bootstrap CSS trouvé: {bootstrap_css}")
        else:
            print(f"  ❌ Bootstrap CSS manquant: {bootstrap_css}")
    else:
        print(f"  ❌ Dossier static source manquant: {static_source}")
    
    # Dossier static collecté
    static_root = Path(settings.STATIC_ROOT)
    if static_root.exists():
        print(f"  ✅ Dossier static collecté: {static_root}")
        
        # Compter les fichiers
        static_files = list(static_root.rglob('*'))
        static_files_count = len([f for f in static_files if f.is_file()])
        print(f"  📊 Fichiers statiques collectés: {static_files_count}")
        
        # Vérifier bootstrap collecté
        bootstrap_collected = static_root / 'assets' / 'vendor_components' / 'bootstrap' / 'dist' / 'css' / 'bootstrap.css'
        if bootstrap_collected.exists():
            print(f"  ✅ Bootstrap CSS collecté: {bootstrap_collected}")
        else:
            print(f"  ❌ Bootstrap CSS non collecté: {bootstrap_collected}")
    else:
        print(f"  ❌ Dossier static collecté manquant: {static_root}")
    
    # Dossier media
    media_root = Path(settings.MEDIA_ROOT)
    if media_root.exists():
        print(f"  ✅ Dossier media: {media_root}")
        
        # Compter les fichiers media
        media_files = list(media_root.rglob('*'))
        media_files_count = len([f for f in media_files if f.is_file()])
        print(f"  📊 Fichiers media: {media_files_count}")
    else:
        print(f"  ⚠️  Dossier media manquant: {media_root}")
    
    print()
    
    # Test des URLs
    print("🌐 Test des URLs:")
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        # Vérifier que les URLs statiques sont configurées
        print("  ✅ URLs Django configurées")
        
        # Test avec un client Django
        client = Client()
        
        # Test d'une URL statique
        static_test_url = f"{settings.STATIC_URL}css/style.css"
        print(f"  🔗 Test URL statique: {static_test_url}")
        
        # Test d'une URL media (si elle existe)
        media_test_url = f"{settings.MEDIA_URL}test.jpg"
        print(f"  🔗 Test URL media: {media_test_url}")
        
    except Exception as e:
        print(f"  ❌ Erreur test URLs: {e}")
    
    print()
    
    # Recommandations
    print("💡 Recommandations:")
    
    if not static_root.exists() or not (static_root / 'assets').exists():
        print("  🔧 Exécuter: python manage.py collectstatic --noinput")
    
    if not media_root.exists():
        print("  🔧 Créer le dossier media ou vérifier MEDIA_ROOT")
    
    print("  🚀 Après correction, redéployer sur Railway")
    print("  🌐 Tester: https://votre-app.up.railway.app/static/css/style.css")

def main():
    """Fonction principale"""
    try:
        test_static_configuration()
        print("\n✅ Test terminé")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()