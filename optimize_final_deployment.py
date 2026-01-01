#!/usr/bin/env python
"""
Optimisations finales pour le déploiement Railway
"""
import os
import sys
from pathlib import Path
import shutil

def create_missing_select2():
    """Créer le fichier Select2 manquant"""
    print("🎨 Création de Select2 manquant...")
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
    else:
        staticfiles_path = Path('staticfiles')
    
    select2_dir = staticfiles_path / 'assets/vendor_components/select2/dist/css'
    select2_dir.mkdir(parents=True, exist_ok=True)
    
    select2_css = select2_dir / 'select2.min.css'
    
    if not select2_css.exists():
        select2_content = '''
/* Select2 CSS pour Railway */
.select2-container {
    box-sizing: border-box;
    display: inline-block;
    margin: 0;
    position: relative;
    vertical-align: middle;
}

.select2-container .select2-selection--single {
    box-sizing: border-box;
    cursor: pointer;
    display: block;
    height: 28px;
    user-select: none;
    -webkit-user-select: none;
}

.select2-container--default .select2-selection--single {
    background-color: #fff;
    border: 1px solid #aaa;
    border-radius: 4px;
}

.select2-container--default .select2-selection--single .select2-selection__rendered {
    color: #444;
    line-height: 28px;
}

.select2-container--default .select2-selection--single .select2-selection__clear {
    cursor: pointer;
    float: right;
    font-weight: bold;
}

.select2-container--default .select2-selection--single .select2-selection__placeholder {
    color: #999;
}

.select2-container--default .select2-selection--single .select2-selection__arrow {
    height: 26px;
    position: absolute;
    top: 1px;
    right: 1px;
    width: 20px;
}

.select2-container--default .select2-selection--single .select2-selection__arrow b {
    border-color: #888 transparent transparent transparent;
    border-style: solid;
    border-width: 5px 4px 0 4px;
    height: 0;
    left: 50%;
    margin-left: -4px;
    margin-top: -2px;
    position: absolute;
    top: 50%;
    width: 0;
}

.select2-dropdown {
    background-color: white;
    border: 1px solid #aaa;
    border-radius: 4px;
    box-sizing: border-box;
    display: block;
    position: absolute;
    left: -100000px;
    width: 100%;
    z-index: 1051;
}

.select2-results {
    display: block;
}

.select2-results__options {
    list-style: none;
    margin: 0;
    padding: 0;
}

.select2-results__option {
    padding: 6px;
    user-select: none;
    -webkit-user-select: none;
}

.select2-results__option[aria-selected] {
    cursor: pointer;
}

.select2-container--default .select2-results__option[aria-selected=true] {
    background-color: #ddd;
}

.select2-container--default .select2-results__option--highlighted[aria-selected] {
    background-color: #5897fb;
    color: white;
}

.select2-container--default .select2-results__option[data-selected=true] {
    background-color: #ddd;
}

.select2-container--default .select2-results__option--highlighted[data-selected] {
    background-color: #5897fb;
    color: white;
}

.select2-close-mask {
    border: 0;
    margin: 0;
    padding: 0;
    display: block;
    position: fixed;
    left: 0;
    top: 0;
    min-height: 100%;
    min-width: 100%;
    height: auto;
    width: auto;
    opacity: 0;
    z-index: 99;
    background-color: #fff;
    filter: alpha(opacity=0);
}

.select2-hidden-accessible {
    border: 0 !important;
    clip: rect(0 0 0 0) !important;
    -webkit-clip-path: inset(50%) !important;
    clip-path: inset(50%) !important;
    height: 1px !important;
    overflow: hidden !important;
    padding: 0 !important;
    position: absolute !important;
    width: 1px !important;
    white-space: nowrap !important;
}
'''
        
        with open(select2_css, 'w', encoding='utf-8') as f:
            f.write(select2_content)
        
        print(f"✅ Select2 CSS créé: {select2_css}")
        return True
    
    print(f"✅ Select2 CSS déjà présent: {select2_css}")
    return True

def optimize_bootstrap_paths():
    """Optimiser les chemins Bootstrap"""
    print("🔧 Optimisation des chemins Bootstrap...")
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
    else:
        staticfiles_path = Path('staticfiles')
    
    # Vérifier si bootstrap.css existe dans le bon répertoire
    bootstrap_source = staticfiles_path / 'assets/vendor_components/bootstrap/dist/css/bootstrap.css'
    bootstrap_target = staticfiles_path / 'css/bootstrap.min.css'
    
    if bootstrap_source.exists() and not bootstrap_target.exists():
        bootstrap_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bootstrap_source, bootstrap_target)
        print(f"✅ Bootstrap copié vers: {bootstrap_target}")
    
    # Créer un lien alternatif si nécessaire
    bootstrap_alt = staticfiles_path / 'assets/vendor_components/bootstrap/dist/css/bootstrap.min.css'
    if bootstrap_source.exists() and not bootstrap_alt.exists():
        shutil.copy2(bootstrap_source, bootstrap_alt)
        print(f"✅ Bootstrap alternatif créé: {bootstrap_alt}")
    
    return True

def create_comprehensive_fallback_css():
    """Créer un CSS de fallback complet"""
    print("🎨 Création du CSS de fallback complet...")
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
    else:
        staticfiles_path = Path('staticfiles')
    
    fallback_css = staticfiles_path / 'css/comprehensive-fallback.css'
    fallback_css.parent.mkdir(parents=True, exist_ok=True)
    
    fallback_content = '''
/* CSS de fallback complet pour Railway */

/* Import des CSS critiques via CDN */
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
@import url('https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css');

/* Corrections pour les composants manquants */
.select2-container {
    box-sizing: border-box;
    display: inline-block;
    margin: 0;
    position: relative;
    vertical-align: middle;
}

.select2-container .select2-selection--single {
    background-color: #fff;
    border: 1px solid #ced4da;
    border-radius: 0.375rem;
    height: calc(1.5em + 0.75rem + 2px);
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    color: #495057;
}

/* Raty - Système de notation */
.raty {
    position: relative;
    display: inline-block;
}

.raty img {
    cursor: pointer;
    float: left;
    margin-right: 2px;
}

.raty-cancel {
    position: absolute;
    left: -10px;
}

/* Bootstrap TouchSpin */
.bootstrap-touchspin .input-group-btn-vertical {
    position: relative;
    white-space: nowrap;
    width: 1%;
    vertical-align: middle;
    display: table-cell;
}

.bootstrap-touchspin .input-group-btn-vertical > .btn {
    display: block;
    float: none;
    width: 100%;
    max-width: 100%;
    padding: 8px 10px;
    margin-left: -1px;
    position: relative;
    border-radius: 0;
}

.bootstrap-touchspin .input-group-btn-vertical .bootstrap-touchspin-up {
    border-top-right-radius: 4px;
}

.bootstrap-touchspin .input-group-btn-vertical .bootstrap-touchspin-down {
    border-bottom-right-radius: 4px;
}

/* Preloader */
.preloader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #fff;
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
}

.preloader::after {
    content: '';
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Avatars par défaut */
.avatar-2, .avatar-3 {
    width: 50px;
    height: 50px;
    background: linear-gradient(45deg, #3498db, #2ecc71);
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 18px;
}

.avatar-2::after { content: "U2"; }
.avatar-3::after { content: "U3"; }

/* Gestion des images media manquantes */
img[src*="/media/"] {
    background: linear-gradient(45deg, #f8f9fa, #e9ecef);
    border: 2px dashed #dee2e6;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #6c757d;
    font-size: 12px;
    min-width: 50px;
    min-height: 50px;
}

img[src*="/media/"]:after { content: "Image"; }

/* Logos */
img[src*="/media/LogoCabinet/"] {
    width: 100px;
    height: 60px;
    background: linear-gradient(45deg, #007bff, #0056b3);
    color: white;
}
img[src*="/media/LogoCabinet/"]:after { content: "LOGO"; font-weight: bold; }

/* Photos agents */
img[src*="/media/PhotoAgent/"] {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(45deg, #28a745, #20c997);
    color: white;
}
img[src*="/media/PhotoAgent/"]:after { content: "👤"; font-size: 20px; }

/* Photos clients */
img[src*="/media/clients_photos/"] {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(45deg, #17a2b8, #138496);
    color: white;
}
img[src*="/media/clients_photos/"]:after { content: "👥"; font-size: 20px; }

/* Corrections pour les icônes */
.fa:before, .fas:before, .far:before, .fal:before, .fab:before {
    font-family: "Font Awesome 6 Free", "Font Awesome 6 Brands", "Font Awesome 6 Pro" !important;
}

.material-icons {
    font-family: 'Material Icons' !important;
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
}

.ion:before {
    font-family: "Ionicons" !important;
}

/* Corrections pour les composants Bootstrap */
.btn {
    display: inline-block;
    font-weight: 400;
    line-height: 1.5;
    color: #212529;
    text-align: center;
    text-decoration: none;
    vertical-align: middle;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
    background-color: transparent;
    border: 1px solid transparent;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    border-radius: 0.375rem;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.btn-primary {
    color: #fff;
    background-color: #0d6efd;
    border-color: #0d6efd;
}

.btn-primary:hover {
    color: #fff;
    background-color: #0b5ed7;
    border-color: #0a58ca;
}

/* Corrections pour les formulaires */
.form-control {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #212529;
    background-color: #fff;
    background-image: none;
    border: 1px solid #ced4da;
    border-radius: 0.375rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
    color: #212529;
    background-color: #fff;
    border-color: #86b7fe;
    outline: 0;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Corrections pour les tableaux */
.table {
    --bs-table-bg: transparent;
    --bs-table-accent-bg: transparent;
    --bs-table-striped-color: #212529;
    --bs-table-striped-bg: rgba(0, 0, 0, 0.05);
    --bs-table-active-color: #212529;
    --bs-table-active-bg: rgba(0, 0, 0, 0.1);
    --bs-table-hover-color: #212529;
    --bs-table-hover-bg: rgba(0, 0, 0, 0.075);
    width: 100%;
    margin-bottom: 1rem;
    color: #212529;
    vertical-align: top;
    border-color: #dee2e6;
}

.table > :not(caption) > * > * {
    padding: 0.5rem 0.5rem;
    background-color: var(--bs-table-bg);
    border-bottom-width: 1px;
    box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);
}

/* Corrections pour les alertes */
.alert {
    position: relative;
    padding: 1rem 1rem;
    margin-bottom: 1rem;
    border: 1px solid transparent;
    border-radius: 0.375rem;
}

.alert-success {
    color: #0f5132;
    background-color: #d1e7dd;
    border-color: #badbcc;
}

.alert-danger {
    color: #842029;
    background-color: #f8d7da;
    border-color: #f5c2c7;
}

.alert-warning {
    color: #664d03;
    background-color: #fff3cd;
    border-color: #ffecb5;
}

.alert-info {
    color: #055160;
    background-color: #d1ecf1;
    border-color: #b8daff;
}
'''
    
    with open(fallback_css, 'w', encoding='utf-8') as f:
        f.write(fallback_content)
    
    print(f"✅ CSS de fallback complet créé: {fallback_css}")
    return True

def create_js_fallbacks():
    """Créer les fallbacks JavaScript"""
    print("📜 Création des fallbacks JavaScript...")
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
    else:
        staticfiles_path = Path('staticfiles')
    
    js_dir = staticfiles_path / 'js'
    js_dir.mkdir(parents=True, exist_ok=True)
    
    # Créer un fichier JS de fallback complet
    fallback_js = js_dir / 'comprehensive-fallback.js'
    
    fallback_js_content = '''
/* JavaScript de fallback complet pour Railway */

// Charger Bootstrap JS via CDN si pas déjà chargé
if (typeof bootstrap === 'undefined') {
    var bootstrapScript = document.createElement('script');
    bootstrapScript.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
    bootstrapScript.integrity = 'sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz';
    bootstrapScript.crossOrigin = 'anonymous';
    document.head.appendChild(bootstrapScript);
}

// Charger jQuery si pas déjà chargé
if (typeof jQuery === 'undefined') {
    var jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
    jqueryScript.integrity = 'sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=';
    jqueryScript.crossOrigin = 'anonymous';
    document.head.appendChild(jqueryScript);
}

// Charger Select2 si pas déjà chargé
if (typeof jQuery !== 'undefined') {
    jQuery(document).ready(function($) {
        if (typeof $.fn.select2 === 'undefined') {
            var select2Script = document.createElement('script');
            select2Script.src = 'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js';
            document.head.appendChild(select2Script);
        }
    });
}

// Charger ApexCharts si pas déjà chargé
if (typeof ApexCharts === 'undefined') {
    var apexScript = document.createElement('script');
    apexScript.src = 'https://cdn.jsdelivr.net/npm/apexcharts@latest';
    document.head.appendChild(apexScript);
}

// Fonction pour initialiser les composants après chargement
function initializeComponents() {
    // Initialiser les tooltips Bootstrap
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Initialiser les popovers Bootstrap
    if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }
    
    // Initialiser Select2
    if (typeof jQuery !== 'undefined' && typeof jQuery.fn.select2 !== 'undefined') {
        jQuery('.select2').select2();
    }
}

// Initialiser les composants quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeComponents);
} else {
    initializeComponents();
}

// Réessayer l'initialisation après un délai pour s'assurer que tous les scripts sont chargés
setTimeout(initializeComponents, 1000);

console.log('✅ Fallbacks JavaScript chargés pour Railway');
'''
    
    with open(fallback_js, 'w', encoding='utf-8') as f:
        f.write(fallback_js_content)
    
    print(f"✅ JavaScript de fallback créé: {fallback_js}")
    return True

def main():
    """Fonction principale d'optimisation"""
    print("🎯 OPTIMISATIONS FINALES POUR RAILWAY")
    print("=" * 50)
    
    optimizations = [
        ("Select2 manquant", create_missing_select2),
        ("Chemins Bootstrap", optimize_bootstrap_paths),
        ("CSS de fallback complet", create_comprehensive_fallback_css),
        ("JavaScript fallbacks", create_js_fallbacks),
    ]
    
    success_count = 0
    for name, optimization_func in optimizations:
        try:
            print(f"\n🔧 {name}...")
            result = optimization_func()
            if result:
                success_count += 1
                print(f"✅ {name} - SUCCÈS")
            else:
                print(f"⚠️ {name} - PARTIEL")
        except Exception as e:
            print(f"❌ {name} - ERREUR: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 OPTIMISATIONS TERMINÉES: {success_count}/{len(optimizations)} réussies")
    
    if success_count == len(optimizations):
        print("🎉 TOUTES LES OPTIMISATIONS APPLIQUÉES AVEC SUCCÈS!")
        print("✨ L'application devrait maintenant être à 100% fonctionnelle!")
        return True
    else:
        print("⚠️ Certaines optimisations ont échoué, mais l'application devrait fonctionner.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)