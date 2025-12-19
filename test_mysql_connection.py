#!/usr/bin/env python
"""
Script de test de connexion MySQL Railway
Pour débugger les problèmes de connexion
"""
import os
import pymysql

def test_mysql_connection():
    """Test simple de connexion MySQL"""
    print("🔍 Test de connexion MySQL Railway")
    print("=" * 50)
    
    # Afficher les variables d'environnement
    mysql_vars = ['MYSQLHOST', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLDATABASE', 'MYSQLPORT']
    
    print("📋 Variables d'environnement:")
    for var in mysql_vars:
        value = os.environ.get(var, 'NON DÉFINIE')
        if var == 'MYSQLPASSWORD':
            # Masquer le mot de passe
            display_value = '*' * len(value) if value != 'NON DÉFINIE' else 'NON DÉFINIE'
        else:
            display_value = value
        print(f"   {var}: {display_value}")
    
    print("\n" + "=" * 50)
    
    # Vérifier que toutes les variables sont présentes
    missing = [var for var in mysql_vars if not os.environ.get(var)]
    if missing:
        print(f"❌ Variables manquantes: {', '.join(missing)}")
        return False
    
    # Configuration de connexion
    config = {
        'host': os.environ['MYSQLHOST'],
        'user': os.environ['MYSQLUSER'],
        'password': os.environ['MYSQLPASSWORD'],
        'database': os.environ['MYSQLDATABASE'],
        'port': int(os.environ['MYSQLPORT']),
        'connect_timeout': 30,
    }
    
    print(f"🔗 Tentative de connexion à: {config['user']}@{config['host']}:{config['port']}/{config['database']}")
    
    try:
        # Installer PyMySQL
        pymysql.install_as_MySQLdb()
        
        # Connexion
        connection = pymysql.connect(**config)
        print("✅ Connexion MySQL réussie!")
        
        # Test simple
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"📊 Version MySQL: {version[0]}")
        
        # Test des tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📋 Nombre de tables: {len(tables)}")
        
        if len(tables) > 0:
            print("🗂️ Quelques tables trouvées:")
            for i, table in enumerate(tables[:5]):  # Afficher les 5 premières
                print(f"   - {table[0]}")
            if len(tables) > 5:
                print(f"   ... et {len(tables) - 5} autres")
        
        cursor.close()
        connection.close()
        
        print("✅ Test de connexion MySQL réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion MySQL: {e}")
        print(f"🔧 Type d'erreur: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_mysql_connection()
    exit(0 if success else 1)