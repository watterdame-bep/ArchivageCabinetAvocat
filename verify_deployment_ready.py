#!/usr/bin/env python3
"""
Script de vérification finale avant déploiement Railway
Vérifie que tous les composants sont prêts pour le déploiement
"""

import os
import sys
import subprocess
import importlib.util

def check_file_exists(filepath, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MANQUANT: {filepath}")
        return False

def check_python_syntax(filepath):
    """Vérifie la syntaxe Python d'un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✅ Syntaxe Python valide: {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Erreur de syntaxe dans {filepath}: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de {filepath}: {e}")
        return False

def check_django_settings():
    """Vérifie que les settings Django se chargent correctement"""
    try:
        # Test avec manage.py check au lieu d'import direct
        result = subprocess.run([
            sys.executable, '-c', 
            'import CabinetAvocat.settings_production; print("Settings OK")'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Settings Django chargés avec succès")
            return True
        else:
            print(f"❌ Erreur lors du chargement des settings Django: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du chargement des settings Django: {e}")
        return False

def check_requirements():
    """Vérifie que requirements.txt contient les bonnes dépendances"""
    required_packages = [
        'Django==4.2.7',
        'PyMySQL==1.1.0',
        'whitenoise==6.6.0',
        'gunicorn==21.2.0',
        'dj-database-url==2.1.0',
        'python-decouple==3.8'
    ]
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing = []
        for package in required_packages:
            if package not in content:
                missing.append(package)
        
        if missing:
            print(f"❌ Packages manquants dans requirements.txt: {missing}")
            return False
        else:
            print("✅ Requirements.txt contient tous les packages nécessaires")
            return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de requirements.txt: {e}")
        return False

def check_collectstatic():
    """Teste collectstatic"""
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', 
            '--settings=CabinetAvocat.settings_production'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ collectstatic fonctionne correctement")
            return True
        else:
            print(f"❌ Erreur collectstatic: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test collectstatic: {e}")
        return False

def main():
    """Fonction principale de vérification"""
    print("🔍 Vérification de la préparation au déploiement Railway\n")
    
    all_checks_passed = True
    
    # Vérification des fichiers de configuration
    config_files = [
        ('requirements.txt', 'Fichier des dépendances Python'),
        ('railway.json', 'Configuration Railway'),
        ('Procfile', 'Fichier de démarrage'),
        ('nixpacks.toml', 'Configuration Nixpacks'),
        ('.env.example', 'Exemple de variables d\'environnement'),
        ('.gitattributes', 'Configuration Git pour l\'encodage'),
        ('CabinetAvocat/settings_production.py', 'Settings de production Django'),
    ]
    
    for filepath, description in config_files:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print()
    
    # Vérification de la syntaxe Python
    python_files = [
        'CabinetAvocat/settings_production.py',
        'manage.py'
    ]
    
    for filepath in python_files:
        if os.path.exists(filepath):
            if not check_python_syntax(filepath):
                all_checks_passed = False
    
    print()
    
    # Vérification des requirements
    if not check_requirements():
        all_checks_passed = False
    
    print()
    
    # Vérification des settings Django
    if not check_django_settings():
        all_checks_passed = False
    
    print()
    
    # Test collectstatic
    if not check_collectstatic():
        all_checks_passed = False
    
    print()
    
    # Vérification des templates JSReport
    jsreport_templates = [
        'templates_jsreport/rapport_agent.html',
        'templates_jsreport/rapport_client.html',
        'templates_jsreport/rapport_juridiction.html',
        'templates_jsreport/rapport_commune.html',
        'templates_jsreport/rapport_dossier.html',
        'templates_jsreport/rapport_activites_internes.html',
        'templates_jsreport/facture_paiement.html',
        'templates_jsreport/Facture_dossier.html',
        'templates_jsreport/Extrait_de_compte_client.html',
    ]
    
    jsreport_ready = True
    for template in jsreport_templates:
        if not check_file_exists(template, f'Template JSReport'):
            jsreport_ready = False
    
    if jsreport_ready:
        print("✅ Tous les templates JSReport sont présents")
    else:
        print("⚠️  Certains templates JSReport sont manquants (à remplir manuellement)")
    
    print("\n" + "="*60)
    
    if all_checks_passed:
        print("🎉 SUCCÈS: Tous les contrôles sont passés!")
        print("✅ Votre application est prête pour le déploiement Railway")
        print("\n📋 Étapes suivantes:")
        print("1. Créer un projet Railway depuis votre repo GitHub")
        print("2. Ajouter un service MySQL Railway")
        print("3. Configurer les variables d'environnement (voir .env.example)")
        print("4. Déployer!")
        print("5. Après déploiement: uploader les templates JSReport avec scripts/upload_jsreport_templates.py")
        return True
    else:
        print("❌ ÉCHEC: Certains contrôles ont échoué")
        print("🔧 Veuillez corriger les erreurs ci-dessus avant de déployer")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)