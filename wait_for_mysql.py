#!/usr/bin/env python
"""
Script d'attente MySQL pour Railway
Attend que MySQL soit prêt avant de démarrer Django
"""
import os
import sys
import time
import pymysql

def wait_for_mysql(max_attempts=30, delay=5):
    """Attend que MySQL soit prêt"""
    print("⏳ Attente de MySQL Railway...")
    
    # Vérifier les variables d'environnement Railway
    required_vars = ['MYSQLHOST', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLDATABASE', 'MYSQLPORT']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Variables MySQL manquantes: {', '.join(missing_vars)}")
        print("💡 Ajouter un service MySQL dans Railway Dashboard")
        print("💡 Puis connecter les variables au service Django")
        sys.exit(1)
    
    # Configuration MySQL Railway
    config = {
        'host': os.environ['MYSQLHOST'],
        'user': os.environ['MYSQLUSER'],
        'password': os.environ['MYSQLPASSWORD'],
        'database': os.environ['MYSQLDATABASE'],
        'port': int(os.environ['MYSQLPORT']),
        'connect_timeout': 10,
        'read_timeout': 10,
        'write_timeout': 10
    }
    
    print(f"🔗 Tentative de connexion: {config['user']}@{config['host']}:{config['port']}/{config['database']}")
    
    # Boucle d'attente
    for attempt in range(1, max_attempts + 1):
        try:
            # Installer PyMySQL
            pymysql.install_as_MySQLdb()
            
            # Tenter la connexion
            connection = pymysql.connect(**config)
            
            # Test simple
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if result and result[0] == 1:
                print(f"✅ MySQL Railway prêt! (tentative {attempt}/{max_attempts})")
                return True
                
        except Exception as e:
            print(f"⏳ Tentative {attempt}/{max_attempts} échouée: {e}")
            
            if attempt < max_attempts:
                print(f"🔄 Nouvelle tentative dans {delay}s...")
                time.sleep(delay)
            else:
                print(f"❌ MySQL non accessible après {max_attempts} tentatives")
                print("🔧 Vérifiez que le service MySQL est démarré dans Railway")
                return False
    
    return False

if __name__ == "__main__":
    success = wait_for_mysql()
    sys.exit(0 if success else 1)