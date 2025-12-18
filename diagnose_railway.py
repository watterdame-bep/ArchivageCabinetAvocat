#!/usr/bin/env python
"""
Script de diagnostic Railway - Vérifie la configuration avant déploiement
Usage: python diagnose_railway.py
"""
import os
import sys

def check_railway_environment():
    """Vérifie si on est dans un environnement Railway"""
    print("🔍 Détection de l'environnement Railway...")
    
    railway_indicators = [
        'RAILWAY_STATIC_URL',
        'RAILWAY_GIT_COMMIT_SHA', 
        'PORT',
        'RAILWAY_ENVIRONMENT_NAME',
        'RAILWAY_PROJECT_NAME'
    ]
    
    detected = []
    for var in railway_indicators:
        if os.environ.get(var):
            detected.append(var)
    
    if detected:
        print(f"✅ Environnement Railway détecté! Variables: {', '.join(detected)}")
        return True
    else:
        print("⚠️ Environnement Railway non détecté (normal en local)")
        return False

def check_mysql_variables():
    """Vérifie les variables MySQL de Railway"""
    print("\n🔍 Vérification des variables MySQL...")
    
    mysql_vars = {
        'MYSQL_HOST': os.environ.get('MYSQL_HOST'),
        'MYSQL_DATABASE': os.environ.get('MYSQL_DATABASE'),
        'MYSQL_USER': os.environ.get('MYSQL_USER'),
        'MYSQL_PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'MYSQL_PORT': os.environ.get('MYSQL_PORT', '3306'),
        'MYSQL_URL': os.environ.get('MYSQL_URL', 'Non définie')
    }
    
    missing = []
    for var, value in mysql_vars.items():
        if value and var != 'MYSQL_URL':
            if var == 'MYSQL_PASSWORD':
                print(f"✅ {var}: [MASQUÉ - {len(value)} caractères]")
            else:
                print(f"✅ {var}: {value}")
        elif var in ['MYSQL_HOST', 'MYSQL_DATABASE', 'MYSQL_USER', 'MYSQL_PASSWORD']:
            print(f"❌ {var}: MANQUANTE")
            missing.append(var)
        else:
            print(f"ℹ️ {var}: {value}")
    
    if missing:
        print(f"\n❌ Variables MySQL manquantes: {', '.join(missing)}")
        print("💡 Solution: Ajouter un service MySQL dans Railway Dashboard")
        return False
    else:
        print("\n✅ Toutes les variables MySQL sont définies")
        return True

def check_django_variables():
    """Vérifie les variables Django essentielles"""
    print("\n🔍 Vérification des variables Django...")
    
    django_vars = {
        'DJANGO_SETTINGS_MODULE': os.environ.get('DJANGO_SETTINGS_MODULE'),
        'SECRET_KEY': os.environ.get('SECRET_KEY'),
        'DEBUG': os.environ.get('DEBUG', 'Non définie'),
        'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS', 'Non définie')
    }
    
    missing = []
    for var, value in django_vars.items():
        if value and value != 'Non définie':
            if var == 'SECRET_KEY':
                print(f"✅ {var}: [MASQUÉ - {len(value)} caractères]")
            else:
                print(f"✅ {var}: {value}")
        elif var in ['DJANGO_SETTINGS_MODULE', 'SECRET_KEY']:
            print(f"❌ {var}: MANQUANTE")
            missing.append(var)
        else:
            print(f"ℹ️ {var}: {value}")
    
    if missing:
        print(f"\n❌ Variables Django manquantes: {', '.join(missing)}")
        return False
    else:
        print("\n✅ Variables Django essentielles définies")
        return True

def check_jsreport_variables():
    """Vérifie les variables JSReport"""
    print("\n🔍 Vérification des variables JSReport...")
    
    jsreport_vars = {
        'JSREPORT_URL': os.environ.get('JSREPORT_URL'),
        'JSREPORT_USERNAME': os.environ.get('JSREPORT_USERNAME'),
        'JSREPORT_PASSWORD': os.environ.get('JSREPORT_PASSWORD'),
        'JSREPORT_TIMEOUT': os.environ.get('JSREPORT_TIMEOUT', '120')
    }
    
    missing = []
    for var, value in jsreport_vars.items():
        if value:
            if var == 'JSREPORT_PASSWORD':
                print(f"✅ {var}: [MASQUÉ - {len(value)} caractères]")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️ {var}: NON DÉFINIE")
            if var != 'JSREPORT_TIMEOUT':  # JSREPORT_TIMEOUT a une valeur par défaut
                missing.append(var)
    
    if missing:
        print(f"\n⚠️ Variables JSReport manquantes: {', '.join(missing)}")
        print("💡 Normal si JSReport n'est pas encore déployé")
        return False
    else:
        print("\n✅ Variables JSReport définies")
        return True

def test_database_connection():
    """Teste la connexion à la base de données"""
    print("\n🔍 Test de connexion à la base de données...")
    
    try:
        # Configurer Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
        import django
        django.setup()
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            print("✅ Connexion à la base de données réussie!")
            return True
        else:
            print("❌ Test de connexion échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def generate_railway_config():
    """Génère un exemple de configuration Railway"""
    print("\n📋 Configuration Railway recommandée:")
    print("=" * 50)
    
    print("\n🔧 Variables à ajouter dans Railway Dashboard:")
    print("(Service Django → Variables)")
    print()
    
    config = """
# Django Core
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=votre-cle-secrete-super-longue-minimum-50-caracteres
DEBUG=False
ALLOWED_HOSTS=.railway.app,.up.railway.app

# JSReport (après déploiement JSReport)
JSREPORT_URL=https://votre-jsreport.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=VotreMotDePasseSecurise
JSREPORT_TIMEOUT=120

# Note: Les variables MYSQL_* sont auto-générées par Railway
# quand vous ajoutez un service MySQL Database
"""
    
    print(config)

def main():
    """Fonction principale de diagnostic"""
    print("🔧 Diagnostic Railway - Cabinet Avocat")
    print("=" * 50)
    
    # Tests de diagnostic
    is_railway = check_railway_environment()
    mysql_ok = check_mysql_variables()
    django_ok = check_django_variables()
    jsreport_ok = check_jsreport_variables()
    
    # Test de connexion DB si on a les variables
    db_ok = False
    if mysql_ok and django_ok:
        db_ok = test_database_connection()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    
    print(f"🌐 Environnement Railway: {'✅ Détecté' if is_railway else '⚠️ Non détecté (normal en local)'}")
    print(f"🗄️ Variables MySQL: {'✅ OK' if mysql_ok else '❌ Manquantes'}")
    print(f"🐍 Variables Django: {'✅ OK' if django_ok else '❌ Manquantes'}")
    print(f"📄 Variables JSReport: {'✅ OK' if jsreport_ok else '⚠️ Manquantes'}")
    print(f"🔗 Connexion DB: {'✅ OK' if db_ok else '❌ Échec' if mysql_ok else '⏭️ Non testée'}")
    
    # Recommandations
    print("\n🎯 RECOMMANDATIONS:")
    
    if not mysql_ok:
        print("1. ➕ Ajouter un service MySQL dans Railway Dashboard")
        print("   → Railway Dashboard → Add Service → Database → MySQL")
    
    if not django_ok:
        print("2. ⚙️ Configurer les variables Django dans Railway")
        print("   → Railway Dashboard → Service Django → Variables")
    
    if not jsreport_ok:
        print("3. 🐳 Déployer JSReport et configurer les variables")
        print("   → Suivre le guide RAILWAY_DEPLOYMENT_STEPS.md")
    
    if mysql_ok and django_ok and not db_ok:
        print("4. 🔧 Vérifier la configuration de la base de données")
        print("   → Vérifier settings_production.py")
    
    # Configuration recommandée
    if not django_ok:
        generate_railway_config()
    
    # Statut final
    if mysql_ok and django_ok and db_ok:
        print("\n🎉 DIAGNOSTIC RÉUSSI - Prêt pour Railway!")
        return True
    else:
        print("\n⚠️ DIAGNOSTIC INCOMPLET - Corriger les points ci-dessus")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)