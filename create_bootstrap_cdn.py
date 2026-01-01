#!/usr/bin/env python
"""
Créer un fichier Bootstrap CSS avec CDN comme fallback
"""
from pathlib import Path

def create_bootstrap_css():
    """Créer un fichier Bootstrap CSS avec import CDN"""
    print("🎨 Création d'un Bootstrap CSS avec CDN...")
    
    staticfiles_path = Path('/app/staticfiles')
    
    # Créer le répertoire Bootstrap
    bootstrap_dir = staticfiles_path / 'assets' / 'vendor_components' / 'bootstrap' / 'dist' / 'css'
    bootstrap_dir.mkdir(parents=True, exist_ok=True)
    
    # Contenu Bootstrap avec import CDN
    bootstrap_content = '''
/* Bootstrap CSS pour Railway - Fallback CDN */
@import url('https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css');

/* Styles additionnels pour assurer la compatibilité */
.btn {
    display: inline-block;
    font-weight: 400;
    color: #212529;
    text-align: center;
    vertical-align: middle;
    cursor: pointer;
    background-color: transparent;
    border: 1px solid transparent;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    border-radius: 0.25rem;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.btn-primary {
    color: #fff;
    background-color: #007bff;
    border-color: #007bff;
}

.btn-primary:hover {
    color: #fff;
    background-color: #0069d9;
    border-color: #0062cc;
}

.form-control {
    display: block;
    width: 100%;
    height: calc(1.5em + 0.75rem + 2px);
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-group {
    margin-bottom: 1rem;
}

.container {
    width: 100%;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin-right: -15px;
    margin-left: -15px;
}

.col, .col-12, .col-md-6, .col-lg-4 {
    position: relative;
    width: 100%;
    padding-right: 15px;
    padding-left: 15px;
}

.card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 0.25rem;
}

.card-body {
    flex: 1 1 auto;
    min-height: 1px;
    padding: 1.25rem;
}
'''
    
    # Créer le fichier Bootstrap
    bootstrap_file = bootstrap_dir / 'bootstrap.css'
    with open(bootstrap_file, 'w', encoding='utf-8') as f:
        f.write(bootstrap_content)
    
    print(f"✅ Bootstrap CSS créé: {bootstrap_file}")
    
    # Créer aussi select2.css
    select2_dir = staticfiles_path / 'assets' / 'vendor_components' / 'select2' / 'dist' / 'css'
    select2_dir.mkdir(parents=True, exist_ok=True)
    
    select2_content = '''
/* Select2 CSS pour Railway - Fallback CDN */
@import url('https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css');

.select2-container {
    box-sizing: border-box;
    display: inline-block;
    margin: 0;
    position: relative;
    vertical-align: middle;
}

.select2-selection {
    background-color: #fff;
    border: 1px solid #aaa;
    border-radius: 4px;
}
'''
    
    select2_file = select2_dir / 'select2.min.css'
    with open(select2_file, 'w', encoding='utf-8') as f:
        f.write(select2_content)
    
    print(f"✅ Select2 CSS créé: {select2_file}")

def main():
    print("🎨 Création des CSS manquants avec CDN")
    print("=" * 40)
    
    create_bootstrap_css()
    
    print("\n✅ CSS créés avec succès!")

if __name__ == '__main__':
    main()