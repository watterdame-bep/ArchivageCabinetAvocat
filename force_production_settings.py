#!/usr/bin/env python
"""
Script pour forcer l'utilisation de settings_production
et vérifier que Django utilise la bonne configuration
"""
import os
import sys

def force_production_settings():
    """Force l'utilisation de settings_production"""
    print("🔧 Forçage de la configuration production...")
    
    # Forcer settings_production
    os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
    print(f"✅ DJANGO_SETTINGS_MODULE défini: {os.environ['DJANGO_SETTINGS_MODULE']}")
    
    # Vérifier les variables MySQL
    mysql_vars = ['MYSQLHOST', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLDATABASE', 'MYSQLPORT']
    missing = [var for var in mysql_vars if not os.environ.get(var)]
    
    if missing:
        print(f"❌ Variables MySQL manquantes: {', '.join(missing)}")
        print("💡 Le service MySQL n'est pas connecté au service Django dans Railway")
        return False
    
    try:
        # Test d'import Django avec la bonne configuration
        import django
        django.setup()
        
        from django.conf import settings
        
        # Vérifier la configuration DB
        db_config = settings.DATABASES['default']
        db_host = db_config.get('HOST')
        
        print(f"🔍 Host configuré dans Django: {db_host}")
        
        if db_host and db_host != 'localhost':
            print("✅ Django utilise la configuration Railway MySQL")
            return True
        else:
            print("❌ Django utilise encore localhost - problème de configuration")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test Django: {e}")
        return False

if __name__ == "__main__":
    success = force_production_settings()
    sys.exit(0 if success else 1)