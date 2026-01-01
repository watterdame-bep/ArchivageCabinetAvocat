#!/usr/bin/env python
"""
Test rapide pour vérifier Bootstrap
"""
import os
from pathlib import Path

def test_bootstrap():
    """Tester la présence de Bootstrap"""
    print("🧪 Test Bootstrap Railway")
    print("=" * 30)
    
    # Chemins à vérifier
    paths_to_check = [
        '/app/static/assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        '/app/staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css',
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {path} ({size} bytes)")
        else:
            print(f"❌ {path} - MANQUANT")
    
    # Lister le contenu de staticfiles/assets
    staticfiles_assets = Path('/app/staticfiles/assets')
    if staticfiles_assets.exists():
        print(f"\n📁 Contenu de {staticfiles_assets}:")
        for item in sorted(staticfiles_assets.iterdir())[:10]:
            print(f"  {item.name}")
    else:
        print(f"\n❌ {staticfiles_assets} n'existe pas")

if __name__ == '__main__':
    test_bootstrap()