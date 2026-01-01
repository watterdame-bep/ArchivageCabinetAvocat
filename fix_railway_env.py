#!/usr/bin/env python
"""
Script pour corriger les variables d'environnement Railway
"""
import os

def check_and_fix_env():
    """Vérifier et corriger les variables d'environnement"""
    print("🔧 Correction des variables d'environnement Railway...")
    
    # Vérifier MYSQLUSERNAME
    if not os.environ.get('MYSQLUSERNAME'):
        # Essayer de déduire depuis d'autres variables
        if os.environ.get('MYSQLUSER'):
            os.environ['MYSQLUSERNAME'] = os.environ.get('MYSQLUSER')
            print("✅ MYSQLUSERNAME défini depuis MYSQLUSER")
        else:
            # Valeur par défaut pour Railway MySQL
            os.environ['MYSQLUSERNAME'] = 'root'
            print("✅ MYSQLUSERNAME défini par défaut: root")
    
    # Afficher les variables MySQL
    mysql_vars = ['MYSQLHOST', 'MYSQLPORT', 'MYSQLDATABASE', 'MYSQLUSERNAME', 'MYSQLPASSWORD']
    print("\n📋 Variables MySQL Railway:")
    for var in mysql_vars:
        value = os.environ.get(var, 'NON_DÉFINIE')
        masked_value = '*' * len(value) if value != 'NON_DÉFINIE' else 'NON_DÉFINIE'
        print(f"  {var}: {masked_value}")
    
    return True

if __name__ == '__main__':
    check_and_fix_env()