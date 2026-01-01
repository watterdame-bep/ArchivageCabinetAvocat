#!/usr/bin/env python
"""
Test spécifique de connexion MySQL Railway
"""
import os
import pymysql

def clean_mysql_vars():
    """Nettoyer et afficher les variables MySQL"""
    print("🔍 Variables MySQL Railway (nettoyées):")
    
    # Nettoyer MYSQLHOST
    mysqlhost = os.environ.get('MYSQLHOST', '')
    if mysqlhost.count('mysql.railway.internal') > 1:
        mysqlhost = 'mysql.railway.internal'
        print(f"⚠️ MYSQLHOST dupliqué détecté, nettoyé: {mysqlhost}")
    
    # Nettoyer MYSQLDATABASE
    mysqldatabase = os.environ.get('MYSQLDATABASE', '')
    if 'railway' in mysqldatabase and mysqldatabase.count('railway') > 1:
        mysqldatabase = 'railway'
        print(f"⚠️ MYSQLDATABASE dupliqué détecté, nettoyé: {mysqldatabase}")
    
    mysql_config = {
        'host': mysqlhost or os.environ.get('MYSQLHOST', 'localhost'),
        'port': int(os.environ.get('MYSQLPORT', 3306)),
        'user': os.environ.get('MYSQLUSERNAME', 'root'),
        'password': os.environ.get('MYSQLPASSWORD', ''),
        'database': mysqldatabase or os.environ.get('MYSQLDATABASE', 'test'),
    }
    
    print(f"  HOST: {mysql_config['host']}")
    print(f"  PORT: {mysql_config['port']}")
    print(f"  USER: {mysql_config['user']}")
    print(f"  PASSWORD: {'*' * len(mysql_config['password']) if mysql_config['password'] else 'VIDE'}")
    print(f"  DATABASE: {mysql_config['database']}")
    
    return mysql_config

def test_mysql_connection():
    """Tester la connexion MySQL avec PyMySQL"""
    print("\n🔌 Test de connexion MySQL...")
    
    mysql_config = clean_mysql_vars()
    
    try:
        # Configuration PyMySQL
        pymysql.install_as_MySQLdb()
        print("✅ PyMySQL configuré comme MySQLdb")
        
        # Test de connexion
        connection = pymysql.connect(
            host=mysql_config['host'],
            port=mysql_config['port'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            database=mysql_config['database'],
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Connexion MySQL réussie!")
            print(f"📊 Version MySQL: {version[0]}")
            
            cursor.execute("SELECT DATABASE()")
            database = cursor.fetchone()
            print(f"🗄️ Base de données active: {database[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Nombre de tables: {len(tables)}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion MySQL: {e}")
        print(f"🔍 Détails de l'erreur: {type(e).__name__}")
        
        # Suggestions de dépannage
        if "Name or service not known" in str(e):
            print("💡 Le service MySQL n'est peut-être pas accessible")
            print("💡 Vérifiez que le service MySQL est démarré dans Railway")
        elif "Access denied" in str(e):
            print("💡 Problème d'authentification MySQL")
            print("💡 Vérifiez les credentials dans Railway")
        
        return False

def main():
    print("🧪 Test de connexion MySQL Railway")
    print("=" * 50)
    
    if test_mysql_connection():
        print("\n🎉 Connexion MySQL réussie!")
        print("✅ La base de données est accessible")
    else:
        print("\n❌ Problème de connexion MySQL")
        print("🔧 Vérifiez la configuration Railway")

if __name__ == '__main__':
    main()