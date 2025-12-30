#!/usr/bin/env python3
"""
Script pour corriger les URLs dans vendors_css.css
Remplace les URLs absolues par des URLs relatives pour Railway
"""

import os
import re

def fix_vendors_css():
    """Corrige les URLs dans vendors_css.css"""
    css_file = 'static/css/vendors_css.css'
    
    if not os.path.exists(css_file):
        print(f"❌ Fichier non trouvé: {css_file}")
        return False
    
    print(f"🔧 Correction des URLs dans {css_file}...")
    
    # Lire le fichier
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les URLs absolues
    absolute_urls = re.findall(r'@import url\(/static/', content)
    print(f"📊 URLs absolues trouvées: {len(absolute_urls)}")
    
    # Remplacer les URLs absolues par des URLs relatives
    # /static/assets/... → ../assets/...
    content = re.sub(
        r'@import url\(/static/assets/',
        '@import url(../assets/',
        content
    )
    
    # Vérifier les changements
    relative_urls = re.findall(r'@import url\(\.\./assets/', content)
    print(f"📊 URLs relatives créées: {len(relative_urls)}")
    
    # Sauvegarder le fichier corrigé
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fichier corrigé: {css_file}")
    return True

def main():
    """Fonction principale"""
    print("🚀 Correction des URLs CSS pour Railway")
    
    if fix_vendors_css():
        print("✅ Correction terminée avec succès!")
        print("📋 Les fichiers CSS devraient maintenant se charger correctement sur Railway")
    else:
        print("❌ Erreur lors de la correction")

if __name__ == "__main__":
    main()