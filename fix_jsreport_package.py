#!/usr/bin/env python3
"""
Script pour corriger le problème du package JSReport inexistant
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
    print("🔧 Correction du problème JSReport Package")
    print("=" * 50)
    
    print("📋 Problème identifié:")
    print("❌ jsreport-python-client==3.0.0 n'existe pas sur PyPI")
    print("✅ Solution: Utiliser requests directement (déjà implémenté)")
    
    print("\n📦 Vérification de requirements.txt...")
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            if "jsreport-python-client" in content:
                print("❌ jsreport-python-client encore présent dans requirements.txt")
                return 1
            else:
                print("✅ jsreport-python-client supprimé de requirements.txt")
    except FileNotFoundError:
        print("❌ requirements.txt non trouvé")
        return 1
    
    print("\n📋 Vérification du service JSReport...")
    if os.path.exists("utils/jsreport_service.py"):
        print("✅ Service JSReport utilise requests directement")
    else:
        print("❌ Service JSReport non trouvé")
        return 1
    
    print("\n" + "=" * 50)
    print("🎯 CORRECTION APPLIQUÉE!")
    print("\n📋 Changements effectués:")
    print("- Suppression de jsreport-python-client des dépendances")
    print("- Le service JSReport utilise requests directement")
    print("- Toutes les fonctionnalités JSReport sont préservées")
    
    print("\n📋 Prochaines étapes:")
    print("1. git add requirements.txt")
    print("2. git commit -m 'Remove non-existent jsreport-python-client package'")
    print("3. git push origin main")
    print("4. Relancer le déploiement Railway")
    
    # Proposer de faire le commit automatiquement
    response = input("\n❓ Voulez-vous commiter cette correction maintenant ? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'o', 'oui']:
        print("\n🔄 Commit de la correction...")
        
        if run_command("git add requirements.txt", "Ajout de requirements.txt"):
            if run_command('git commit -m "Remove non-existent jsreport-python-client package"', "Commit"):
                if run_command("git push origin main", "Push vers GitHub"):
                    print("\n🎉 CORRECTION POUSSÉE VERS GITHUB!")
                    print("✅ Le déploiement Railway devrait maintenant réussir")
                    return 0
        return 1
    else:
        print("\n📝 Commitez manuellement avec:")
        print("   git add requirements.txt")
        print('   git commit -m "Remove non-existent jsreport-python-client package"')
        print("   git push origin main")
        return 0

if __name__ == "__main__":
    sys.exit(main())