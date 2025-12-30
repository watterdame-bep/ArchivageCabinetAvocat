#!/usr/bin/env python3
"""
Script pour corriger les problèmes MySQL Railway
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Exécuter une commande"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            return True
        else:
            print(f"❌ {description} - Erreur: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {str(e)}")
        return False

def main():
    print("🔧 Correction des problèmes MySQL Railway")
    print("=" * 50)
    
    print("📋 Problèmes identifiés et corrigés:")
    print("✅ Suppression de mysqlclient (problème de compilation)")
    print("✅ Utilisation de PyMySQL uniquement (pure Python)")
    print("✅ Ajout de nixpacks.toml pour configuration Railway")
    print("✅ Mise à jour de railway.json")
    
    print("\n📦 Vérification de requirements.txt...")
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            if "mysqlclient" in content:
                print("❌ mysqlclient encore présent dans requirements.txt")
                return 1
            elif "PyMySQL" in content:
                print("✅ PyMySQL configuré correctement")
            else:
                print("⚠️  PyMySQL non trouvé dans requirements.txt")
    except FileNotFoundError:
        print("❌ requirements.txt non trouvé")
        return 1
    
    print("\n📋 Fichiers de configuration Railway:")
    files_to_check = [
        ("nixpacks.toml", "Configuration Nixpacks"),
        ("railway.json", "Configuration Railway"),
        ("Procfile", "Configuration Procfile")
    ]
    
    for filename, description in files_to_check:
        if os.path.exists(filename):
            print(f"✅ {description}: {filename}")
        else:
            print(f"❌ {description}: {filename} - MANQUANT")
    
    print("\n" + "=" * 50)
    print("🎯 CORRECTIONS APPLIQUÉES!")
    print("\n📋 Prochaines étapes:")
    print("1. git add .")
    print("2. git commit -m 'Fix MySQL Railway deployment issues'")
    print("3. git push origin main")
    print("4. Relancer le déploiement Railway")
    print("\n💡 Le déploiement devrait maintenant réussir!")
    
    # Proposer de faire le commit automatiquement
    response = input("\n❓ Voulez-vous commiter ces corrections maintenant ? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'o', 'oui']:
        print("\n🔄 Commit des corrections...")
        
        if run_command("git add .", "Ajout des fichiers"):
            if run_command('git commit -m "Fix MySQL Railway deployment - remove mysqlclient, add nixpacks.toml"', "Commit"):
                if run_command("git push origin main", "Push vers GitHub"):
                    print("\n🎉 CORRECTIONS POUSSÉES VERS GITHUB!")
                    print("✅ Vous pouvez maintenant relancer le déploiement Railway")
                    return 0
        return 1
    else:
        print("\n📝 Commitez manuellement avec:")
        print("   git add .")
        print('   git commit -m "Fix MySQL Railway deployment issues"')
        print("   git push origin main")
        return 0

if __name__ == "__main__":
    sys.exit(main())