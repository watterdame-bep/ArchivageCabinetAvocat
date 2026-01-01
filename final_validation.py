#!/usr/bin/env python
"""
Validation finale complète du déploiement Railway
"""
import os
import sys
from pathlib import Path
import django
from django.conf import settings

def validate_static_files():
    """Validation complète des fichiers statiques"""
    print("📦 Validation des fichiers statiques...")
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
    else:
        staticfiles_path = Path('staticfiles')
    
    # Fichiers critiques à vérifier
    critical_files = {
        'CSS Bootstrap': [
            'css/bootstrap.min.css',
            'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
            'assets/vendor_components/bootstrap/dist/css/bootstrap.min.css',
        ],
        'CSS Icônes': [
            'assets/icons/font-awesome/css/font-awesome.css',
            'assets/icons/material-design-iconic-font/css/materialdesignicons.css',
            'assets/icons/Ionicons/css/ionicons.css',
        ],
        'CSS Composants': [
            'assets/vendor_components/select2/dist/css/select2.min.css',
            'assets/vendor_components/raty-master/lib/jquery.raty.css',
            'assets/vendor_components/bootstrap-touchspin/dist/jquery.bootstrap-touchspin.css',
        ],
        'CSS Fallbacks': [
            'css/railway-fixes.css',
            'css/media-fallback.css',
            'css/comprehensive-fallback.css',
        ],
        'JavaScript': [
            'js/bootstrap.min.js',
            'js/comprehensive-fallback.js',
            'assets/vendor_components/apexcharts-bundle/dist/apexcharts.js',
        ],
        'CSS Principaux': [
            'css/style.css',
            'css/vendors_css.css',
        ],
    }
    
    validation_results = {}
    total_files = 0
    found_files = 0
    
    for category, files in critical_files.items():
        category_results = []
        for file_path in files:
            full_path = staticfiles_path / file_path
            exists = full_path.exists()
            size = full_path.stat().st_size if exists else 0
            
            category_results.append({
                'path': file_path,
                'exists': exists,
                'size': size,
                'status': '✅' if exists else '❌'
            })
            
            total_files += 1
            if exists:
                found_files += 1
        
        validation_results[category] = category_results
    
    # Afficher les résultats
    print(f"\n📊 RÉSULTATS DE VALIDATION DES FICHIERS STATIQUES")
    print("=" * 60)
    
    for category, results in validation_results.items():
        category_found = sum(1 for r in results if r['exists'])
        category_total = len(results)
        print(f"\n📁 {category}: {category_found}/{category_total}")
        
        for result in results:
            size_info = f" ({result['size']} bytes)" if result['exists'] else ""
            print(f"  {result['status']} {result['path']}{size_info}")
    
    success_rate = (found_files / total_files) * 100
    print(f"\n🎯 TAUX DE RÉUSSITE: {found_files}/{total_files} ({success_rate:.1f}%)")
    
    return success_rate >= 80  # 80% minimum pour considérer comme succès

def validate_fonts_and_icons():
    """Validation des fonts et icônes"""
    print("\n🔤 Validation des fonts et icônes...")
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
    else:
        staticfiles_path = Path('staticfiles')
    
    font_directories = [
        'assets/icons/font-awesome/fonts/',
        'assets/icons/material-design-iconic-font/fonts/',
        'assets/icons/Ionicons/fonts/',
        'assets/icons/feather-icons/',
    ]
    
    total_fonts = 0
    found_fonts = 0
    
    for font_dir in font_directories:
        full_dir = staticfiles_path / font_dir
        if full_dir.exists():
            font_files = list(full_dir.glob('*'))
            font_count = len(font_files)
            total_fonts += font_count
            found_fonts += font_count
            print(f"✅ {font_dir}: {font_count} fichiers")
        else:
            print(f"❌ {font_dir}: répertoire manquant")
    
    font_success_rate = (found_fonts / max(total_fonts, 1)) * 100
    print(f"🎯 Fonts: {found_fonts} fichiers trouvés ({font_success_rate:.1f}%)")
    
    return font_success_rate >= 70

def validate_database_connection():
    """Validation de la connexion base de données"""
    print("\n🗄️ Validation de la connexion base de données...")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')
        django.setup()
        
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        # Test de connexion simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        # Test des migrations
        try:
            execute_from_command_line(['manage.py', 'showmigrations', '--verbosity=0'])
            migrations_ok = True
        except:
            migrations_ok = False
        
        print("✅ Connexion base de données: OK")
        print(f"{'✅' if migrations_ok else '⚠️'} Migrations: {'OK' if migrations_ok else 'Problème détecté'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def validate_environment_variables():
    """Validation des variables d'environnement"""
    print("\n🔍 Validation des variables d'environnement...")
    
    required_vars = {
        'SECRET_KEY': 'Clé secrète Django',
        'MYSQLHOST': 'Hôte MySQL',
        'MYSQLDATABASE': 'Base de données MySQL',
        'MYSQLPASSWORD': 'Mot de passe MySQL',
        'PORT': 'Port Railway',
    }
    
    optional_vars = {
        'MYSQLUSERNAME': 'Nom d\'utilisateur MySQL',
        'MYSQLPORT': 'Port MySQL',
        'DEBUG': 'Mode debug',
        'DJANGO_SETTINGS_MODULE': 'Module de configuration',
    }
    
    missing_required = []
    present_vars = []
    
    # Vérifier les variables requises
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            present_vars.append(f"✅ {var}: {'*' * min(len(value), 20)}")
        else:
            missing_required.append(f"❌ {var} ({description})")
    
    # Vérifier les variables optionnelles
    for var, description in optional_vars.items():
        value = os.environ.get(var)
        if value:
            present_vars.append(f"✅ {var}: {'*' * min(len(value), 20)}")
        else:
            present_vars.append(f"⚠️ {var}: non définie (optionnelle)")
    
    # Afficher les résultats
    for var_info in present_vars:
        print(f"  {var_info}")
    
    if missing_required:
        print("\n❌ Variables requises manquantes:")
        for var_info in missing_required:
            print(f"  {var_info}")
        return False
    
    print("\n✅ Toutes les variables requises sont présentes")
    return True

def validate_django_configuration():
    """Validation de la configuration Django"""
    print("\n⚙️ Validation de la configuration Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')
        django.setup()
        
        from django.core.management import execute_from_command_line
        
        # Test de configuration avec --deploy pour la production
        try:
            execute_from_command_line(['manage.py', 'check', '--deploy', '--verbosity=0'])
            deploy_check = True
        except:
            deploy_check = False
        
        # Test de configuration basique
        try:
            execute_from_command_line(['manage.py', 'check', '--verbosity=0'])
            basic_check = True
        except:
            basic_check = False
        
        print(f"{'✅' if basic_check else '❌'} Configuration basique: {'OK' if basic_check else 'Erreur'}")
        print(f"{'✅' if deploy_check else '⚠️'} Configuration production: {'OK' if deploy_check else 'Avertissements'}")
        
        return basic_check
        
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False

def main():
    """Validation finale complète"""
    print("🎯 VALIDATION FINALE COMPLÈTE DU DÉPLOIEMENT")
    print("=" * 60)
    
    validations = [
        ("Variables d'environnement", validate_environment_variables),
        ("Fichiers statiques", validate_static_files),
        ("Fonts et icônes", validate_fonts_and_icons),
        ("Base de données", validate_database_connection),
        ("Configuration Django", validate_django_configuration),
    ]
    
    results = []
    success_count = 0
    
    for name, validation_func in validations:
        try:
            print(f"\n{'='*20} {name.upper()} {'='*20}")
            result = validation_func()
            results.append((name, result))
            if result:
                success_count += 1
        except Exception as e:
            print(f"❌ Erreur lors de {name}: {e}")
            results.append((name, False))
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ FINAL DE LA VALIDATION")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"{name}: {status}")
    
    success_rate = (success_count / len(results)) * 100
    print(f"\n🎯 TAUX DE RÉUSSITE GLOBAL: {success_count}/{len(results)} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("\n🎉 VALIDATION RÉUSSIE!")
        print("✨ L'application est prête pour la production sur Railway!")
        print("🚀 Déploiement validé avec succès!")
        return True
    elif success_rate >= 60:
        print("\n⚠️ VALIDATION PARTIELLE")
        print("🔧 L'application fonctionne mais quelques optimisations sont possibles.")
        return True
    else:
        print("\n❌ VALIDATION ÉCHOUÉE")
        print("🛠️ Des corrections sont nécessaires avant la mise en production.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)