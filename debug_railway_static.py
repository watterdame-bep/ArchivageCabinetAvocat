#!/usr/bin/env python3
"""
Script de debug pour analyser les problèmes de fichiers statiques sur Railway
"""

import os
import sys
from pathlib import Path

def analyze_static_structure():
    """Analyse la structure des fichiers statiques"""
    print("🔍 Analyse de la structure des fichiers statiques\n")
    
    # Vérifier la configuration
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    import django
    django.setup()
    from django.conf import settings
    
    print("📋 Configuration Django:")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    
    # Vérifier les fichiers problématiques
    static_root = Path(settings.STATIC_ROOT)
    problematic_files = [
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'assets/vendor_components/select2/dist/css/select2.min.css',
        'assets/vendor_components/OwlCarousel2/dist/assets/owl.carousel.css',
        'css/vendors_css.css',
        'css/style.css'
    ]
    
    print(f"\n📁 Vérification des fichiers dans {static_root}:")
    for file_path in problematic_files:
        full_path = static_root / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_path} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_path} MANQUANT")
    
    # Vérifier le contenu de vendors_css.css
    vendors_css = static_root / 'css/vendors_css.css'
    if vendors_css.exists():
        print(f"\n📄 Contenu de vendors_css.css (premières lignes):")
        with open(vendors_css, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            for i, line in enumerate(lines, 1):
                print(f"  {i:2d}: {line.rstrip()}")
    
    # Vérifier les URLs générées par Django
    print(f"\n🔗 URLs générées par Django:")
    from django.templatetags.static import static
    
    test_files = [
        'css/vendors_css.css',
        'css/style.css',
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css'
    ]
    
    for file_path in test_files:
        try:
            url = static(file_path)
            print(f"  {file_path} → {url}")
        except Exception as e:
            print(f"  {file_path} → ERREUR: {e}")

def test_whitenoise_serving():
    """Teste le serving WhiteNoise"""
    print("\n🌐 Test du serving WhiteNoise:")
    
    try:
        from django.test import Client
        client = Client()
        
        # Tester des URLs statiques directes
        test_urls = [
            '/static/css/style.css',
            '/static/css/vendors_css.css',
            '/static/assets/vendor_components/bootstrap/dist/css/bootstrap.css'
        ]
        
        for url in test_urls:
            try:
                response = client.get(url)
                print(f"  {url} → Status: {response.status_code}")
                if response.status_code == 200:
                    print(f"    Content-Type: {response.get('Content-Type', 'Unknown')}")
                    print(f"    Size: {len(response.content):,} bytes")
                elif response.status_code == 404:
                    print(f"    ❌ Fichier non trouvé par WhiteNoise")
            except Exception as e:
                print(f"  {url} → ERREUR: {e}")
                
    except Exception as e:
        print(f"  ❌ Erreur lors du test WhiteNoise: {e}")

def check_media_configuration():
    """Vérifie la configuration des médias"""
    print("\n📷 Configuration des médias:")
    
    try:
        from django.conf import settings
        print(f"  MEDIA_URL: {settings.MEDIA_URL}")
        print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        # Vérifier si le dossier media existe
        media_root = Path(settings.MEDIA_ROOT)
        if media_root.exists():
            file_count = sum(1 for _ in media_root.rglob('*') if _.is_file())
            print(f"  📁 {file_count} fichiers dans MEDIA_ROOT")
        else:
            print(f"  ❌ MEDIA_ROOT n'existe pas: {media_root}")
            
    except Exception as e:
        print(f"  ❌ Erreur configuration média: {e}")

def main():
    """Fonction principale"""
    print("🚀 Debug des fichiers statiques Railway\n")
    
    try:
        analyze_static_structure()
        test_whitenoise_serving()
        check_media_configuration()
        
        print("\n💡 Recommandations:")
        print("  1. Vérifier que tous les fichiers existent dans staticfiles/")
        print("  2. Tester les URLs directes sur Railway")
        print("  3. Vérifier les logs WhiteNoise sur Railway")
        print("  4. Configurer un stockage externe pour /media")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()