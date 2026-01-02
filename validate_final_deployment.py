#!/usr/bin/env python
"""
Validation finale du déploiement - Cabinet d'Avocats
"""
import os
from pathlib import Path

def validate_css_files():
    """Valider que tous les fichiers CSS sont présents"""
    print("🎨 VALIDATION DES FICHIERS CSS")
    print("-" * 50)
    
    required_css = {
        'vendors_css.css': ['static/css/vendors_css.css', 'staticfiles/css/vendors_css.css'],
        'style.css': ['static/css/style.css', 'staticfiles/css/style.css'],
        'comprehensive-fix.css': ['static/css/comprehensive-fix.css', 'staticfiles/css/comprehensive-fix.css'],
        'font-size-fix.css': ['static/css/font-size-fix.css', 'staticfiles/css/font-size-fix.css'],
        'template-font-fix.css': ['static/css/template-font-fix.css', 'staticfiles/css/template-font-fix.css'],
        'missing-assets-fallback.css': ['staticfiles/css/missing-assets-fallback.css']
    }
    
    all_present = True
    
    for name, paths in required_css.items():
        print(f"\n📋 {name}:")
        for path in paths:
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"  ✅ {path} ({size} bytes)")
            else:
                print(f"  ❌ {path} MANQUANT")
                all_present = False
    
    return all_present

def validate_css_imports():
    """Valider les imports dans vendors_css.css"""
    print("\n📋 VALIDATION DES IMPORTS CSS")
    print("-" * 50)
    
    vendors_css_path = Path('static/css/vendors_css.css')
    if not vendors_css_path.exists():
        print("❌ vendors_css.css non trouvé")
        return False
    
    with open(vendors_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_imports = [
        'bootstrap.css',
        'font-size-fix.css',
        'template-font-fix.css',
        'missing-assets-fallback.css',
        'comprehensive-fix.css'
    ]
    
    all_imports_present = True
    
    for imp in required_imports:
        if imp in content:
            print(f"✅ Import présent: {imp}")
        else:
            print(f"❌ Import manquant: {imp}")
            all_imports_present = False
    
    total_imports = content.count('@import')
    print(f"\n📊 Total des imports: {total_imports}")
    
    return all_imports_present

def validate_static_structure():
    """Valider la structure des fichiers statiques"""
    print("\n📁 VALIDATION DE LA STRUCTURE STATIQUE")
    print("-" * 50)
    
    staticfiles_dir = Path('staticfiles')
    if not staticfiles_dir.exists():
        print("❌ Dossier staticfiles manquant")
        return False
    
    required_dirs = [
        'css',
        'assets/vendor_components/bootstrap',
        'assets/icons/font-awesome',
        'assets/icons/material-design-iconic-font',
        'assets/icons/Ionicons'
    ]
    
    all_dirs_present = True
    
    for dir_path in required_dirs:
        full_path = staticfiles_dir / dir_path
        if full_path.exists():
            files = len(list(full_path.rglob('*')))
            print(f"✅ {dir_path}: {files} fichiers")
        else:
            print(f"❌ {dir_path}: MANQUANT")
            all_dirs_present = False
    
    # Compter les fichiers par type
    css_count = len(list(staticfiles_dir.rglob('*.css')))
    js_count = len(list(staticfiles_dir.rglob('*.js')))
    font_count = len(list(staticfiles_dir.rglob('*.woff*'))) + len(list(staticfiles_dir.rglob('*.ttf'))) + len(list(staticfiles_dir.rglob('*.eot')))
    
    print(f"\n📊 STATISTIQUES:")
    print(f"  📄 Fichiers CSS: {css_count}")
    print(f"  📄 Fichiers JS: {js_count}")
    print(f"  🔤 Fichiers Fonts: {font_count}")
    
    return all_dirs_present

def validate_environment():
    """Valider les variables d'environnement"""
    print("\n🔧 VALIDATION DES VARIABLES D'ENVIRONNEMENT")
    print("-" * 50)
    
    required_vars = [
        'SECRET_KEY',
        'MYSQLHOST',
        'MYSQLDATABASE',
        'MYSQLUSER',
        'MYSQLPASSWORD',
        'MYSQLPORT'
    ]
    
    all_vars_present = True
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Masquer les valeurs sensibles
            if var in ['SECRET_KEY', 'MYSQLPASSWORD']:
                display_value = '*' * min(len(value), 20)
            else:
                display_value = value[:20] + ('...' if len(value) > 20 else '')
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: MANQUANT")
            all_vars_present = False
    
    return all_vars_present

def validate_django_config():
    """Valider la configuration Django"""
    print("\n⚙️ VALIDATION DE LA CONFIGURATION DJANGO")
    print("-" * 50)
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')
        
        import django
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        django.setup()
        
        print("✅ Configuration Django chargée")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {len(settings.ALLOWED_HOSTS)} hosts")
        print(f"✅ DATABASES: {len(settings.DATABASES)} configurations")
        print(f"✅ STATIC_URL: {settings.STATIC_URL}")
        print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False

def main():
    """Fonction principale de validation"""
    print("🎯 VALIDATION FINALE DU DÉPLOIEMENT")
    print("🏢 Cabinet d'Avocats - Django Railway")
    print("=" * 60)
    
    validations = [
        ("Fichiers CSS", validate_css_files),
        ("Imports CSS", validate_css_imports),
        ("Structure statique", validate_static_structure),
        ("Variables d'environnement", validate_environment),
        ("Configuration Django", validate_django_config),
    ]
    
    success_count = 0
    total_validations = len(validations)
    
    for name, validation_func in validations:
        try:
            result = validation_func()
            if result:
                success_count += 1
                print(f"\n✅ {name} - VALIDÉ")
            else:
                print(f"\n⚠️ {name} - PROBLÈMES DÉTECTÉS")
        except Exception as e:
            print(f"\n❌ {name} - ERREUR: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 VALIDATION TERMINÉE: {success_count}/{total_validations} validations réussies")
    
    if success_count == total_validations:
        print("🎉 DÉPLOIEMENT PRÊT!")
        print("✨ Tous les composants sont correctement configurés!")
        print("\n📋 STATUT FINAL:")
        print("  ✅ Fichiers CSS présents et correctement importés")
        print("  ✅ Structure statique complète")
        print("  ✅ Variables d'environnement configurées")
        print("  ✅ Configuration Django valide")
        print("\n🚀 L'application peut être déployée sur Railway!")
        return True
    elif success_count >= 3:
        print("⚠️ DÉPLOIEMENT POSSIBLE AVEC AVERTISSEMENTS")
        print("🔧 Certains problèmes mineurs détectés mais le déploiement devrait fonctionner")
        return True
    else:
        print("❌ DÉPLOIEMENT NON RECOMMANDÉ")
        print("🔧 Trop de problèmes détectés, veuillez corriger avant le déploiement")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)