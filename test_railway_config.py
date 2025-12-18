#!/usr/bin/env python
"""
Test de la nouvelle configuration Railway build-safe
Simule les deux phases: build et runtime
"""
import os
import sys
import tempfile
from pathlib import Path

def test_build_phase():
    """Teste la phase de build (sans variables MySQL)"""
    print("🔧 Test Phase BUILD (sans variables MySQL)")
    print("-" * 50)
    
    # Sauvegarder les variables existantes
    mysql_vars = {}
    mysql_var_names = ['MYSQLHOST', 'MYSQLDATABASE', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLPORT']
    
    for var in mysql_var_names:
        mysql_vars[var] = os.environ.get(var)
        if var in os.environ:
            del os.environ[var]
    
    try:
        # Configurer Django pour le test
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
        
        # Importer les settings (simule collectstatic)
        import django
        from django.conf import settings
        django.setup()
        
        # Vérifier la configuration
        db_config = settings.DATABASES['default']
        
        if db_config['ENGINE'] == 'django.db.backends.sqlite3':
            print("✅ Configuration SQLite détectée pour le build")
            print(f"✅ DB temporaire: {db_config['NAME']}")
            
            # Test de connexion SQLite
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            if result and result[0] == 1:
                print("✅ Connexion SQLite build réussie")
                return True
            else:
                print("❌ Connexion SQLite build échouée")
                return False
        else:
            print("❌ Configuration MySQL détectée pendant le build (problème!)")
            return False
            
    except Exception as e:
        print(f"❌ Erreur pendant le test build: {e}")
        return False
    
    finally:
        # Restaurer les variables
        for var, value in mysql_vars.items():
            if value:
                os.environ[var] = value

def test_runtime_phase():
    """Teste la phase runtime (avec variables MySQL simulées)"""
    print("\n🚀 Test Phase RUNTIME (avec variables MySQL)")
    print("-" * 50)
    
    # Simuler les variables MySQL Railway
    test_mysql_vars = {
        'MYSQLHOST': 'containers-us-west-test.railway.app',
        'MYSQLDATABASE': 'railway',
        'MYSQLUSER': 'root',
        'MYSQLPASSWORD': 'test-password-123',
        'MYSQLPORT': '3306'
    }
    
    # Sauvegarder les variables existantes
    original_vars = {}
    for var in test_mysql_vars:
        original_vars[var] = os.environ.get(var)
        os.environ[var] = test_mysql_vars[var]
    
    try:
        # Recharger les settings
        if 'django.conf' in sys.modules:
            del sys.modules['django.conf']
        if 'CabinetAvocat.settings_production' in sys.modules:
            del sys.modules['CabinetAvocat.settings_production']
        
        # Configurer Django pour le test runtime
        os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
        
        import django
        from django.conf import settings
        django.setup()
        
        # Vérifier la configuration MySQL
        db_config = settings.DATABASES['default']
        
        if db_config['ENGINE'] == 'django.db.backends.mysql':
            print("✅ Configuration MySQL détectée pour le runtime")
            print(f"✅ Host: {db_config['HOST']}")
            print(f"✅ Database: {db_config['NAME']}")
            print(f"✅ User: {db_config['USER']}")
            print(f"✅ Port: {db_config['PORT']}")
            
            # Note: On ne teste pas la vraie connexion MySQL car c'est un test local
            print("✅ Configuration MySQL valide (connexion non testée)")
            return True
        else:
            print("❌ Configuration SQLite détectée pendant le runtime (problème!)")
            return False
            
    except Exception as e:
        print(f"❌ Erreur pendant le test runtime: {e}")
        return False
    
    finally:
        # Restaurer les variables originales
        for var, value in original_vars.items():
            if value:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]

def test_wait_for_mysql_script():
    """Teste le script wait_for_mysql.py"""
    print("\n⏳ Test Script wait_for_mysql.py")
    print("-" * 50)
    
    # Test sans variables (doit échouer proprement)
    mysql_var_names = ['MYSQLHOST', 'MYSQLDATABASE', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLPORT']
    original_vars = {}
    
    for var in mysql_var_names:
        original_vars[var] = os.environ.get(var)
        if var in os.environ:
            del os.environ[var]
    
    try:
        # Importer et tester wait_for_mysql
        import importlib.util
        spec = importlib.util.spec_from_file_location("wait_for_mysql", "wait_for_mysql.py")
        wait_module = importlib.util.module_from_spec(spec)
        
        # Test de validation des variables (doit échouer)
        try:
            result = wait_module.wait_for_mysql(max_attempts=1, delay=1)
            if not result:
                print("✅ Script détecte correctement les variables manquantes")
                return True
            else:
                print("❌ Script ne détecte pas les variables manquantes")
                return False
        except SystemExit:
            print("✅ Script sort proprement quand variables manquantes")
            return True
            
    except Exception as e:
        print(f"❌ Erreur test wait_for_mysql: {e}")
        return False
    
    finally:
        # Restaurer les variables
        for var, value in original_vars.items():
            if value:
                os.environ[var] = value

def main():
    """Fonction principale de test"""
    print("🧪 Test Configuration Railway Build-Safe")
    print("=" * 60)
    
    # Tests
    tests = [
        ("Phase BUILD (SQLite)", test_build_phase),
        ("Phase RUNTIME (MySQL)", test_runtime_phase),
        ("Script wait_for_mysql", test_wait_for_mysql_script),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{len(tests)} tests réussis")
    
    if passed == len(tests):
        print("\n🎉 CONFIGURATION VALIDÉE!")
        print("✅ Build Railway réussira (SQLite pour collectstatic)")
        print("✅ Runtime Railway utilisera MySQL")
        print("✅ Pas de crash pendant le déploiement")
        print("\n🚀 Prêt pour le déploiement Railway!")
        return True
    else:
        print("\n⚠️ CONFIGURATION INCOMPLÈTE")
        print("🔧 Vérifier les erreurs ci-dessus")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)