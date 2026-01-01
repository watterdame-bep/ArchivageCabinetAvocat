#!/usr/bin/env python
"""
Script pour injecter le CSS global dans les templates
"""
from pathlib import Path
import re

def inject_css_in_templates():
    """Injecter le CSS global dans les templates"""
    print("💉 Injection du CSS global dans les templates...")
    
    # Chercher les templates
    template_dirs = [
        Path('templates'),
        Path('*/templates'),
        Path('*/*/templates'),
    ]
    
    css_injection = '''
    <!-- CSS Global Railway Fixes -->
    <link rel="stylesheet" href="{% static 'css/railway-global-fixes.css' %}">
    <link rel="stylesheet" href="{% static 'css/railway-fixes.css' %}">
    <link rel="stylesheet" href="{% static 'css/media-fallback.css' %}">
    '''
    
    templates_found = []
    
    for pattern in template_dirs:
        for template_dir in Path('.').glob(str(pattern)):
            if template_dir.is_dir():
                for template_file in template_dir.rglob('*.html'):
                    templates_found.append(template_file)
    
    if not templates_found:
        print("⚠️ Aucun template trouvé")
        return
    
    # Chercher le template de base
    base_templates = [t for t in templates_found if 'base' in t.name.lower() or 'layout' in t.name.lower()]
    
    if base_templates:
        base_template = base_templates[0]
        print(f"📄 Template de base trouvé: {base_template}")
        
        try:
            content = base_template.read_text(encoding='utf-8')
            
            # Vérifier si le CSS n'est pas déjà injecté
            if 'railway-global-fixes.css' not in content:
                # Chercher la balise </head> et injecter avant
                if '</head>' in content:
                    content = content.replace('</head>', f'{css_injection}\n</head>')
                    base_template.write_text(content, encoding='utf-8')
                    print(f"✅ CSS injecté dans {base_template}")
                else:
                    print(f"⚠️ Balise </head> non trouvée dans {base_template}")
            else:
                print(f"✅ CSS déjà présent dans {base_template}")
                
        except Exception as e:
            print(f"❌ Erreur lors de l'injection dans {base_template}: {e}")
    
    else:
        print("⚠️ Aucun template de base trouvé")
        # Lister les templates trouvés
        print("📄 Templates disponibles:")
        for template in templates_found[:10]:  # Limiter à 10
            print(f"  - {template}")

if __name__ == '__main__':
    inject_css_in_templates()