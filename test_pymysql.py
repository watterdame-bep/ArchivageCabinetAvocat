#!/usr/bin/env python
"""
Test PyMySQL configuration pour Railway
"""
import sys

def test_pymysql_import():
    """Tester l'import de PyMySQL"""
    try:
        import pymysql
        print("✅ PyMySQL importé avec succès")
        print(f"📦 Version PyMySQL: {pymysql.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import PyMySQL: {e}")
        return False

def test_pymysql_as_mysqldb():
    """Tester la configuration PyMySQL comme MySQLdb"""
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        print("✅ PyMySQL configuré comme MySQLdb")
        
        # Tester l'import MySQLdb
        import MySQLdb
        print("✅ MySQLdb disponible via PyMySQL")
        return True
    except Exception as e:
        print(f"❌ Erreur configuration MySQLdb: {e}")
        return False

def test_django_mysql_backend():
    """Tester le backend MySQL Django"""
    try:
        from django.db.backends.mysql import base
        print("✅ Backend MySQL Django disponible")
        return True
    except ImportError as e:
        print(f"❌ Erreur backend MySQL Django: {e}")
        return False

def main():
    print("🔍 Test de configuration PyMySQL pour Railway")
    print("=" * 50)
    
    tests = [
        ("Import PyMySQL", test_pymysql_import),
        ("Configuration MySQLdb", test_pymysql_as_mysqldb),
        ("Backend Django MySQL", test_django_mysql_backend),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 Tous les tests PyMySQL réussis!")
        print("✅ Votre configuration est prête pour Railway")
    else:
        print("❌ Certains tests ont échoué")
        print("💡 Installez PyMySQL: pip install PyMySQL>=1.1.0")
        sys.exit(1)

if __name__ == '__main__':
    main()