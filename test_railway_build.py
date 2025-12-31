#!/usr/bin/env python3
"""
Script pour simuler le build Railway localement
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 {description}...")
    print(f"Commande: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - Succès")
        if result.stdout:
            print(f"Output: {result.stdout[:200]}...")
    else:
        print(f"❌ {description} - Erreur")
        print(f"Error: {result.stderr}")
        return False
    
    return True

def main():
    """Simule le processus de build Railway"""
    print("🚀 Test du build Railway localement")
    print("=" * 50)
    
    # Définir les variables d'environnement
    os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
    
    # Étapes du build
    steps = [
        ("pip install --upgrade pip", "Mise à jour pip"),
        ("pip install -r requirements.txt", "Installation des dépendances"),
        ("python manage.py collectstatic --noinput --settings=CabinetAvocat.settings_production", "Collection des fichiers statiques"),
        ("python manage.py check --settings=CabinetAvocat.settings_production", "Vérification Django")
    ]
    
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"❌ Échec à l'étape: {desc}")
            sys.exit(1)
    
    print("=" * 50)
    print("✅ Simulation du build Railway réussie !")
    print("🚀 Prêt pour le déploiement sur Railway")

if __name__ == "__main__":
    main()