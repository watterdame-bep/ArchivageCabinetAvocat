#!/usr/bin/env python
"""
Correction des problèmes d'icônes et de charts
"""
import os
from pathlib import Path

def fix_icons_display():
    """Corriger l'affichage des icônes"""
    print("🎨 CORRECTION DE L'AFFICHAGE DES ICÔNES")
    print("=" * 50)
    
    # Créer un CSS spécifique pour corriger les icônes
    icons_fix_css = '''
/* Correction spécifique pour les icônes - Cabinet d'Avocats */

/* Force le chargement des fonts d'icônes avec priorité */
@font-face {
    font-family: 'FontAwesome';
    src: url('/static/assets/icons/font-awesome/fonts/fontawesome-webfont3e6e.woff2') format('woff2'),
         url('/static/assets/icons/font-awesome/fonts/fontawesome-webfont3e6e.woff') format('woff'),
         url('/static/assets/icons/font-awesome/fonts/fontawesome-webfont3e6e.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'Material Design Icons';
    src: url('/static/assets/icons/material-design-iconic-font/fonts/materialdesignicons-webfontdf71.woff2') format('woff2'),
         url('/static/assets/icons/material-design-iconic-font/fonts/materialdesignicons-webfontdf71.woff') format('woff'),
         url('/static/assets/icons/material-design-iconic-font/fonts/materialdesignicons-webfontdf71.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'Ionicons';
    src: url('/static/assets/icons/Ionicons/fonts/ionicons28b5.woff2') format('woff2'),
         url('/static/assets/icons/Ionicons/fonts/ionicons28b5.woff') format('woff'),
         url('/static/assets/icons/Ionicons/fonts/ionicons28b5.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'themify';
    src: url('/static/assets/icons/themify-icons/fonts/themify.woff') format('woff'),
         url('/static/assets/icons/themify-icons/fonts/themify.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}

/* Correction pour FontAwesome */
.fa, .fas, .far, .fal, .fab {
    font-family: 'FontAwesome' !important;
    font-weight: normal !important;
    font-style: normal !important;
    text-decoration: inherit !important;
    text-rendering: auto !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}

/* Correction pour Material Design Icons */
.mdi, .material-icons {
    font-family: 'Material Design Icons' !important;
    font-weight: normal !important;
    font-style: normal !important;
    text-decoration: inherit !important;
    text-rendering: auto !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}

/* Correction pour Ionicons */
.ion, .ionicons {
    font-family: 'Ionicons' !important;
    font-weight: normal !important;
    font-style: normal !important;
    text-decoration: inherit !important;
    text-rendering: auto !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}

/* Correction pour Themify Icons */
.ti {
    font-family: 'themify' !important;
    font-weight: normal !important;
    font-style: normal !important;
    text-decoration: inherit !important;
    text-rendering: auto !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}

/* Correction spécifique pour les icônes de la sidebar */
.sidebar-menu .fa, .sidebar-menu .ion, .sidebar-menu .mdi, .sidebar-menu .ti {
    display: inline-block !important;
    width: 1.28571429em !important;
    text-align: center !important;
    margin-right: 10px !important;
}

/* Correction pour les icônes dans les boutons */
.btn .fa, .btn .ion, .btn .mdi, .btn .ti {
    margin-right: 5px !important;
}

/* Correction pour les icônes dans la navbar */
.navbar .fa, .navbar .ion, .navbar .mdi, .navbar .ti {
    font-size: 16px !important;
}

/* Correction pour les icônes dans les dropdowns */
.dropdown-menu .fa, .dropdown-menu .ion, .dropdown-menu .mdi, .dropdown-menu .ti {
    margin-right: 8px !important;
    width: 16px !important;
    text-align: center !important;
}

/* Correction pour les icônes dans les cartes */
.card .fa, .card .ion, .card .mdi, .card .ti {
    margin-right: 5px !important;
}

/* Correction pour les icônes dans les alertes */
.alert .fa, .alert .ion, .alert .mdi, .alert .ti {
    margin-right: 8px !important;
}

/* Correction pour les icônes dans les badges */
.badge .fa, .badge .ion, .badge .mdi, .badge .ti {
    font-size: 0.8em !important;
}

/* Correction pour les icônes dans les breadcrumbs */
.breadcrumb .fa, .breadcrumb .ion, .breadcrumb .mdi, .breadcrumb .ti {
    margin-right: 5px !important;
}

/* Correction pour les icônes dans les tabs */
.nav-tabs .fa, .nav-tabs .ion, .nav-tabs .mdi, .nav-tabs .ti,
.nav-pills .fa, .nav-pills .ion, .nav-pills .mdi, .nav-pills .ti {
    margin-right: 5px !important;
}

/* Correction pour les icônes dans les listes */
.list-group-item .fa, .list-group-item .ion, .list-group-item .mdi, .list-group-item .ti {
    margin-right: 8px !important;
    width: 16px !important;
    text-align: center !important;
}

/* Correction pour les icônes dans les modales */
.modal-header .fa, .modal-header .ion, .modal-header .mdi, .modal-header .ti {
    margin-right: 8px !important;
}

/* Correction pour les icônes dans les tooltips */
.tooltip .fa, .tooltip .ion, .tooltip .mdi, .tooltip .ti {
    font-size: 12px !important;
}

/* Correction pour les icônes dans les popovers */
.popover .fa, .popover .ion, .popover .mdi, .popover .ti {
    margin-right: 5px !important;
}

/* Correction pour les icônes spécifiques du template */
.icon-Layout-4-blocks:before { content: "\\f009"; }
.icon-Hummer:before { content: "\\f0e3"; }
.icon-User:before { content: "\\f007"; }
.icon-Commit:before { content: "\\f126"; }
.icon-Position:before { content: "\\f065"; }
.icon-Notification:before { content: "\\f0f3"; }
.icon-Settings1:before { content: "\\f013"; }
.icon-Menu:before { content: "\\f0c9"; }
.icon-Search:before { content: "\\f002"; }
.icon-Key:before { content: "\\f084"; }
.icon-Lock-overturning:before { content: "\\f023"; }
.icon-Group-chat:before { content: "\\f086"; }
.icon-Incoming-mail:before { content: "\\f0e0"; }
.icon-Add-user:before { content: "\\f234"; }
.icon-Clipboard:before { content: "\\f0ea"; }
.icon-Group:before { content: "\\f0c0"; }
.icon-Active-call:before { content: "\\f095"; }
.icon-Question-circle:before { content: "\\f059"; }
.icon-Notifications:before { content: "\\f0f3"; }
.icon-Color:before { content: "\\f1fc"; }

/* Force l'affichage des icônes même si les fonts ne se chargent pas */
.fa:before, .fas:before, .far:before, .fal:before, .fab:before,
.mdi:before, .ion:before, .ti:before {
    font-family: 'FontAwesome', 'Material Design Icons', 'Ionicons', 'themify', sans-serif !important;
}

/* Fallback pour les icônes qui ne se chargent pas */
.fa:not([class*="fa-"]):before,
.mdi:not([class*="mdi-"]):before,
.ion:not([class*="ion-"]):before,
.ti:not([class*="ti-"]):before {
    content: "●" !important;
    color: #666 !important;
}
'''
    
    # Créer le fichier dans static/ et staticfiles/
    static_path = Path('static/css/icons-fix.css')
    staticfiles_path = Path('staticfiles/css/icons-fix.css')
    
    static_path.parent.mkdir(parents=True, exist_ok=True)
    staticfiles_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(static_path, 'w', encoding='utf-8') as f:
        f.write(icons_fix_css)
    
    with open(staticfiles_path, 'w', encoding='utf-8') as f:
        f.write(icons_fix_css)
    
    print(f"✅ CSS de correction des icônes créé: {static_path}")
    print(f"✅ CSS de correction des icônes créé: {staticfiles_path}")
    print(f"📊 Taille: {staticfiles_path.stat().st_size} bytes")
    
    return True

def fix_charts_loading():
    """Corriger le chargement des charts"""
    print("\n📊 CORRECTION DU CHARGEMENT DES CHARTS")
    print("=" * 50)
    
    # Créer un JavaScript pour forcer le rechargement des charts
    charts_fix_js = '''
/* Correction du chargement des charts - Cabinet d'Avocats */

// Fonction pour initialiser les charts après le chargement complet
function initializeCharts() {
    console.log('Initialisation des charts...');
    
    // Attendre que tous les scripts soient chargés
    setTimeout(function() {
        // Forcer le redimensionnement des charts
        if (typeof window.dispatchEvent === 'function') {
            window.dispatchEvent(new Event('resize'));
        }
        
        // Réinitialiser les charts ApexCharts si présents
        if (typeof ApexCharts !== 'undefined') {
            console.log('ApexCharts détecté, réinitialisation...');
            // Trouver tous les éléments de charts
            document.querySelectorAll('[id*="chart"], [class*="chart"]').forEach(function(element) {
                if (element.id && !element.classList.contains('chart-initialized')) {
                    element.classList.add('chart-initialized');
                    // Forcer le rendu du chart
                    setTimeout(function() {
                        if (window[element.id + '_chart']) {
                            window[element.id + '_chart'].render();
                        }
                    }, 100);
                }
            });
        }
        
        // Réinitialiser les charts Morris si présents
        if (typeof Morris !== 'undefined') {
            console.log('Morris charts détecté, réinitialisation...');
            // Redessiner tous les charts Morris
            Morris.charts.forEach(function(chart) {
                if (chart && typeof chart.redraw === 'function') {
                    chart.redraw();
                }
            });
        }
        
        // Réinitialiser les charts Chart.js si présents
        if (typeof Chart !== 'undefined') {
            console.log('Chart.js détecté, réinitialisation...');
            Chart.helpers.each(Chart.instances, function(instance) {
                if (instance && typeof instance.update === 'function') {
                    instance.update();
                }
            });
        }
        
        // Réinitialiser les charts C3 si présents
        if (typeof c3 !== 'undefined') {
            console.log('C3 charts détecté, réinitialisation...');
            // Les charts C3 sont stockés globalement
            Object.keys(window).forEach(function(key) {
                if (key.includes('chart') && window[key] && typeof window[key].flush === 'function') {
                    window[key].flush();
                }
            });
        }
        
    }, 500);
}

// Initialiser les charts quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCharts);
} else {
    initializeCharts();
}

// Réinitialiser les charts lors du redimensionnement de la fenêtre
window.addEventListener('resize', function() {
    setTimeout(initializeCharts, 100);
});

// Réinitialiser les charts lors des changements de page (pour les SPA)
window.addEventListener('popstate', function() {
    setTimeout(initializeCharts, 200);
});

// Observer les changements dans le DOM pour les charts ajoutés dynamiquement
if (typeof MutationObserver !== 'undefined') {
    const chartObserver = new MutationObserver(function(mutations) {
        let hasNewCharts = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        if (node.id && (node.id.includes('chart') || node.className.includes('chart'))) {
                            hasNewCharts = true;
                        }
                        // Vérifier les enfants aussi
                        const chartElements = node.querySelectorAll && node.querySelectorAll('[id*="chart"], [class*="chart"]');
                        if (chartElements && chartElements.length > 0) {
                            hasNewCharts = true;
                        }
                    }
                });
            }
        });
        
        if (hasNewCharts) {
            console.log('Nouveaux charts détectés, réinitialisation...');
            setTimeout(initializeCharts, 300);
        }
    });
    
    // Observer les changements dans le body
    chartObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Fonction globale pour forcer la réinitialisation des charts
window.forceChartsRefresh = function() {
    console.log('Forçage de la réinitialisation des charts...');
    initializeCharts();
};

// Auto-refresh des charts toutes les 30 secondes pour s'assurer qu'ils restent visibles
setInterval(function() {
    // Vérifier si des charts sont invisibles
    const charts = document.querySelectorAll('[id*="chart"], [class*="chart"]');
    let hasInvisibleCharts = false;
    
    charts.forEach(function(chart) {
        if (chart.offsetHeight === 0 || chart.offsetWidth === 0) {
            hasInvisibleCharts = true;
        }
    });
    
    if (hasInvisibleCharts) {
        console.log('Charts invisibles détectés, réinitialisation...');
        initializeCharts();
    }
}, 30000);

console.log('Script de correction des charts chargé');
'''
    
    # Créer le fichier dans static/ et staticfiles/
    static_path = Path('static/js/charts-fix.js')
    staticfiles_path = Path('staticfiles/js/charts-fix.js')
    
    static_path.parent.mkdir(parents=True, exist_ok=True)
    staticfiles_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(static_path, 'w', encoding='utf-8') as f:
        f.write(charts_fix_js)
    
    with open(staticfiles_path, 'w', encoding='utf-8') as f:
        f.write(charts_fix_js)
    
    print(f"✅ JavaScript de correction des charts créé: {static_path}")
    print(f"✅ JavaScript de correction des charts créé: {staticfiles_path}")
    print(f"📊 Taille: {staticfiles_path.stat().st_size} bytes")
    
    return True

def update_vendors_css_with_icons_fix():
    """Ajouter le fix des icônes au vendors_css.css"""
    print("\n🔧 MISE À JOUR DE VENDORS_CSS.CSS AVEC LE FIX DES ICÔNES")
    print("=" * 50)
    
    vendors_css_path = Path('static/css/vendors_css.css')
    staticfiles_vendors_css = Path('staticfiles/css/vendors_css.css')
    
    if not vendors_css_path.exists():
        print("❌ vendors_css.css non trouvé")
        return False
    
    with open(vendors_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ajouter l'import du fix des icônes s'il n'existe pas
    if 'icons-fix.css' not in content:
        # Ajouter l'import après les autres corrections
        content = content.replace(
            '@import url(/static/css/comprehensive-fix.css);',
            '@import url(/static/css/comprehensive-fix.css);\n@import url(/static/css/icons-fix.css);'
        )
        
        # Écrire dans static/
        with open(vendors_css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Copier vers staticfiles/
        with open(staticfiles_vendors_css, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Import du fix des icônes ajouté à vendors_css.css")
    else:
        print("ℹ️ Fix des icônes déjà présent dans vendors_css.css")
    
    return True

def update_base_template_with_charts_fix():
    """Ajouter le script de fix des charts au template de base"""
    print("\n📋 MISE À JOUR DU TEMPLATE DE BASE AVEC LE FIX DES CHARTS")
    print("=" * 50)
    
    base_template_path = Path('templates/admin_template/base.html')
    
    if not base_template_path.exists():
        print("❌ Template de base non trouvé")
        return False
    
    with open(base_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le script est déjà ajouté
    if 'charts-fix.js' not in content:
        # Ajouter le script avant la fermeture du body
        script_tag = '\n\t<!-- Script de correction des charts -->\n\t<script src="{% static \'js/charts-fix.js\' %}"></script>\n\n</body>'
        
        if '</body>' in content:
            content = content.replace('</body>', script_tag)
            
            with open(base_template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Script de fix des charts ajouté au template de base")
        else:
            print("⚠️ Balise </body> non trouvée dans le template")
            return False
    else:
        print("ℹ️ Script de fix des charts déjà présent dans le template")
    
    return True

def main():
    """Fonction principale"""
    print("🎯 CORRECTION DES ICÔNES ET CHARTS")
    print("🏢 Cabinet d'Avocats - Django Railway")
    print("=" * 60)
    
    tasks = [
        ("Correction de l'affichage des icônes", fix_icons_display),
        ("Correction du chargement des charts", fix_charts_loading),
        ("Mise à jour vendors_css avec fix icônes", update_vendors_css_with_icons_fix),
        ("Mise à jour template avec fix charts", update_base_template_with_charts_fix),
    ]
    
    success_count = 0
    
    for name, task_func in tasks:
        try:
            result = task_func()
            if result:
                success_count += 1
                print(f"\n✅ {name} - SUCCÈS")
            else:
                print(f"\n⚠️ {name} - PROBLÈME")
        except Exception as e:
            print(f"\n❌ {name} - ERREUR: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 CORRECTION TERMINÉE: {success_count}/{len(tasks)} tâches réussies")
    
    if success_count >= 3:
        print("🎉 PROBLÈMES D'ICÔNES ET CHARTS CORRIGÉS!")
        print("✨ Les icônes devraient maintenant s'afficher correctement!")
        print("📊 Les charts devraient se charger dès la première visite!")
        print("\n📋 CORRECTIONS APPLIQUÉES:")
        print("  ✅ CSS de correction des icônes avec fonts forcées")
        print("  ✅ JavaScript de réinitialisation automatique des charts")
        print("  ✅ Import du fix des icônes dans vendors_css.css")
        print("  ✅ Script de fix des charts dans le template de base")
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("  1. Redéployer l'application sur Railway")
        print("  2. Vérifier l'affichage des icônes")
        print("  3. Tester le chargement des charts au premier accès")
        return True
    else:
        print("⚠️ Certaines corrections ont échoué")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)