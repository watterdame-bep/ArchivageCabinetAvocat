#!/usr/bin/env python
"""
Script de vérification finale du déploiement Railway
"""
import os
import sys
from pathlib import Path
import django
from django.conf import settings

def check_environment():
    """Vérifier les variables d'environnement"""
    print("🔍 Vérification des variables d'environnement...")
    
    required_vars = ['SECRET_KEY', 'MYSQLHOST', 'MYSQLDATABASE', 'MYSQLUSERNAME', 'MYSQLPASSWORD']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * len(os.environ.get(var, ''))}")
    
    if missing_vars:
        print(f"❌ Variables manquantes: {', '.join(missing_vars)}")
        return False
    
    print("✅ Toutes les variables d'environnement sont définies")
    return True

def check_static_files():
    """Vérifier les fichiers statiques critiques"""
    print("\n📦 Vérification des fichiers statiques...")
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
    else:
        staticfiles_path = Path('staticfiles')
    
    critical_files = [
        'css/bootstrap.min.css',
        'css/railway-fixes.css',
        'css/media-fallback.css',
        'js/bootstrap.min.js',
        'assets/vendor_components/raty-master/lib/jquery.raty.css',
        'assets/vendor_components/bootstrap-touchspin/dist/jquery.bootstrap-touchspin.css',
        'assets/vendor_components/apexcharts-bundle/dist/apexcharts.js',
    ]
    
    missing_files = []
    for file_path in critical_files:
        full_path = staticfiles_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    if missing_files:
        print(f"\n⚠️ Fichiers manquants: {len(missing_files)}")
        return False
    
    print(f"\n✅ Tous les fichiers statiques critiques sont présents")
    return True

def check_database_connection():
    """Tester la connexion à la base de données"""
    print("\n🗄️ Test de connexion à la base de données...")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')
        django.setup()
        
        from django.db import connection
        
        # Test de connexion
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        print("✅ Connexion à la base de données réussie")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def check_django_configuration():
    """Vérifier la configuration Django"""
    print("\n⚙️ Vérification de la configuration Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')
        django.setup()
        
        from django.core.management import execute_from_command_line
        
        # Test de la configuration
        execute_from_command_line(['manage.py', 'check', '--deploy'])
        
        print("✅ Configuration Django valide")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False

def main():
    """Fonction principale de vérification"""
    print("🎯 VÉRIFICATION FINALE DU DÉPLOIEMENT RAILWAY")
    print("=" * 60)
    
    checks = [
        ("Variables d'environnement", check_environment),
        ("Fichiers statiques", check_static_files),
        ("Connexion base de données", check_database_connection),
        ("Configuration Django", check_django_configuration),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erreur lors de {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 60)
    
    success_count = 0
    for name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"{name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n🎯 RÉSULTAT GLOBAL: {success_count}/{len(results)} vérifications réussies")
    
    if success_count == len(results):
        print("🎉 DÉPLOIEMENT PRÊT! L'application devrait fonctionner parfaitement sur Railway.")
        return True
    else:
        print("⚠️ Des problèmes ont été détectés. Veuillez les corriger avant le déploiement.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)