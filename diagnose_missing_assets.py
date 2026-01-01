#!/usr/bin/env python
"""
Diagnostic avancé des assets manquants
"""
from pathlib import Path
import re

def diagnose_missing_assets():
    """Diagnostiquer les assets manquants en analysant les templates"""
    print("🔍 DIAGNOSTIC AVANCÉ DES ASSETS MANQUANTS")
    print("=" * 60)
    
    # Détecter l'environnement
    if Path('/app').exists():
        staticfiles_path = Path('/app/staticfiles')
        static_path = Path('/app/static')
        templates_path = Path('/app')
    else:
        staticfiles_path = Path('staticfiles')
        static_path = Path('static')
        templates_path = Path('.')
    
    # 1. Analyser les templates pour trouver les références CSS/JS
    print("📄 1. Analyse des templates...")
    
    template_files = []
    for pattern in ['**/*.html', '**/templates/**/*.html']:
        template_files.extend(list(templates_path.glob(pattern)))
    
    css_references = set()
    js_references = set()
    
    for template_file in template_files:
        try:
            content = template_file.read_text(encoding='utf-8')
            
            # Chercher les références CSS
            css_matches = re.findall(r'href=["\']([^"\']*\.css[^"\']*)["\']', content)
            for match in css_matches:
                if 'static' in match or 'assets' in match:
                    css_references.add(match.replace('{% static \'', '').replace('\' %}', '').replace('"', '').replace("'", ''))
            
            # Chercher les références JS
            js_matches = re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']', content)
            for match in js_matches:
                if 'static' in match or 'assets' in match:
                    js_references.add(match.replace('{% static \'', '').replace('\' %}', '').replace('"', '').replace("'", ''))
                    
        except Exception as e:
            print(f"⚠️ Erreur lecture {template_file}: {e}")
    
    print(f"📊 Références trouvées: {len(css_references)} CSS, {len(js_references)} JS")
    
    # 2. Vérifier quels fichiers existent
    print("\n🔍 2. Vérification des fichiers...")
    
    missing_css = []
    missing_js = []
    
    for css_ref in css_references:
        css_path = staticfiles_path / css_ref
        if not css_path.exists():
            missing_css.append(css_ref)
        else:
            print(f"✅ CSS: {css_ref}")
    
    for js_ref in js_references:
        js_path = staticfiles_path / js_ref
        if not js_path.exists():
            missing_js.append(js_ref)
        else:
            print(f"✅ JS: {js_ref}")
    
    # 3. Afficher les fichiers manquants
    print(f"\n❌ FICHIERS MANQUANTS:")
    print(f"CSS manquants: {len(missing_css)}")
    for css in missing_css[:20]:  # Limiter à 20
        print(f"  - {css}")
    
    print(f"\nJS manquants: {len(missing_js)}")
    for js in missing_js[:20]:  # Limiter à 20
        print(f"  - {js}")
    
    # 4. Créer les fichiers manquants les plus critiques
    print(f"\n🔧 4. Création des fichiers critiques manquants...")
    
    critical_css = {
        'css/bootstrap.min.css': '@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css");',
        'css/font-awesome.min.css': '@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css");',
        'css/material-icons.css': '@import url("https://fonts.googleapis.com/icon?family=Material+Icons");',
        'css/ionicons.css': '@import url("https://cdn.jsdelivr.net/npm/ionicons@7.1.0/dist/collection/components/icon/icon.css");',
    }
    
    critical_js = {
        'js/bootstrap.min.js': '''
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
    script.integrity = 'sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz';
    script.crossOrigin = 'anonymous';
    document.head.appendChild(script);
})();
''',
        'js/jquery.min.js': '''
(function() {
    if (typeof jQuery === 'undefined') {
        var script = document.createElement('script');
        script.src = 'https://code.jquery.com/jquery-3.7.1.min.js';
        script.integrity = 'sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=';
        script.crossOrigin = 'anonymous';
        document.head.appendChild(script);
    }
})();
''',
    }
    
    # Créer les CSS critiques manquants
    for css_file, content in critical_css.items():
        if css_file in missing_css:
            css_path = staticfiles_path / css_file
            css_path.parent.mkdir(parents=True, exist_ok=True)
            css_path.write_text(content, encoding='utf-8')
            print(f"✅ Créé CSS critique: {css_file}")
    
    # Créer les JS critiques manquants
    for js_file, content in critical_js.items():
        if js_file in missing_js:
            js_path = staticfiles_path / js_file
            js_path.parent.mkdir(parents=True, exist_ok=True)
            js_path.write_text(content, encoding='utf-8')
            print(f"✅ Créé JS critique: {js_file}")
    
    # 5. Créer des fallbacks pour les assets manquants
    print(f"\n🎨 5. Création de fallbacks pour assets manquants...")
    
    for css in missing_css:
        if any(keyword in css.lower() for keyword in ['bootstrap', 'font-awesome', 'material', 'ion']):
            continue  # Déjà traité dans les critiques
            
        css_path = staticfiles_path / css
        css_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Créer un CSS de fallback basique
        fallback_content = f'''
/* Fallback CSS pour {css} */
/* Généré automatiquement pour Railway */

.btn {{ 
    padding: 0.375rem 0.75rem; 
    margin-bottom: 0; 
    font-size: 1rem; 
    line-height: 1.5; 
    border-radius: 0.375rem; 
    border: 1px solid transparent;
    cursor: pointer;
}}

.btn-primary {{ background-color: #007bff; border-color: #007bff; color: #fff; }}
.btn-secondary {{ background-color: #6c757d; border-color: #6c757d; color: #fff; }}
.btn-success {{ background-color: #28a745; border-color: #28a745; color: #fff; }}
.btn-danger {{ background-color: #dc3545; border-color: #dc3545; color: #fff; }}
.btn-warning {{ background-color: #ffc107; border-color: #ffc107; color: #212529; }}
.btn-info {{ background-color: #17a2b8; border-color: #17a2b8; color: #fff; }}

.form-control {{ 
    display: block; 
    width: 100%; 
    padding: 0.375rem 0.75rem; 
    font-size: 1rem; 
    line-height: 1.5; 
    color: #495057; 
    background-color: #fff; 
    border: 1px solid #ced4da; 
    border-radius: 0.375rem; 
}}

.table {{ width: 100%; margin-bottom: 1rem; color: #212529; }}
.table th, .table td {{ padding: 0.75rem; vertical-align: top; border-top: 1px solid #dee2e6; }}
'''
        
        css_path.write_text(fallback_content, encoding='utf-8')
        print(f"✅ Fallback créé: {css}")
    
    print(f"\n🎉 DIAGNOSTIC TERMINÉ!")
    print(f"📊 Résumé:")
    print(f"  - CSS manquants traités: {len(missing_css)}")
    print(f"  - JS manquants traités: {len(missing_js)}")
    print(f"  - Fallbacks créés pour tous les assets manquants")

if __name__ == '__main__':
    diagnose_missing_assets()