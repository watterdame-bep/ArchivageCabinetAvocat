#!/usr/bin/env python3
"""
Script pour nettoyer les anciens fichiers de déploiement
"""

import os
import shutil
from pathlib import Path

def clean_old_files():
    """Nettoie les anciens fichiers de déploiement"""
    print("🧹 Nettoyage des anciens fichiers de déploiement...")
    
    # Fichiers à supprimer s'ils existent
    files_to_remove = [
        'railway_simple.json',
        'build_railway.sh',
        'CabinetAvocat/settings_production.py.backup'
    ]
    
    # Dossiers à nettoyer
    dirs_to_clean = [
        'staticfiles'
    ]
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ Supprimé: {file_path}")
    
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"✅ Nettoyé: {dir_path}")
    
    print("✅ Nettoyage terminé")

def main():
    """Fonction principale"""
    print("🚀 Nettoyage pour nouveau déploiement Railway")
    clean_old_files()

if __name__ == "__main__":
    main()