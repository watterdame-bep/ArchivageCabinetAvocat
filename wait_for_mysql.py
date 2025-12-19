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
    
    # Vérifier les variables d'environnement Railway (noms exacts)
    required_vars = ['MYSQL_HOST', 'MYSQLUSER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE', 'MYSQL_PORT']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Variables MySQL manquantes: {', '.join(missing_vars)}")
        print("💡 Ajouter un service MySQL dans Railway Dashboard")
        print("💡 Puis connecter les variables au service Django")
        sys.exit(1)
    
    # Configuration MySQL Railway (noms exacts des variables)
    config = {
        'host': os.environ['MYSQL_HOST'],
        'user': os.environ['MYSQLUSER'],  # Railway utilise MYSQLUSER
        'password': os.environ['MYSQL_PASSWORD'],
        'database': os.environ['MYSQL_DATABASE'],
        'port': int(os.environ['MYSQL_PORT']),
        'connect_timeout': 10,
        'read_timeout': 10,
        'write_timeout': 10,
        # Configuration pour MySQL 9.x Railway avec PyMySQL
        'ssl_disabled': True,  # Simplifie la connexion Railway
        'autocommit': True
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