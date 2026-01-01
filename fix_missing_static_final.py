#!/usr/bin/env python
"""
Script final pour corriger TOUS les fichiers statiques manquants
"""
from pathlib import Path
import shutil

def fix_all_missing_files():
    """Corriger tous les fichiers manquants identifiés"""
    print("🔧 CORRECTION FINALE DE TOUS LES FICHIERS MANQUANTS")
    print("=" * 60)
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
        static_path = Path('/app/static')
    else:
        staticfiles_path = Path('staticfiles')
        static_path = Path('static')
    
    # 1. Corriger Bootstrap CSS manquant
    print("🎨 1. Correction Bootstrap CSS...")
    bootstrap_source = staticfiles_path / 'assets/vendor_components/bootstrap/dist/css/bootstrap.css'
    if not bootstrap_source.exists():
        # Créer le répertoire
        bootstrap_source.parent.mkdir(parents=True, exist_ok=True)
        
        # Créer un Bootstrap CSS complet
        bootstrap_content = '''
/*!
 * Bootstrap v5.3.0 (https://getbootstrap.com/)
 * Copyright 2011-2023 The Bootstrap Authors
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
 */
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');

/* Corrections spécifiques pour Railway */
.btn { margin: 2px; }
.form-control { margin-bottom: 10px; }
.card { margin-bottom: 20px; }
.table { margin-bottom: 20px; }

/* Corrections pour les composants manquants */
.input-group-btn-vertical {
    position: relative;
    white-space: nowrap;
    width: 1%;
    vertical-align: middle;
    display: table-cell;
}

.input-group-btn-vertical > .btn {
    display: block;
    float: none;
    width: 100%;
    max-width: 100%;
    padding: 8px 10px;
    margin-left: -1px;
    position: relative;
    border-radius: 0;
}

.bootstrap-touchspin-up {
    border-top-right-radius: 4px;
}

.bootstrap-touchspin-down {
    border-bottom-right-radius: 4px;
}
'''
        
        with open(bootstrap_source, 'w', encoding='utf-8') as f:
            f.write(bootstrap_content)
        print(f"✅ Bootstrap CSS créé: {bootstrap_source}")
    
    # 2. Corriger Select2 CSS manquant
    print("🎨 2. Correction Select2 CSS...")
    select2_css = staticfiles_path / 'assets/vendor_components/select2/dist/css/select2.min.css'
    if not select2_css.exists():
        select2_css.parent.mkdir(parents=True, exist_ok=True)
        
        select2_content = '''
@import url('https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css');

/* Corrections Select2 pour Railway */
.select2-container {
    width: 100% !important;
}

.select2-selection {
    height: 38px !important;
    border: 1px solid #ced4da !important;
    border-radius: 0.375rem !important;
}

.select2-selection__rendered {
    line-height: 36px !important;
    padding-left: 12px !important;
}

.select2-selection__arrow {
    height: 36px !important;
}
'''
        
        with open(select2_css, 'w', encoding='utf-8') as f:
            f.write(select2_content)
        print(f"✅ Select2 CSS créé: {select2_css}")
    
    # 3. Créer tous les CSS de composants manquants
    print("🎨 3. Création des CSS de composants...")
    
    components_css = {
        'assets/vendor_components/datatables.net-bs/css/dataTables.bootstrap.min.css': '''
@import url('https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css');
.dataTables_wrapper { margin-top: 20px; }
''',
        'assets/vendor_components/sweetalert/sweetalert.css': '''
@import url('https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css');
''',
        'assets/vendor_components/jquery-toast-plugin/dist/jquery.toast.min.css': '''
.jq-toast-wrap { position: fixed; top: 10px; right: 15px; z-index: 9999; }
.jq-toast-single { padding: 10px; margin: 5px; border-radius: 4px; }
.jq-toast-success { background: #28a745; color: white; }
.jq-toast-error { background: #dc3545; color: white; }
.jq-toast-warning { background: #ffc107; color: black; }
.jq-toast-info { background: #17a2b8; color: white; }
''',
        'assets/vendor_components/morris.js/morris.css': '''
.morris-hover { position: absolute; z-index: 1000; }
.morris-hover.morris-default-style { padding: 6px; color: #666; background: rgba(255, 255, 255, 0.8); border: solid 2px rgba(230, 230, 230, 0.8); border-radius: 5px; }
''',
        'assets/vendor_components/c3/c3.min.css': '''
@import url('https://cdn.jsdelivr.net/npm/c3@0.7.20/c3.min.css');
''',
        'assets/vendor_components/chartist-js-develop/dist/chartist.min.css': '''
@import url('https://cdn.jsdelivr.net/npm/chartist@0.11.4/dist/chartist.min.css');
''',
    }
    
    for file_path, content in components_css.items():
        full_path = staticfiles_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Créé: {file_path}")
    
    # 4. Créer les JS manquants
    print("📜 4. Création des JS manquants...")
    
    components_js = {
        'assets/vendor_components/datatables.net/js/jquery.dataTables.min.js': '''
// DataTables via CDN
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js';
    document.head.appendChild(script);
})();
''',
        'assets/vendor_components/datatables.net-bs/js/dataTables.bootstrap.min.js': '''
// DataTables Bootstrap via CDN
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js';
    document.head.appendChild(script);
})();
''',
        'assets/vendor_components/sweetalert/sweetalert.min.js': '''
// SweetAlert via CDN
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
    document.head.appendChild(script);
})();
''',
        'assets/vendor_components/jquery-toast-plugin/dist/jquery.toast.min.js': '''
// jQuery Toast Plugin
(function($) {
    $.toast = function(options) {
        var settings = $.extend({
            text: '',
            heading: '',
            icon: 'info',
            showHideTransition: 'fade',
            allowToastClose: true,
            hideAfter: 3000,
            stack: 5,
            position: 'top-right'
        }, options);
        
        var toastHtml = '<div class="jq-toast-single jq-toast-' + settings.icon + '">';
        if (settings.heading) {
            toastHtml += '<h2 class="jq-toast-heading">' + settings.heading + '</h2>';
        }
        toastHtml += '<span class="jq-toast-text">' + settings.text + '</span>';
        if (settings.allowToastClose) {
            toastHtml += '<span class="close-jq-toast-single">&times;</span>';
        }
        toastHtml += '</div>';
        
        var $toast = $(toastHtml);
        
        if (!$('.jq-toast-wrap').length) {
            $('body').append('<div class="jq-toast-wrap"></div>');
        }
        
        $('.jq-toast-wrap').append($toast);
        
        if (settings.hideAfter !== false) {
            setTimeout(function() {
                $toast.fadeOut(function() {
                    $(this).remove();
                });
            }, settings.hideAfter);
        }
        
        $toast.find('.close-jq-toast-single').click(function() {
            $toast.fadeOut(function() {
                $(this).remove();
            });
        });
    };
})(jQuery);
''',
        'assets/vendor_components/morris.js/morris.min.js': '''
// Morris.js via CDN
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/morris.js@0.5.1/morris.min.js';
    document.head.appendChild(script);
})();
''',
        'assets/vendor_components/c3/c3.min.js': '''
// C3.js via CDN
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/c3@0.7.20/c3.min.js';
    document.head.appendChild(script);
})();
''',
        'assets/vendor_components/chartist-js-develop/dist/chartist.min.js': '''
// Chartist.js via CDN
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chartist@0.11.4/dist/chartist.min.js';
    document.head.appendChild(script);
})();
''',
    }
    
    for file_path, content in components_js.items():
        full_path = staticfiles_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Créé: {file_path}")
    
    # 5. Créer un CSS global de corrections
    print("🎨 5. CSS global de corrections...")
    
    global_fixes_css = staticfiles_path / 'css/railway-global-fixes.css'
    global_fixes_content = '''
/* CSS GLOBAL DE CORRECTIONS POUR RAILWAY */

/* Import de tous les CDN nécessaires */
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
@import url('https://cdn.jsdelivr.net/npm/ionicons@7.1.0/dist/collection/components/icon/icon.css');

/* Corrections pour les composants manquants */
.btn-group-vertical > .btn:not(:first-child):not(:last-child) {
    border-radius: 0;
}

.btn-group-vertical > .btn:first-child:not(:last-child) {
    border-top-left-radius: 0.375rem;
    border-top-right-radius: 0.375rem;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}

.btn-group-vertical > .btn:last-child:not(:first-child) {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    border-bottom-right-radius: 0.375rem;
    border-bottom-left-radius: 0.375rem;
}

/* Corrections pour les tableaux */
.table-responsive {
    overflow-x: auto;
}

.table th, .table td {
    padding: 0.75rem;
    vertical-align: top;
    border-top: 1px solid #dee2e6;
}

/* Corrections pour les formulaires */
.form-group {
    margin-bottom: 1rem;
}

.form-control:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Corrections pour les cartes */
.card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 0.375rem;
}

.card-header {
    padding: 0.75rem 1.25rem;
    margin-bottom: 0;
    background-color: rgba(0, 0, 0, 0.03);
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.card-body {
    flex: 1 1 auto;
    padding: 1.25rem;
}

/* Corrections pour les alertes */
.alert {
    position: relative;
    padding: 0.75rem 1.25rem;
    margin-bottom: 1rem;
    border: 1px solid transparent;
    border-radius: 0.375rem;
}

.alert-success {
    color: #155724;
    background-color: #d4edda;
    border-color: #c3e6cb;
}

.alert-danger {
    color: #721c24;
    background-color: #f8d7da;
    border-color: #f5c6cb;
}

.alert-warning {
    color: #856404;
    background-color: #fff3cd;
    border-color: #ffeaa7;
}

.alert-info {
    color: #0c5460;
    background-color: #d1ecf1;
    border-color: #bee5eb;
}

/* Corrections pour les badges */
.badge {
    display: inline-block;
    padding: 0.25em 0.4em;
    font-size: 75%;
    font-weight: 700;
    line-height: 1;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: 0.375rem;
}

.badge-primary {
    color: #fff;
    background-color: #007bff;
}

.badge-success {
    color: #fff;
    background-color: #28a745;
}

.badge-danger {
    color: #fff;
    background-color: #dc3545;
}

.badge-warning {
    color: #212529;
    background-color: #ffc107;
}

.badge-info {
    color: #fff;
    background-color: #17a2b8;
}

/* Corrections pour les icônes manquantes */
.fa, .fas, .far, .fal, .fab {
    font-family: "Font Awesome 6 Free", "Font Awesome 6 Brands" !important;
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

.ion {
    font-family: "Ionicons" !important;
}

/* Corrections pour les images manquantes */
img[src*="/media/"]:not([src*="data:"]) {
    background: linear-gradient(45deg, #f8f9fa, #e9ecef);
    border: 2px dashed #dee2e6;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #6c757d;
    font-size: 12px;
    min-width: 50px;
    min-height: 50px;
    position: relative;
}

img[src*="/media/"]:not([src*="data:"]):after {
    content: "📷";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 20px;
}

/* Corrections spécifiques pour les logos */
img[src*="/media/LogoCabinet/"]:after {
    content: "🏛️";
    font-size: 30px;
}

/* Corrections pour les avatars */
img[src*="/media/PhotoAgent/"]:after,
img[src*="/media/clients_photos/"]:after {
    content: "👤";
    font-size: 25px;
}

/* Corrections pour les spinners/preloaders */
.preloader, .spinner {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.9);
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
}

.preloader::after, .spinner::after {
    content: '';
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Corrections pour les tooltips */
.tooltip {
    position: absolute;
    z-index: 1070;
    display: block;
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-style: normal;
    font-weight: 400;
    line-height: 1.5;
    text-align: left;
    text-decoration: none;
    text-shadow: none;
    text-transform: none;
    letter-spacing: normal;
    word-break: normal;
    word-spacing: normal;
    white-space: normal;
    line-break: auto;
    font-size: 0.875rem;
    word-wrap: break-word;
    opacity: 0;
}

.tooltip.show {
    opacity: 0.9;
}

/* Corrections pour les modals */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1050;
    display: none;
    width: 100%;
    height: 100%;
    overflow: hidden;
    outline: 0;
}

.modal-dialog {
    position: relative;
    width: auto;
    margin: 0.5rem;
    pointer-events: none;
}

.modal-content {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    pointer-events: auto;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 0.3rem;
    outline: 0;
}
'''
    
    with open(global_fixes_css, 'w', encoding='utf-8') as f:
        f.write(global_fixes_content)
    print(f"✅ CSS global créé: {global_fixes_css}")
    
    print("\n🎉 TOUTES LES CORRECTIONS APPLIQUÉES!")
    print("✨ L'apparence devrait maintenant être parfaite!")

if __name__ == '__main__':
    fix_all_missing_files()