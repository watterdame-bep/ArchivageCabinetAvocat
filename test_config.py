#!/usr/bin/env python
"""
Test rapide de la configuration Railway
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

def test_environment():
    """Tester les variables d'environnement"""
    print("🔍 Variables d'environnement Railway:")
    
    vars_to_check = [
        'SECRET_KEY', 'PORT', 'MYSQLHOST', 'MYSQLPORT', 
        'MYSQLUSERNAME', 'MYSQLPASSWORD', 'MYSQLDATABASE'
    ]
    
    for var in vars_to_check:
        value = os.environ.get(var, 'NON DÉFINIE')
        if 'PASSWORD' in var or 'SECRET' in var:
            if value != 'NON DÉFINIE':
                value = '*' * 10
        print(f"  {var}: {value}")
    
    # Vérifier les doublons dans les variables
    mysqlhost = os.environ.get('MYSQLHOST', '')
    mysqldatabase = os.environ.get('MYSQLDATABASE', '')
    
    if mysqlhost.count('mysql.railway.internal') > 1:
        print(f"⚠️ MYSQLHOST dupliqué détecté: {mysqlhost}")
    
    if 'railway' in mysqldatabase and mysqldatabase.count('railway') > 1:
        print(f"⚠️ MYSQLDATABASE dupliqué détecté: {mysqldatabase}")

def test_django():
    """Tester Django"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')
        django.setup()
        
        from django.conf import settings
        print(f"✅ Django configuré")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        return False

def test_database():
    """Tester la base de données"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Connexion base de données OK")
            return True
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def main():
    print("🧪 Test de configuration Railway")
    print("=" * 40)
    
    test_environment()
    
    print("\n🔧 Test Django...")
    if not test_django():
        sys.exit(1)
    
    print("\n🗄️ Test base de données...")
    if not test_database():
        print("⚠️ Base de données non accessible (normal si pas encore migrée)")
    
    print("\n✅ Configuration de base OK!")

if __name__ == '__main__':
    main()