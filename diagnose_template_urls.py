#!/usr/bin/env python3
"""
Diagnostic des URLs hardcodées dans les templates
"""

import os
import re
from pathlib import Path

def find_hardcoded_static_urls():
    """Trouve tous les URLs /static/ hardcodés dans les templates"""
    print("🔍 Recherche des URLs /static/ hardcodées dans les templates\n")
    
    template_dirs = [
        'templates',
        'Authentification/templates',
        'Administrateur/templates', 
        'Agent/templates',
        'Dossier/templates',
        'Structure/templates',
        'parametre/templates',
        'paiement/templates',
        'rapport/templates'
    ]
    
    hardcoded_files = []
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for html_file in Path(template_dir).rglob('*.html'):
                try:
                    content = html_file.read_text(encoding='utf-8')
                    
                    # Chercher les URLs hardcodées
                    patterns = [
                        r'href=["\']\/static\/',
                        r'src=["\']\/static\/',
                        r'url\(["\']\/static\/',
                        r'@import ["\']\/static\/'
                    ]
                    
                    found_issues = []
                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            found_issues.extend(matches)
                    
                    if found_issues:
                        hardcoded_files.append({
                            'file': str(html_file),
                            'issues': found_issues,
                            'count': len(found_issues)
                        })
                        
                except Exception as e:
                    print(f"⚠️ Erreur lecture {html_file}: {e}")
    
    return hardcoded_files

def find_missing_static_tags():
    """Trouve les templates qui n'ont pas {% load static %}"""
    print("🔍 Recherche des templates sans {% load static %}\n")
    
    template_dirs = ['templates']
    missing_static_load = []
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for html_file in Path(template_dir).rglob('*.html'):
                try:
                    content = html_file.read_text(encoding='utf-8')
                    
                    # Vérifier si le template utilise des assets mais n'a pas {% load static %}
                    has_static_usage = bool(re.search(r'(href|src)=["\'][^"\']*\.(css|js|png|jpg|gif)', content))
                    has_static_load = '{% load static %}' in content or '{%load static%}' in content
                    
                    if has_static_usage and not has_static_load:
                        missing_static_load.append(str(html_file))
                        
                except Exception as e:
                    print(f"⚠️ Erreur lecture {html_file}: {e}")
    
    return missing_static_load

def check_staticfiles_dirs_config():
    """Vérifie la configuration STATICFILES_DIRS"""
    print("🔧 Vérification de la configuration STATICFILES_DIRS\n")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
        import django
        django.setup()
        from django.conf import settings
        
        print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"STATIC_URL: {settings.STATIC_URL}")
        
        # Vérifier si les dossiers existent
        for static_dir in settings.STATICFILES_DIRS:
            if os.path.exists(static_dir):
                print(f"✅ {static_dir} existe")
                # Compter les fichiers
                file_count = sum(1 for _ in Path(static_dir).rglob('*') if _.is_file())
                print(f"   📊 {file_count} fichiers trouvés")
            else:
                print(f"❌ {static_dir} n'existe pas")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Diagnostic des URLs de templates\n")
    
    # 1. Chercher les URLs hardcodées
    hardcoded = find_hardcoded_static_urls()
    
    print("📋 URLS HARDCODÉES TROUVÉES:")
    if hardcoded:
        for item in hardcoded:
            print(f"  ❌ {item['file']} ({item['count']} problèmes)")
            for issue in item['issues'][:3]:  # Montrer max 3 exemples
                print(f"     {issue}")
    else:
        print("  ✅ Aucune URL hardcodée trouvée")
    
    # 2. Chercher les templates sans {% load static %}
    missing_load = find_missing_static_tags()
    
    print(f"\n📋 TEMPLATES SANS {{% load static %}}:")
    if missing_load:
        for template in missing_load:
            print(f"  ⚠️ {template}")
    else:
        print("  ✅ Tous les templates ont {% load static %}")
    
    # 3. Vérifier la configuration
    print(f"\n📋 CONFIGURATION:")
    config_ok = check_staticfiles_dirs_config()
    
    # 4. Résumé et recommandations
    print("\n" + "="*60)
    print("📋 RÉSUMÉ ET RECOMMANDATIONS")
    print("="*60)
    
    if hardcoded:
        print("\n🚨 PROBLÈMES CRITIQUES DÉTECTÉS:")
        print("  1. URLs /static/ hardcodées dans les templates")
        print("  2. Ces URLs ne fonctionnent pas avec WhiteNoise en production")
        
        print("\n💡 SOLUTIONS:")
        print("  1. Remplacer href='/static/...' par href=\"{% static '...' %}\"")
        print("  2. Ajouter {% load static %} en haut des templates")
        print("  3. Redéployer après corrections")
    
    if not config_ok:
        print("\n🚨 PROBLÈME DE CONFIGURATION:")
        print("  - settings_production.py non accessible")
        print("  - Railway n'utilise peut-être pas les bons settings")
    
    if not hardcoded and config_ok:
        print("\n✅ CONFIGURATION CORRECTE")
        print("  - Pas d'URLs hardcodées détectées")
        print("  - Configuration Django OK")
        print("  - Le problème vient probablement d'ailleurs")

if __name__ == "__main__":
    main()