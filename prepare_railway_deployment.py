#!/usr/bin/env python3
"""
Script de préparation finale pour le déploiement Railway
Vérifie tout et prépare le commit Git
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Exécuter une commande et afficher le résultat"""
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

def check_jsreport_templates():
    """Vérifier que tous les templates JSReport sont présents"""
    print("\n📄 Vérification des templates JSReport:")
    
    templates_dir = Path("templates_jsreport")
    if not templates_dir.exists():
        print("❌ Dossier templates_jsreport manquant")
        return False
    
    expected_templates = [
        "rapport_agent",
        "rapport_client", 
        "rapport_juridiction",
        "rapport_commune",
        "rapport_dossier",
        "rapport_activite",
        "Facture_paiement_client",
        "Facture_dossier",
        "Extrait_de_compte_client"
    ]
    
    all_present = True
    for template in expected_templates:
        html_file = templates_dir / f"{template}.html"
        json_file = templates_dir / f"{template}.json"
        
        if html_file.exists() and json_file.exists():
            print(f"✅ Template {template} complet (.html + .json)")
        else:
            print(f"❌ Template {template} incomplet")
            if not html_file.exists():
                print(f"   Manque: {html_file}")
            if not json_file.exists():
                print(f"   Manque: {json_file}")
            all_present = False
    
    return all_present

def check_git_status():
    """Vérifier le statut Git"""
    print("\n📋 Vérification Git:")
    
    # Vérifier si on est dans un repo Git
    if not os.path.exists(".git"):
        print("❌ Pas de repository Git détecté")
        print("   Initialisez avec: git init")
        return False
    
    # Vérifier les fichiers modifiés
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        if result.stdout.strip():
            print("📝 Fichiers modifiés détectés:")
            print(result.stdout)
            return True
        else:
            print("✅ Aucune modification en attente")
            return True
    else:
        print("❌ Erreur lors de la vérification Git")
        return False

def main():
    print("🚀 Préparation du déploiement Railway")
    print("=" * 50)
    
    # Vérification générale
    print("🔍 Exécution du script de vérification...")
    if not run_command("python check_deployment.py", "Vérification générale"):
        print("❌ La vérification générale a échoué")
        return 1
    
    # Vérification des templates JSReport
    if not check_jsreport_templates():
        print("❌ Problème avec les templates JSReport")
        return 1
    
    # Vérification Git
    if not check_git_status():
        print("❌ Problème avec Git")
        return 1
    
    # Proposer les commandes Git
    print("\n" + "=" * 50)
    print("🎉 TOUT EST PRÊT POUR LE DÉPLOIEMENT!")
    print("\n📋 Commandes à exécuter pour déployer:")
    print("1️⃣  git add .")
    print("2️⃣  git commit -m 'Ready for Railway deployment with MySQL + JSReport'")
    print("3️⃣  git push origin main")
    
    # Demander si on veut exécuter automatiquement
    response = input("\n❓ Voulez-vous exécuter ces commandes automatiquement ? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'o', 'oui']:
        print("\n🔄 Exécution des commandes Git...")
        
        # Git add
        if run_command("git add .", "Ajout des fichiers"):
            # Git commit
            if run_command('git commit -m "Ready for Railway deployment with MySQL + JSReport"', "Commit"):
                # Git push
                if run_command("git push origin main", "Push vers GitHub"):
                    print("\n🎉 DÉPLOIEMENT PRÉPARÉ AVEC SUCCÈS!")
                    print("\n📋 Prochaines étapes sur Railway:")
                    print("1. Créer un nouveau projet depuis GitHub")
                    print("2. Ajouter le service MySQL Railway")
                    print("3. Configurer les variables d'environnement (voir .env.example)")
                    print("4. Déployer l'application")
                    print("5. Uploader les templates JSReport avec le script")
                    print("\n📖 Consultez DEPLOYMENT_MYSQL_CORRECTED.md pour les détails")
                    return 0
                else:
                    print("❌ Erreur lors du push")
                    return 1
            else:
                print("❌ Erreur lors du commit")
                return 1
        else:
            print("❌ Erreur lors de l'ajout des fichiers")
            return 1
    else:
        print("\n📝 Exécutez manuellement les commandes ci-dessus")
        print("📖 Consultez DEPLOYMENT_MYSQL_CORRECTED.md pour les détails")
        return 0

if __name__ == "__main__":
    sys.exit(main())