#!/usr/bin/env python
"""
Script de diagnostic complet pour Railway
Identifie pourquoi Django se connecte à localhost au lieu de Railway MySQL
"""
import os
import sys

def debug_railway_environment():
    """Diagnostic complet de l'environnement Railway"""
    print("🔍 DIAGNOSTIC RAILWAY - VARIABLES D'ENVIRONNEMENT")
    print("=" * 60)
    
    # 1. Vérifier le fichier de settings utilisé
    print("1️⃣ CONFIGURATION DJANGO:")
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'NON DÉFINI')
    print(f"   DJANGO_SETTINGS_MODULE: {settings_module}")
    
    if 'production' not in settings_module.lower():
        print("   ⚠️  ATTENTION: Django n'utilise pas settings_production!")
        print("   💡 Vérifiez que DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production")
    
    print("\n" + "-" * 60)
    
    # 2. Vérifier toutes les variables MySQL Railway
    print("2️⃣ VARIABLES MYSQL RAILWAY:")
    mysql_vars = {
        'MYSQLHOST': 'Host du serveur MySQL',
        'MYSQLUSER': 'Nom d\'utilisateur MySQL',
        'MYSQLPASSWORD': 'Mot de passe MySQL',
        'MYSQLDATABASE': 'Nom de la base de données',
        'MYSQLPORT': 'Port MySQL'
    }
    
    missing_vars = []
    for var, description in mysql_vars.items():
        value = os.environ.get(var)
        if value:
            if var == 'MYSQLPASSWORD':
                display_value = '*' * len(value)
            else:
                display_value = value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: NON DÉFINIE")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n   🚨 PROBLÈME CRITIQUE: Variables manquantes: {', '.join(missing_vars)}")
        print("   💡 Dans Railway Dashboard:")
        print("      1. Allez dans votre service Django")
        print("      2. Onglet 'Variables'")
        print("      3. Cliquez 'Add Variable Reference'")
        print("      4. Sélectionnez votre service MySQL")
        print("      5. Redéployez")
    
    print("\n" + "-" * 60)
    
    # 3. Vérifier d'autres variables importantes
    print("3️⃣ AUTRES VARIABLES IMPORTANTES:")
    other_vars = ['PORT', 'RAILWAY_ENVIRONMENT', 'RAILWAY_PROJECT_ID', 'RAILWAY_SERVICE_ID']
    for var in other_vars:
        value = os.environ.get(var, 'NON DÉFINIE')
        print(f"   {var}: {value}")
    
    print("\n" + "-" * 60)
    
    # 4. Test d'import des settings
    print("4️⃣ TEST D'IMPORT DES SETTINGS:")
    try:
        # Forcer l'utilisation de settings_production
        os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
        
        import django
        django.setup()
        
        from django.conf import settings
        
        print("   ✅ Import des settings réussi")
        
        # Vérifier la configuration de la base de données
        db_config = settings.DATABASES.get('default', {})
        db_host = db_config.get('HOST', 'NON DÉFINI')
        db_name = db_config.get('NAME', 'NON DÉFINI')
        db_user = db_config.get('USER', 'NON DÉFINI')
        db_port = db_config.get('PORT', 'NON DÉFINI')
        
        print(f"   📊 Configuration DB Django:")
        print(f"      HOST: {db_host}")
        print(f"      NAME: {db_name}")
        print(f"      USER: {db_user}")
        print(f"      PORT: {db_port}")
        
        if db_host == 'localhost' or not db_host:
            print("   🚨 PROBLÈME: Django utilise localhost au lieu de Railway!")
            print("   💡 Les variables MySQL ne sont pas injectées correctement")
        else:
            print("   ✅ Django utilise le bon host Railway")
            
    except Exception as e:
        print(f"   ❌ Erreur d'import des settings: {e}")
    
    print("\n" + "=" * 60)
    
    # 5. Résumé et recommandations
    print("5️⃣ RÉSUMÉ ET RECOMMANDATIONS:")
    
    if missing_vars:
        print("   🚨 PROBLÈME PRINCIPAL: Variables MySQL manquantes")
        print("   🔧 SOLUTION: Connecter le service MySQL au service Django dans Railway")
        return False
    elif settings_module != 'CabinetAvocat.settings_production':
        print("   🚨 PROBLÈME PRINCIPAL: Mauvais fichier de settings")
        print("   🔧 SOLUTION: Définir DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production")
        return False
    else:
        print("   ✅ Configuration semble correcte")
        print("   💡 Si le problème persiste, vérifiez les logs Railway pour plus de détails")
        return True

if __name__ == "__main__":
    success = debug_railway_environment()
    sys.exit(0 if success else 1)