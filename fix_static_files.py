#!/usr/bin/env python
"""
Script pour corriger les fichiers statiques manquants
"""
import os
import shutil
from pathlib import Path

def find_bootstrap_files():
    """Chercher où sont les fichiers Bootstrap dans le conteneur"""
    print("🔍 Recherche des fichiers Bootstrap...")
    
    search_paths = [
        '/app/static',
        '/app',
        '/usr/local/lib/python3.11/site-packages',
    ]
    
    for search_path in search_paths:
        print(f"\n📁 Recherche dans {search_path}...")
        try:
            for root, dirs, files in os.walk(search_path):
                if 'bootstrap.css' in files:
                    print(f"✅ Trouvé: {root}/bootstrap.css")
                if 'bootstrap' in dirs:
                    bootstrap_path = os.path.join(root, 'bootstrap')
                    print(f"📁 Dossier Bootstrap: {bootstrap_path}")
                    
                    # Vérifier le contenu
                    css_path = os.path.join(bootstrap_path, 'dist', 'css')
                    if os.path.exists(css_path):
                        css_files = os.listdir(css_path)
                        print(f"   CSS files: {css_files}")
        except Exception as e:
            print(f"❌ Erreur recherche dans {search_path}: {e}")

def list_static_directory():
    """Lister le contenu du répertoire static"""
    print("\n📁 Contenu de /app/static:")
    static_path = Path('/app/static')
    
    if static_path.exists():
        for item in static_path.rglob('*bootstrap*'):
            print(f"🔍 Bootstrap trouvé: {item}")
        
        # Lister assets/vendor_components
        vendor_path = static_path / 'assets' / 'vendor_components'
        if vendor_path.exists():
            print(f"\n📁 Contenu de {vendor_path}:")
            for item in sorted(vendor_path.iterdir())[:20]:
                print(f"  {item.name}")
        else:
            print(f"❌ {vendor_path} n'existe pas")
    else:
        print("❌ /app/static n'existe pas")

def copy_from_correct_location():
    """Copier depuis la bonne localisation"""
    print("\n🔧 Tentative de copie depuis la localisation correcte...")
    
    # Chercher Bootstrap dans le répertoire static
    static_path = Path('/app/static')
    staticfiles_path = Path('/app/staticfiles')
    
    # Chercher tous les fichiers bootstrap.css
    bootstrap_files = list(static_path.rglob('bootstrap.css'))
    
    for bootstrap_file in bootstrap_files:
        print(f"📁 Bootstrap trouvé: {bootstrap_file}")
        
        # Calculer le chemin relatif depuis static
        try:
            rel_path = bootstrap_file.relative_to(static_path)
            dest_path = staticfiles_path / rel_path
            
            # Créer le répertoire de destination
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copier le fichier
            shutil.copy2(bootstrap_file, dest_path)
            print(f"✅ Copié vers: {dest_path}")
            
        except Exception as e:
            print(f"❌ Erreur copie: {e}")

def main():
    print("🔧 Diagnostic et correction des fichiers statiques")
    print("=" * 60)
    
    find_bootstrap_files()
    list_static_directory()
    copy_from_correct_location()
    
    # Vérifier le résultat
    bootstrap_css = Path('/app/staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css')
    if bootstrap_css.exists():
        print("\n✅ Bootstrap CSS maintenant disponible!")
    else:
        print("\n❌ Bootstrap CSS toujours manquant")
        
        # Essayer une copie alternative
        print("🔄 Tentative de copie alternative...")
        staticfiles_path = Path('/app/staticfiles')
        
        # Créer le répertoire Bootstrap manuellement
        bootstrap_dir = staticfiles_path / 'assets' / 'vendor_components' / 'bootstrap' / 'dist' / 'css'
        bootstrap_dir.mkdir(parents=True, exist_ok=True)
        
        # Créer un fichier Bootstrap minimal
        bootstrap_content = """
/* Bootstrap CSS minimal pour Railway */
.btn { 
    padding: 6px 12px; 
    margin-bottom: 0; 
    font-size: 14px; 
    font-weight: normal; 
    line-height: 1.42857143; 
    text-align: center; 
    white-space: nowrap; 
    vertical-align: middle; 
    cursor: pointer; 
    border: 1px solid transparent; 
    border-radius: 4px; 
}
.btn-primary { 
    color: #fff; 
    background-color: #337ab7; 
    border-color: #2e6da4; 
}
.form-control { 
    display: block; 
    width: 100%; 
    height: 34px; 
    padding: 6px 12px; 
    font-size: 14px; 
    line-height: 1.42857143; 
    color: #555; 
    background-color: #fff; 
    border: 1px solid #ccc; 
    border-radius: 4px; 
}
"""
        
        bootstrap_file = bootstrap_dir / 'bootstrap.css'
        with open(bootstrap_file, 'w') as f:
            f.write(bootstrap_content)
        
        print(f"✅ Bootstrap CSS minimal créé: {bootstrap_file}")

if __name__ == '__main__':
    main()