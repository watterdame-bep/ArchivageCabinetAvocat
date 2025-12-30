#!/usr/bin/env python3
"""
Script pour commiter les corrections d'encodage et préparer le redéploiement
"""

import os
import sys
import subprocess

def run_git_command(command, description):
    """Exécuter une commande Git"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {str(e)}")
        return False

def main():
    print("🛠️  Commit des corrections d'encodage UTF-8")
    print("=" * 50)
    
    # Vérifier le statut Git
    print("📋 Vérification du statut Git...")
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        if result.stdout.strip():
            print("📝 Fichiers modifiés détectés:")
            modified_files = result.stdout.strip().split('\n')
            for file in modified_files[:10]:  # Afficher les 10 premiers
                print(f"   {file}")
            if len(modified_files) > 10:
                print(f"   ... et {len(modified_files) - 10} autres fichiers")
        else:
            print("✅ Aucune modification en attente")
            return 0
    
    # Ajouter tous les fichiers
    if not run_git_command("git add .", "Ajout des fichiers modifiés"):
        return 1
    
    # Commit avec message descriptif
    commit_message = "Fix UTF-8 encoding issues for Railway deployment\n\n- Fixed WeatherIcon.js encoding problems\n- Converted 63+ files from various encodings to UTF-8\n- Added .gitattributes to prevent future encoding issues\n- Ready for Railway deployment"
    
    if not run_git_command(f'git commit -m "{commit_message}"', "Commit des corrections"):
        return 1
    
    # Proposer le push
    print("\n" + "=" * 50)
    print("✅ CORRECTIONS COMMITÉES AVEC SUCCÈS!")
    
    response = input("\n❓ Voulez-vous pousser vers GitHub maintenant ? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'o', 'oui']:
        if run_git_command("git push origin main", "Push vers GitHub"):
            print("\n🎉 CORRECTIONS POUSSÉES VERS GITHUB!")
            print("\n📋 Prochaines étapes:")
            print("1. Aller sur Railway")
            print("2. Relancer le déploiement (il devrait maintenant réussir)")
            print("3. Vérifier que l'application démarre correctement")
            print("4. Configurer les variables d'environnement si nécessaire")
            print("5. Uploader les templates JSReport")
            return 0
        else:
            return 1
    else:
        print("\n📝 Push manuel requis:")
        print("   git push origin main")
        print("\n📋 Puis relancez le déploiement Railway")
        return 0

if __name__ == "__main__":
    sys.exit(main())