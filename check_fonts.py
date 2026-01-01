#!/usr/bin/env python
"""
Vérifier les fonts et icônes disponibles
"""
from pathlib import Path
import os

def check_fonts():
    """Vérifier les fonts disponibles"""
    print("🔤 Vérification des fonts...")
    
    staticfiles_path = Path('/app/staticfiles')
    
    # Chemins des fonts à vérifier
    font_paths = [
        'assets/icons/font-awesome/fonts/',
        'assets/icons/material-design-iconic-font/fonts/',
        'assets/icons/Ionicons/fonts/',
        'assets/icons/feather-icons/',
    ]
    
    for font_path in font_paths:
        full_path = staticfiles_path / font_path
        if full_path.exists():
            fonts = list(full_path.glob('*'))
            print(f"✅ {font_path}: {len(fonts)} fichiers")
            for font in fonts[:3]:  # Afficher les 3 premiers
                print(f"   - {font.name}")
        else:
            print(f"❌ {font_path}: MANQUANT")

def check_css_files():
    """Vérifier les fichiers CSS critiques"""
    print("\n🎨 Vérification des CSS critiques...")
    
    staticfiles_path = Path('/app/staticfiles')
    
    css_files = [
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'assets/icons/font-awesome/css/font-awesome.css',
        'assets/icons/material-design-iconic-font/css/materialdesignicons.css',
        'assets/icons/Ionicons/css/ionicons.css',
        'css/style.css',
        'css/vendors_css.css',
    ]
    
    for css_file in css_files:
        full_path = staticfiles_path / css_file
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {css_file}: {size} bytes")
        else:
            print(f"❌ {css_file}: MANQUANT")

def main():
    print("🔍 Vérification des fonts et CSS")
    print("=" * 40)
    
    check_fonts()
    check_css_files()

if __name__ == '__main__':
    main()