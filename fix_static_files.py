#!/usr/bin/env python
"""
Script pour corriger les fichiers statiques manquants
"""
import os
import shutil
from pathlib import Path

def copy_missing_files():
    """Copier manuellement les fichiers critiques manquants"""
    print("🔧 Correction des fichiers statiques manquants...")
    
    # Chemins de base
    static_root = Path('/app/staticfiles')
    static_source = Path('/app/static')
    
    # Fichiers critiques à copier
    critical_files = [
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'assets/vendor_components/bootstrap/dist/css/bootstrap.min.css',
        'assets/vendor_components/select2/dist/css/select2.min.css',
        'assets/vendor_components/OwlCarousel2/dist/assets/owl.carousel.css',
        'assets/vendor_components/OwlCarousel2/dist/assets/owl.theme.default.min.css',
        'assets/vendor_components/Magnific-Popup-master/dist/magnific-popup.css',
        'assets/vendor_components/lightbox-master/dist/ekko-lightbox.css',
        'assets/vendor_components/bootstrap-colorpicker/dist/css/bootstrap-colorpicker.min.css',
        'assets/vendor_components/bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css',
        'assets/vendor_components/bootstrap-tagsinput/dist/bootstrap-tagsinput.css',
        'assets/vendor_components/bootstrap-select/dist/css/bootstrap-select.css',
        'assets/vendor_components/x-editable/dist/bootstrap3-editable/css/bootstrap-editable.css',
    ]
    
    copied_count = 0
    
    for file_path in critical_files:
        source_file = static_source / file_path
        dest_file = static_root / file_path
        
        if source_file.exists():
            # Créer le répertoire de destination si nécessaire
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(source_file, dest_file)
                print(f"✅ Copié: {file_path}")
                copied_count += 1
            except Exception as e:
                print(f"❌ Erreur copie {file_path}: {e}")
        else:
            print(f"⚠️ Source manquante: {file_path}")
    
    print(f"📊 {copied_count} fichiers copiés")
    
    # Vérifier Bootstrap après copie
    bootstrap_css = static_root / 'assets/vendor_components/bootstrap/dist/css/bootstrap.css'
    if bootstrap_css.exists():
        print("✅ Bootstrap CSS maintenant disponible!")
    else:
        print("❌ Bootstrap CSS toujours manquant")

def copy_entire_vendor_components():
    """Copier tout le dossier vendor_components si nécessaire"""
    print("🔄 Copie complète du dossier vendor_components...")
    
    static_root = Path('/app/staticfiles')
    static_source = Path('/app/static')
    
    source_vendor = static_source / 'assets/vendor_components'
    dest_vendor = static_root / 'assets/vendor_components'
    
    if source_vendor.exists():
        try:
            if dest_vendor.exists():
                shutil.rmtree(dest_vendor)
            
            shutil.copytree(source_vendor, dest_vendor)
            print("✅ Dossier vendor_components copié complètement")
            
            # Vérifier Bootstrap
            bootstrap_css = dest_vendor / 'bootstrap/dist/css/bootstrap.css'
            if bootstrap_css.exists():
                print("✅ Bootstrap CSS maintenant disponible!")
            else:
                print("❌ Bootstrap CSS toujours manquant après copie complète")
                
        except Exception as e:
            print(f"❌ Erreur copie complète: {e}")
    else:
        print("❌ Dossier source vendor_components introuvable")

def main():
    print("🔧 Correction des fichiers statiques Railway")
    print("=" * 50)
    
    # Essayer d'abord la copie sélective
    copy_missing_files()
    
    # Si Bootstrap n'est toujours pas là, copie complète
    bootstrap_css = Path('/app/staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css')
    if not bootstrap_css.exists():
        print("\n🔄 Bootstrap toujours manquant, copie complète...")
        copy_entire_vendor_components()
    
    print("\n✅ Correction terminée!")

if __name__ == '__main__':
    main()