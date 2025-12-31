#!/usr/bin/env python3
"""
Vérification finale de la configuration de déploiement
"""

import os
from pathlib import Path

def check_files():
    """Vérifie que tous les fichiers nécessaires sont présents"""
    print("🔍 Vérification des fichiers de déploiement...")
    
    required_files = [
        'Procfile',
        'requirements.txt',
        'CabinetAvocat/settings_production.py',
        '.env.example'
    ]
    
    forbidden_files = [
        'nixpacks.toml',
        'railway.json',
        'runtime.txt',
        'build_railway.sh',
        'railway_simple.json',
        'Dockerfile'
    ]
    
    # Vérifier les fichiers requis
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MANQUANT")
            return False
    
    # Vérifier l'absence de fichiers problématiques
    for file_path in forbidden_files:
        if Path(file_path).exists():
            print(f"⚠️  {file_path} - DEVRAIT ÊTRE SUPPRIMÉ")
        else:
            print(f"✅ {file_path} - Absent (bon)")
    
    return True

def check_procfile():
    """Vérifie le contenu du Procfile"""
    print("\n🔍 Vérification du Procfile...")
    
    try:
        with open('Procfile', 'r') as f:
            content = f.read()
        
        if 'web:' in content and 'gunicorn' in content:
            print("✅ Procfile contient la commande web")
        else:
            print("❌ Procfile incorrect")
            return False
        
        if 'release:' in content:
            print("✅ Procfile contient la commande release")
        else:
            print("⚠️  Pas de commande release (optionnel)")
        
        return True
    except FileNotFoundError:
        print("❌ Procfile non trouvé")
        return False

def check_requirements():
    """Vérifie le requirements.txt"""
    print("\n🔍 Vérification du requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        essential_packages = ['Django', 'gunicorn', 'whitenoise', 'PyMySQL']
        
        for package in essential_packages:
            if package in content:
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - MANQUANT")
                return False
        
        return True
    except FileNotFoundError:
        print("❌ requirements.txt non trouvé")
        return False

def main():
    """Fonction principale"""
    print("🚀 Vérification de la Configuration Railway Ultra-Simple")
    print("=" * 60)
    
    checks = [
        check_files(),
        check_procfile(),
        check_requirements()
    ]
    
    print("=" * 60)
    
    if all(checks):
        print("✅ Configuration prête pour Railway !")
        print("📋 Prochaines étapes :")
        print("   1. railway login")
        print("   2. railway link")
        print("   3. railway up")
    else:
        print("❌ Configuration incomplète")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())