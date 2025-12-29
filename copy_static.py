#!/usr/bin/env python
"""
Script pour copier manuellement les fichiers statiques sur Railway
"""
import os
import shutil
from pathlib import Path

def copy_static_files():
    """Copie les fichiers statiques depuis staticfiles vers le dossier servi par Whitenoise"""
    
    # Chemins
    base_dir = Path(__file__).resolve().parent
    staticfiles_dir = base_dir / 'staticfiles'
    
    print(f"📁 BASE_DIR: {base_dir}")
    print(f"📁 STATICFILES_DIR: {staticfiles_dir}")
    
    # Vérifier si staticfiles existe
    if staticfiles_dir.exists():
        files_count = len(list(staticfiles_dir.rglob('*')))
        print(f"✅ Dossier staticfiles trouvé avec {files_count} fichiers")
        return True
    else:
        print("❌ Dossier staticfiles non trouvé")
        return False

if __name__ == "__main__":
    copy_static_files()