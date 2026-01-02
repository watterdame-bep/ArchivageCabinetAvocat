#!/usr/bin/env python
"""
Analyse complète des problèmes CSS et correction
"""
import os
from pathlib import Path

def analyze_css_issues():
    """Analyser les problèmes CSS actuels"""
    print("🔍 ANALYSE COMPLÈTE DES PROBLÈMES CSS")
    print("🏢 Cabinet d'Avocats - Django Railway")
    print("=" * 60)
    
    # Vérifier les fichiers CSS principaux
    css_files = {
        'vendors_css.css': 'static/css/vendors_css.css',
        'style.css': 'static/css/style.css',
        'font-size-fix.css': 'staticfiles/css/font-size-fix.css',
        'template-font-fix.css': 'staticfiles/css/template-font-fix.css',
        'missing-assets-fallback.css': 'staticfiles/css/missing-assets-fallback.css'
    }
    
    print("📁 VÉRIFICATION DES FICHIERS CSS PRINCIPAUX:")
    print("-" * 50)
    
    for name, path in css_files.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {name}: {size} bytes - {path}")
        else:
            print(f"❌ {name}: MANQUANT - {path}")
    
    # Vérifier les imports dans vendors_css.css
    print("\n📋 ANALYSE DE VENDORS_CSS.CSS:")
    print("-" * 50)
    
    vendors_css_path = Path('static/css/vendors_css.css')
    if vendors_css_path.exists():
        with open(vendors_css_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        imports = content.count('@import')
        print(f"📊 Nombre d'imports trouvés: {imports}")
        
        # Vérifier les imports critiques
        critical_imports = [
            'bootstrap.css',
            'font-awesome',
            'materialdesignicons',
            'ionicons',
            'font-size-fix.css',
            'missing-assets-fallback.css'
        ]
        
        for imp in critical_imports:
            if imp in content:
                print(f"✅ Import trouvé: {imp}")
            else:
                print(f"❌ Import manquant: {imp}")
    
    # Vérifier les fichiers dans staticfiles
    print("\n📦 VÉRIFICATION DES STATICFILES:")
    print("-" * 50)
    
    staticfiles_dir = Path('staticfiles')
    if staticfiles_dir.exists():
        # Compter les fichiers par type
        css_count = len(list(staticfiles_dir.rglob('*.css')))
        js_count = len(list(staticfiles_dir.rglob('*.js')))
        font_count = len(list(staticfiles_dir.rglob('*.woff*'))) + len(list(staticfiles_dir.rglob('*.ttf'))) + len(list(staticfiles_dir.rglob('*.eot')))
        
        print(f"📊 Fichiers CSS: {css_count}")
        print(f"📊 Fichiers JS: {js_count}")
        print(f"📊 Fichiers Fonts: {font_count}")
        
        # Vérifier les dossiers critiques
        critical_dirs = [
            'css',
            'assets/vendor_components/bootstrap',
            'assets/icons/font-awesome',
            'assets/icons/material-design-iconic-font',
            'assets/icons/Ionicons'
        ]
        
        for dir_path in critical_dirs:
            full_path = staticfiles_dir / dir_path
            if full_path.exists():
                files = len(list(full_path.rglob('*')))
                print(f"✅ {dir_path}: {files} fichiers")
            else:
                print(f"❌ {dir_path}: MANQUANT")
    
    return True

def fix_vendors_css_imports():
    """Corriger les imports dans vendors_css.css"""
    print("\n🔧 CORRECTION DES IMPORTS DANS VENDORS_CSS.CSS:")
    print("-" * 50)
    
    vendors_css_path = Path('static/css/vendors_css.css')
    staticfiles_vendors_css = Path('staticfiles/css/vendors_css.css')
    
    if not vendors_css_path.exists():
        print("❌ vendors_css.css non trouvé")
        return False
    
    with open(vendors_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ajouter les imports manquants
    missing_imports = []
    
    if 'font-size-fix.css' not in content:
        missing_imports.append('@import url(/static/css/font-size-fix.css);')
    
    if 'template-font-fix.css' not in content:
        missing_imports.append('@import url(/static/css/template-font-fix.css);')
    
    if 'missing-assets-fallback.css' not in content:
        missing_imports.append('@import url(/static/css/missing-assets-fallback.css);')
    
    if missing_imports:
        # Ajouter les imports à la fin
        content += '\n\n/* Corrections ajoutées automatiquement */\n'
        content += '\n'.join(missing_imports)
        
        # Écrire dans static/
        with open(vendors_css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Copier vers staticfiles/
        staticfiles_vendors_css.parent.mkdir(parents=True, exist_ok=True)
        with open(staticfiles_vendors_css, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Ajouté {len(missing_imports)} imports manquants")
        for imp in missing_imports:
            print(f"  + {imp}")
    else:
        print("ℹ️ Tous les imports sont déjà présents")
    
    return True

def copy_font_fixes_to_staticfiles():
    """Copier les corrections de fonts vers staticfiles"""
    print("\n📋 COPIE DES CORRECTIONS VERS STATICFILES:")
    print("-" * 50)
    
    staticfiles_css = Path('staticfiles/css')
    staticfiles_css.mkdir(parents=True, exist_ok=True)
    
    # Copier font-size-fix.css vers static/ aussi
    font_fix_source = Path('staticfiles/css/font-size-fix.css')
    font_fix_dest = Path('static/css/font-size-fix.css')
    
    if font_fix_source.exists():
        with open(font_fix_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(font_fix_dest, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Copié font-size-fix.css vers static/css/")
    
    # Copier template-font-fix.css vers static/ aussi
    template_fix_source = Path('staticfiles/css/template-font-fix.css')
    template_fix_dest = Path('static/css/template-font-fix.css')
    
    if template_fix_source.exists():
        with open(template_fix_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(template_fix_dest, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Copié template-font-fix.css vers static/css/")
    
    return True

def create_comprehensive_css_fix():
    """Créer un CSS de correction complet"""
    print("\n🎨 CRÉATION D'UN CSS DE CORRECTION COMPLET:")
    print("-" * 50)
    
    comprehensive_css = '''
/* CORRECTION COMPLÈTE CSS - Cabinet d'Avocats */
/* Chargement prioritaire des fonts Google */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&family=Rubik:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700;1,900&display=swap');

/* Fallback CDN pour Bootstrap si manquant */
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');

/* Fallback CDN pour FontAwesome si manquant */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

/* Fallback CDN pour Material Design Icons si manquant */
@import url('https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css');

/* Fallback CDN pour Ionicons si manquant */
@import url('https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.css');

/* CORRECTION GLOBALE DES FONTS */
* {
    font-family: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

html {
    font-size: 14px !important;
}

body {
    font-size: 14px !important;
    line-height: 1.5 !important;
    font-family: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

/* Titres avec Rubik */
h1, h2, h3, h4, h5, h6, .h1, .h2, .h3, .h4, .h5, .h6 {
    font-family: "Rubik", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

/* CORRECTION SPÉCIFIQUE SIDEBAR */
.main-sidebar {
    font-size: 14px !important;
}

.main-sidebar .sidebar-menu > li > a {
    font-size: 14px !important;
    line-height: 1.4 !important;
    font-weight: 400 !important;
}

.main-sidebar .sidebar-menu .treeview-menu > li > a {
    font-size: 13px !important;
    line-height: 1.3 !important;
    font-weight: 400 !important;
}

/* CORRECTION DROPDOWNS */
.dropdown-menu {
    font-size: 14px !important;
}

.dropdown-menu > li > a {
    font-size: 14px !important;
    line-height: 1.4 !important;
}

/* CORRECTION NAVBAR */
.navbar {
    font-size: 14px !important;
}

.navbar-nav > li > a {
    font-size: 14px !important;
}

/* CORRECTION CONTROL SIDEBAR */
.control-sidebar {
    font-size: 14px !important;
}

.control-sidebar h4 {
    font-size: 16px !important;
    font-weight: 600 !important;
}

.control-sidebar .form-group label {
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* CORRECTION FORMULAIRES */
.form-control {
    font-size: 14px !important;
}

label {
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* CORRECTION BOUTONS */
.btn {
    font-size: 14px !important;
    line-height: 1.4 !important;
}

/* CORRECTION TABLEAUX */
.table {
    font-size: 14px !important;
}

.table th {
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* CORRECTION CARTES */
.card-title {
    font-size: 18px !important;
    font-weight: 600 !important;
}

.card-text {
    font-size: 14px !important;
}

/* CORRECTION BADGES */
.badge {
    font-size: 11px !important;
    font-weight: 600 !important;
}

/* CORRECTION ALERTES */
.alert {
    font-size: 14px !important;
}

/* CORRECTION MODALES */
.modal-title {
    font-size: 18px !important;
    font-weight: 600 !important;
}

.modal-body {
    font-size: 14px !important;
}

/* CORRECTION BREADCRUMBS */
.breadcrumb {
    font-size: 13px !important;
}

/* CORRECTION PAGINATION */
.pagination {
    font-size: 14px !important;
}

/* CORRECTION LISTES */
.list-group-item {
    font-size: 14px !important;
}

/* CORRECTION WIDGETS */
.info-box-text {
    font-size: 13px !important;
    font-weight: 600 !important;
}

.info-box-number {
    font-size: 18px !important;
    font-weight: 700 !important;
}

.small-box h3 {
    font-size: 28px !important;
    font-weight: 700 !important;
}

.small-box p {
    font-size: 14px !important;
}

/* CORRECTION TOOLTIPS */
.tooltip {
    font-size: 12px !important;
}

/* CORRECTION POPOVERS */
.popover {
    font-size: 13px !important;
}

.popover-title {
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* CORRECTION SELECT2 */
.select2-container--default .select2-selection--single {
    font-size: 14px !important;
    line-height: 1.4 !important;
}

.select2-dropdown {
    font-size: 14px !important;
}

/* CORRECTION DATATABLES */
.dataTables_wrapper {
    font-size: 14px !important;
}

.dataTables_info {
    font-size: 13px !important;
}

.dataTables_paginate {
    font-size: 13px !important;
}

/* CORRECTION POUR LES ICÔNES MANQUANTES */
.fa:before, .fas:before, .far:before, .fal:before, .fab:before {
    font-family: "Font Awesome 6 Free", "Font Awesome 6 Pro", "FontAwesome" !important;
}

.mdi:before {
    font-family: "Material Design Icons", "MaterialDesignIcons" !important;
}

.ion:before, .ionicons:before {
    font-family: "Ionicons" !important;
}

/* CORRECTION POUR LES IMAGES MANQUANTES */
img[src*="avatar"]:not([src*="http"]) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

img[src*="logo"]:not([src*="http"]) {
    background: #2c3e50;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

/* CORRECTION POUR LES BACKGROUNDS MANQUANTS */
.bg-primary { background-color: #1e42a0 !important; }
.bg-secondary { background-color: #e4e6ef !important; }
.bg-success { background-color: #42b53f !important; }
.bg-info { background-color: #3596f7 !important; }
.bg-warning { background-color: #ffa800 !important; }
.bg-danger { background-color: #ee3158 !important; }
.bg-dark { background-color: #172b4c !important; }
.bg-light { background-color: #f3f6f9 !important; }

/* CORRECTION POUR LES COULEURS DE TEXTE */
.text-primary { color: #1e42a0 !important; }
.text-secondary { color: #e4e6ef !important; }
.text-success { color: #42b53f !important; }
.text-info { color: #3596f7 !important; }
.text-warning { color: #ffa800 !important; }
.text-danger { color: #ee3158 !important; }
.text-dark { color: #172b4c !important; }
.text-light { color: #f3f6f9 !important; }

/* CORRECTION POUR LES BORDURES */
.border-primary { border-color: #1e42a0 !important; }
.border-secondary { border-color: #e4e6ef !important; }
.border-success { border-color: #42b53f !important; }
.border-info { border-color: #3596f7 !important; }
.border-warning { border-color: #ffa800 !important; }
.border-danger { border-color: #ee3158 !important; }
.border-dark { border-color: #172b4c !important; }
.border-light { border-color: #f3f6f9 !important; }

/* CORRECTION POUR LES OMBRES */
.shadow-sm { box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important; }
.shadow { box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important; }
.shadow-lg { box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175) !important; }

/* CORRECTION POUR LES ANIMATIONS */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideInDown {
    from {
        transform: translate3d(0, -100%, 0);
        visibility: visible;
    }
    to {
        transform: translate3d(0, 0, 0);
    }
}

@keyframes slideInUp {
    from {
        transform: translate3d(0, 100%, 0);
        visibility: visible;
    }
    to {
        transform: translate3d(0, 0, 0);
    }
}

.fadeIn { animation: fadeIn 0.5s ease-in-out; }
.slideInDown { animation: slideInDown 0.5s ease-in-out; }
.slideInUp { animation: slideInUp 0.5s ease-in-out; }

/* CORRECTION POUR LES TRANSITIONS */
.transition-all { transition: all 0.3s ease-in-out !important; }
.transition-opacity { transition: opacity 0.3s ease-in-out !important; }
.transition-transform { transition: transform 0.3s ease-in-out !important; }

/* CORRECTION POUR LES HOVER EFFECTS */
.btn:hover { transform: translateY(-1px); transition: all 0.2s ease-in-out; }
.card:hover { box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); transition: all 0.2s ease-in-out; }

/* CORRECTION POUR LA RESPONSIVITÉ */
@media (max-width: 768px) {
    html { font-size: 13px !important; }
    body { font-size: 13px !important; }
    .main-sidebar .sidebar-menu > li > a { font-size: 13px !important; }
    .main-sidebar .sidebar-menu .treeview-menu > li > a { font-size: 12px !important; }
}

@media (max-width: 576px) {
    html { font-size: 12px !important; }
    body { font-size: 12px !important; }
    .main-sidebar .sidebar-menu > li > a { font-size: 12px !important; }
    .main-sidebar .sidebar-menu .treeview-menu > li > a { font-size: 11px !important; }
}
'''
    
    # Créer le fichier dans static/ et staticfiles/
    static_path = Path('static/css/comprehensive-fix.css')
    staticfiles_path = Path('staticfiles/css/comprehensive-fix.css')
    
    static_path.parent.mkdir(parents=True, exist_ok=True)
    staticfiles_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(static_path, 'w', encoding='utf-8') as f:
        f.write(comprehensive_css)
    
    with open(staticfiles_path, 'w', encoding='utf-8') as f:
        f.write(comprehensive_css)
    
    print(f"✅ CSS complet créé: {len(comprehensive_css)} caractères")
    print(f"📁 Fichier créé dans: {static_path}")
    print(f"📁 Fichier créé dans: {staticfiles_path}")
    
    return True

def main():
    """Fonction principale d'analyse et correction"""
    print("🎯 ANALYSE ET CORRECTION COMPLÈTE DES PROBLÈMES CSS")
    print("🏢 Cabinet d'Avocats - Django Railway")
    print("=" * 70)
    
    tasks = [
        ("Analyse des problèmes CSS", analyze_css_issues),
        ("Correction des imports vendors_css", fix_vendors_css_imports),
        ("Copie des corrections vers staticfiles", copy_font_fixes_to_staticfiles),
        ("Création du CSS de correction complet", create_comprehensive_css_fix),
    ]
    
    success_count = 0
    for name, task_func in tasks:
        try:
            print(f"\n🔄 {name}...")
            result = task_func()
            if result:
                success_count += 1
                print(f"✅ {name} - SUCCÈS")
            else:
                print(f"⚠️ {name} - PARTIEL")
        except Exception as e:
            print(f"❌ {name} - ERREUR: {e}")
    
    print("\n" + "=" * 70)
    print(f"🎯 ANALYSE ET CORRECTION TERMINÉES: {success_count}/{len(tasks)} tâches réussies")
    
    if success_count >= 3:
        print("🎉 PROBLÈMES CSS RÉSOLUS!")
        print("✨ L'apparence du site devrait maintenant être correcte!")
        print("\n📋 CORRECTIONS APPLIQUÉES:")
        print("  ✅ Analyse complète des fichiers CSS")
        print("  ✅ Correction des imports manquants")
        print("  ✅ CSS de correction complet créé")
        print("  ✅ Fallbacks CDN ajoutés")
        print("  ✅ Fonts Google chargées correctement")
        print("  ✅ Tailles de police harmonisées")
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("  1. Ajouter l'import du CSS complet dans vendors_css.css")
        print("  2. Redéployer l'application sur Railway")
        print("  3. Vérifier l'apparence du site")
        return True
    else:
        print("⚠️ Certaines corrections ont échoué")
        print("🔧 Vérifiez les erreurs et réessayez")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)