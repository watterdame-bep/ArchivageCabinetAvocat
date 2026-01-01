#!/usr/bin/env python
"""
Test simple de connexion MySQL avec les variables Railway
"""
import os
from decouple import config

def test_mysql_variables():
    """Vérifier que toutes les variables MySQL sont présentes"""
    print("🔍 Vérification des variables MySQL Railway...")
    
    required_vars = {
        'MYSQLHOST': config('MYSQLHOST', default=None),
        'MYSQLPORT': config('MYSQLPORT', default=None),
        'MYSQLUSERNAME': config('MYSQLUSERNAME', default=None),
        'MYSQLPASSWORD': config('MYSQLPASSWORD', default=None),
        'MYSQLDATABASE': config('MYSQLDATABASE', default=None),
    }
    
    missing_vars = []
    for var_name, var_value in required_vars.items():
        if var_value is None:
            missing_vars.append(var_name)
            print(f"❌ {var_name}: Non définie")
        else:
            if 'PASSWORD' in var_name:
                print(f"✅ {var_name}: {'*' * len(str(var_value))}")
            else:
                print(f"✅ {var_name}: {var_value}")
    
    if missing_vars:
        print(f"\n⚠️ Variables manquantes: {', '.join(missing_vars)}")
        print("💡 Assurez-vous que le service MySQL est connecté au service backend dans Railway")
        return False
    else:
        print("\n✅ Toutes les variables MySQL sont présentes!")
        return True

def test_mysql_connection():
    """Tester la connexion MySQL avec PyMySQL"""
    try:
        import pymysql
        
        connection = pymysql.connect(
            host=config('MYSQLHOST'),
            port=int(config('MYSQLPORT', default=3306)),
            user=config('MYSQLUSERNAME'),
            password=config('MYSQLPASSWORD'),
            database=config('MYSQLDATABASE'),
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
            
        connection.close()
        return True
        
    except ImportError:
        print("❌ PyMySQL n'est pas installé. Installez-le avec: pip install PyMySQL")
        return False
    except Exception as e:
        print(f"❌ Erreur de connexion MySQL: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Test de connexion MySQL Railway")
    print("=" * 40)
    
    # Vérifier les variables
    if test_mysql_variables():
        print("\n🔌 Test de connexion...")
        if test_mysql_connection():
            print("\n🎉 Configuration MySQL Railway parfaite!")
        else:
            print("\n❌ Problème de connexion MySQL")
    else:
        print("\n❌ Configuration incomplète")