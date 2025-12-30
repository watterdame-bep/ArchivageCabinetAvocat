#!/usr/bin/env python3
"""
Script pour corriger vendors_css.css avec des chemins absoluts Django
"""

import os
import re
from pathlib import Path

def fix_vendors_css():
    """Corrige vendors_css.css pour utiliser des chemins absoluts Django"""
    print("🔧 Correction de vendors_css.css pour Railway...")
    
    vendors_css_path = Path('static/css/vendors_css.css')
    if not vendors_css_path.exists():
        print(f"❌ Fichier non trouvé: {vendors_css_path}")
        return False
    
    # Lire le contenu actuel
    with open(vendors_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 Fichier original: {len(content)} caractères")
    
    # Remplacer les @import relatifs par des chemins absoluts
    # Pattern: @import url(../assets/...) → @import url(/static/assets/...)
    pattern = r'@import url\(\.\./assets/'
    replacement = '@import url(/static/assets/'
    
    new_content = re.sub(pattern, replacement, content)
    
    # Compter les remplacements
    import_count = len(re.findall(pattern, content))
    print(f"🔄 {import_count} imports relatifs trouvés")
    
    if import_count > 0:
        # Sauvegarder l'original
        backup_path = vendors_css_path.with_suffix('.css.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Sauvegarde créée: {backup_path}")
        
        # Écrire le nouveau contenu
        with open(vendors_css_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {import_count} imports corrigés vers des chemins absolus")
        
        # Afficher quelques exemples
        print("\n📋 Exemples de corrections:")
        lines = new_content.split('\n')
        for i, line in enumerate(lines[:10]):
            if '@import url(/static/assets/' in line:
                print(f"  {line.strip()}")
        
        return True
    else:
        print("ℹ️ Aucun import relatif trouvé à corriger")
        return True

def verify_correction():
    """Vérifie que la correction a bien été appliquée"""
    print("\n🔍 Vérification de la correction...")
    
    vendors_css_path = Path('static/css/vendors_css.css')
    if not vendors_css_path.exists():
        print("❌ Fichier vendors_css.css non trouvé")
        return False
    
    with open(vendors_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier qu'il n'y a plus d'imports relatifs
    relative_imports = re.findall(r'@import url\(\.\./assets/', content)
    absolute_imports = re.findall(r'@import url\(/static/assets/', content)
    
    print(f"  📊 Imports relatifs restants: {len(relative_imports)}")
    print(f"  📊 Imports absolus: {len(absolute_imports)}")
    
    if len(relative_imports) == 0 and len(absolute_imports) > 0:
        print("  ✅ Correction réussie - tous les imports sont absolus")
        return True
    else:
        print("  ❌ Correction incomplète")
        return False

def test_collectstatic():
    """Teste collectstatic après la correction"""
    print("\n📁 Test collectstatic après correction...")
    
    import subprocess
    import sys
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear',
            '--settings=CabinetAvocat.settings_production'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ collectstatic réussi après correction")
            
            # Compter les fichiers
            lines = result.stdout.split('\n')
            for line in lines:
                if 'static files copied' in line:
                    print(f"  📊 {line.strip()}")
            
            return True
        else:
            print(f"❌ Erreur collectstatic: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test collectstatic: {e}")
        return False

def create_deployment_summary():
    """Crée un résumé pour le déploiement"""
    print("\n" + "="*60)
    print("📋 RÉSUMÉ - CORRECTION VENDORS_CSS POUR RAILWAY")
    print("="*60)
    
    print("\n✅ CORRECTION APPLIQUÉE:")
    print("  🔧 vendors_css.css: Chemins relatifs → Chemins absolus")
    print("  🔧 @import url(../assets/...) → @import url(/static/assets/...)")
    print("  🔧 Compatible avec WhiteNoise sur Railway")
    
    print("\n🚀 DÉPLOIEMENT:")
    print("  git add static/css/vendors_css.css")
    print("  git commit -m 'Fix vendors_css.css with absolute paths for Railway WhiteNoise'")
    print("  git push origin main")
    
    print("\n🧪 RÉSULTAT ATTENDU SUR RAILWAY:")
    print("  ✅ Plus d'erreurs 404 pour les fichiers CSS")
    print("  ✅ Design Bootstrap complet")
    print("  ✅ Tous les composants CSS chargés")
    
    print("\n📊 LOGS RAILWAY ATTENDUS:")
    print("  ✅ 'X static files copied to /app/staticfiles'")
    print("  ✅ 'Starting gunicorn on port 8080'")
    print("  ❌ Plus de 'Not Found: /static/assets/vendor_components/...'")

def main():
    """Fonction principale"""
    print("🚀 Correction de vendors_css.css pour Railway\n")
    
    steps = [
        ("Correction des imports", fix_vendors_css),
        ("Vérification", verify_correction),
        ("Test collectstatic", test_collectstatic),
    ]
    
    all_success = True
    for name, func in steps:
        print(f"\n{'='*20} {name} {'='*20}")
        if not func():
            all_success = False
    
    # Résumé final
    create_deployment_summary()
    
    if all_success:
        print("\n🎉 SUCCÈS: vendors_css.css corrigé pour Railway!")
        print("✅ Prêt pour le déploiement")
    else:
        print("\n❌ ÉCHEC: Certaines corrections ont échoué")
    
    return all_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)