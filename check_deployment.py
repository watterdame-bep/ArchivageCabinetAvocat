#!/usr/bin/env python3
"""
Script de vérification avant déploiement Railway
Vérifie que tous les fichiers nécessaires sont présents
"""

import os
import sys

def check_file_exists(filepath, description):
    """Vérifier qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MANQUANT")
        return False

def check_directory_exists(dirpath, description):
    """Vérifier qu'un répertoire existe"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: {dirpath} - MANQUANT")
        return False

def main():
    print("🔍 Vérification des fichiers de déploiement Railway\n")
    
    all_good = True
    
    # Fichiers de configuration Django
    files_to_check = [
        ("requirements.txt", "Dépendances Python"),
        ("runtime.txt", "Version Python"),
        ("Procfile", "Configuration Procfile"),
        ("railway.json", "Configuration Railway"),
        ("manage.py", "Script Django manage.py"),
        (".gitignore", "Fichier .gitignore"),
        (".env.example", "Exemple variables d'environnement"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Fichiers de configuration spécifiques
    config_files = [
        ("CabinetAvocat/settings.py", "Settings Django principal"),
        ("CabinetAvocat/settings_production.py", "Settings Django production"),
        ("CabinetAvocat/wsgi.py", "Configuration WSGI"),
        ("CabinetAvocat/urls.py", "URLs principales Django"),
    ]
    
    for filepath, description in config_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Répertoires importants
    directories_to_check = [
        ("static", "Répertoire fichiers statiques"),
        ("media", "Répertoire fichiers média"),
        ("templates", "Répertoire templates"),
        ("rapport", "Module rapport"),
        ("utils", "Module utils (JSReport)"),
    ]
    
    for dirpath, description in directories_to_check:
        if not check_directory_exists(dirpath, description):
            all_good = False
    
    # Vérifications spécifiques JSReport
    print("\n🔧 Vérifications JSReport:")
    
    jsreport_files = [
        ("utils/jsreport_service.py", "Service JSReport"),
    ]
    
    for filepath, description in jsreport_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Vérifier le contenu de requirements.txt
    print("\n📦 Vérification des dépendances:")
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            required_packages = [
                "Django",
                "gunicorn",
                "psycopg2-binary",
                "whitenoise",
                "dj-database-url",
                "python-decouple",
                "jsreport-python-client"
            ]
            
            for package in required_packages:
                if package.lower() in content.lower():
                    print(f"✅ Package {package} trouvé")
                else:
                    print(f"❌ Package {package} manquant")
                    all_good = False
    except FileNotFoundError:
        print("❌ Impossible de lire requirements.txt")
        all_good = False
    
    # Résumé
    print("\n" + "="*50)
    if all_good:
        print("🎉 TOUT EST PRÊT POUR LE DÉPLOIEMENT!")
        print("\n📋 Prochaines étapes:")
        print("1. Exécuter: git add .")
        print("2. Exécuter: git commit -m 'Ready for Railway deployment'")
        print("3. Exécuter: git push origin main")
        print("4. Configurer Railway avec les variables d'environnement")
        print("5. Vérifier la connexion à votre service JSReport")
        print("\n📖 Consultez README_RAILWAY.md pour les détails")
        return 0
    else:
        print("❌ PROBLÈMES DÉTECTÉS - Corrigez avant de déployer")
        print("\n🔧 Actions requises:")
        print("- Vérifiez les fichiers manquants ci-dessus")
        print("- Assurez-vous que tous les modules sont présents")
        print("- Vérifiez la configuration JSReport")
        return 1

if __name__ == "__main__":
    sys.exit(main())