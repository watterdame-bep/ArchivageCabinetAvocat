#!/usr/bin/env python
"""
Test PyMySQL pour Railway
"""
import os

def test_pymysql():
    """Tester PyMySQL"""
    try:
        import pymysql
        print(f"✅ PyMySQL importé - Version: {pymysql.__version__}")
        
        # Configuration comme MySQLdb
        pymysql.install_as_MySQLdb()
        print("✅ PyMySQL configuré comme MySQLdb")
        
        # Test d'import MySQLdb
        import MySQLdb
        print("✅ MySQLdb disponible via PyMySQL")
        
        return True
    except Exception as e:
        print(f"❌ Erreur PyMySQL: {e}")
        return False

def test_railway_mysql_vars():
    """Tester les variables MySQL Railway"""
    print("\n🔍 Variables MySQL Railway:")
    mysql_vars = {
        'MYSQLHOST': os.environ.get('MYSQLHOST', 'Non définie'),
        'MYSQLPORT': os.environ.get('MYSQLPORT', 'Non définie'),
        'MYSQLUSERNAME': os.environ.get('MYSQLUSERNAME', 'Non définie'),
        'MYSQLPASSWORD': os.environ.get('MYSQLPASSWORD', 'Non définie'),
        'MYSQLDATABASE': os.environ.get('MYSQLDATABASE', 'Non définie'),
    }
    
    all_set = True
    for var, value in mysql_vars.items():
        if value == 'Non définie':
            print(f"❌ {var}: {value}")
            all_set = False
        else:
            if 'PASSWORD' in var:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
    
    return all_set

def test_connection():
    """Tester la connexion MySQL avec PyMySQL"""
    try:
        import pymysql
        
        connection = pymysql.connect(
            host=os.environ.get('MYSQLHOST', 'localhost'),
            port=int(os.environ.get('MYSQLPORT', 3306)),
            user=os.environ.get('MYSQLUSERNAME', 'root'),
            password=os.environ.get('MYSQLPASSWORD', ''),
            database=os.environ.get('MYSQLDATABASE', 'test'),
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Connexion MySQL réussie!")
            print(f"📊 Version MySQL: {version[0]}")
            
            cursor.execute("SELECT DATABASE()")
            database = cursor.fetchone()
            print(f"🗄️ Base de données: {database[0]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def main():
    print("🧪 Test PyMySQL pour Railway")
    print("=" * 40)
    
    # Test PyMySQL
    if not test_pymysql():
        return
    
    # Test variables Railway
    if not test_railway_mysql_vars():
        print("\n⚠️ Certaines variables MySQL manquent")
        print("💡 Assurez-vous que le service MySQL est connecté")
        return
    
    # Test de connexion
    print("\n🔌 Test de connexion...")
    if test_connection():
        print("\n🎉 Tous les tests PyMySQL réussis!")
        print("✅ Configuration prête pour Railway")
    else:
        print("\n❌ Problème de connexion MySQL")

if __name__ == '__main__':
    main()