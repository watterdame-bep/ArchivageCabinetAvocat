#!/usr/bin/env python
"""
Correction des problèmes d'encodage - Remplacer é par é
"""
import os
import re
from pathlib import Path

def fix_encoding_in_file(file_path):
    """Corriger l'encodage dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les occurrences avant correction
        count_before = content.count('é')
        
        if count_before > 0:
            # Remplacer é par é
            content = content.replace('é', 'é')
            
            # Autres corrections d'encodage courantes
            content = content.replace('è', 'è')
            content = content.replace('ô', 'ô')
            content = content.replace(''', "'")
            content = content.replace(''', "'")
            content = content.replace('"', '"')
            content = content.replace(''', '"')
            content = content.replace('à', 'à')
            content = content.replace('â', 'â')
            content = content.replace('ù', 'ù')
            content = content.replace('ô', 'ô')
            content = content.replace('è', 'è')
            content = content.replace('é', 'é')
            content = content.replace('ê', 'ê')
            content = content.replace('ë', 'ë')
            content = content.replace('ì', 'ì')
            content = content.replace('í', 'í')
            content = content.replace('î', 'î')
            content = content.replace('ï', 'ï')
            
            # Écrire le fichier corrigé
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return count_before
        
        return 0
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {file_path}: {e}")
        return 0

def fix_encoding_in_templates():
    """Corriger l'encodage dans tous les templates"""
    print("🔤 CORRECTION DES PROBLÈMES D'ENCODAGE DANS LES TEMPLATES")
    print("=" * 60)
    
    templates_dir = Path('templates')
    if not templates_dir.exists():
        print("❌ Dossier templates non trouvé")
        return False
    
    # Trouver tous les fichiers HTML
    html_files = list(templates_dir.rglob('*.html'))
    
    print(f"📁 Fichiers HTML trouvés: {len(html_files)}")
    print("-" * 50)
    
    total_corrections = 0
    files_corrected = 0
    
    for html_file in html_files:
        corrections = fix_encoding_in_file(html_file)
        if corrections > 0:
            files_corrected += 1
            total_corrections += corrections
            print(f"✅ {html_file}: {corrections} corrections")
        else:
            print(f"ℹ️ {html_file}: aucune correction nécessaire")
    
    print("-" * 50)
    print(f"📊 RÉSUMÉ:")
    print(f"  📄 Fichiers traités: {len(html_files)}")
    print(f"  📄 Fichiers corrigés: {files_corrected}")
    print(f"  🔤 Total corrections: {total_corrections}")
    
    return total_corrections > 0

def fix_encoding_in_python_files():
    """Corriger l'encodage dans les fichiers Python"""
    print("\n🐍 CORRECTION DES PROBLÈMES D'ENCODAGE DANS LES FICHIERS PYTHON")
    print("=" * 60)
    
    # Trouver tous les fichiers Python
    python_files = list(Path('.').rglob('*.py'))
    
    # Exclure certains dossiers
    excluded_dirs = ['envir', '.git', '__pycache__', 'venv', 'env']
    python_files = [f for f in python_files if not any(excluded in str(f) for excluded in excluded_dirs)]
    
    print(f"📁 Fichiers Python trouvés: {len(python_files)}")
    print("-" * 50)
    
    total_corrections = 0
    files_corrected = 0
    
    for py_file in python_files:
        corrections = fix_encoding_in_file(py_file)
        if corrections > 0:
            files_corrected += 1
            total_corrections += corrections
            print(f"✅ {py_file}: {corrections} corrections")
    
    if files_corrected == 0:
        print("ℹ️ Aucune correction nécessaire dans les fichiers Python")
    
    print("-" * 50)
    print(f"📊 RÉSUMÉ:")
    print(f"  📄 Fichiers traités: {len(python_files)}")
    print(f"  📄 Fichiers corrigés: {files_corrected}")
    print(f"  🔤 Total corrections: {total_corrections}")
    
    return total_corrections > 0

def fix_encoding_in_css_files():
    """Corriger l'encodage dans les fichiers CSS"""
    print("\n🎨 CORRECTION DES PROBLÈMES D'ENCODAGE DANS LES FICHIERS CSS")
    print("=" * 60)
    
    # Trouver tous les fichiers CSS
    css_files = []
    for css_dir in ['static/css', 'staticfiles/css']:
        css_path = Path(css_dir)
        if css_path.exists():
            css_files.extend(list(css_path.rglob('*.css')))
    
    print(f"📁 Fichiers CSS trouvés: {len(css_files)}")
    print("-" * 50)
    
    total_corrections = 0
    files_corrected = 0
    
    for css_file in css_files:
        corrections = fix_encoding_in_file(css_file)
        if corrections > 0:
            files_corrected += 1
            total_corrections += corrections
            print(f"✅ {css_file}: {corrections} corrections")
    
    if files_corrected == 0:
        print("ℹ️ Aucune correction nécessaire dans les fichiers CSS")
    
    print("-" * 50)
    print(f"📊 RÉSUMÉ:")
    print(f"  📄 Fichiers traités: {len(css_files)}")
    print(f"  📄 Fichiers corrigés: {files_corrected}")
    print(f"  🔤 Total corrections: {total_corrections}")
    
    return total_corrections > 0

def validate_encoding_fixes():
    """Valider que toutes les corrections ont été appliquées"""
    print("\n🔍 VALIDATION DES CORRECTIONS D'ENCODAGE")
    print("=" * 60)
    
    # Chercher les caractères problématiques restants
    problematic_chars = ['é', 'è', 'ô', ''', ''', 'à', 'â']
    
    all_files = []
    
    # Templates
    templates_dir = Path('templates')
    if templates_dir.exists():
        all_files.extend(list(templates_dir.rglob('*.html')))
    
    # Fichiers Python
    python_files = list(Path('.').rglob('*.py'))
    excluded_dirs = ['envir', '.git', '__pycache__', 'venv', 'env']
    python_files = [f for f in python_files if not any(excluded in str(f) for excluded in excluded_dirs)]
    all_files.extend(python_files)
    
    # Fichiers CSS
    for css_dir in ['static/css', 'staticfiles/css']:
        css_path = Path(css_dir)
        if css_path.exists():
            all_files.extend(list(css_path.rglob('*.css')))
    
    remaining_issues = 0
    files_with_issues = []
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for char in problematic_chars:
                if char in content:
                    count = content.count(char)
                    remaining_issues += count
                    if file_path not in files_with_issues:
                        files_with_issues.append(file_path)
                    print(f"⚠️ {file_path}: {count}x '{char}'")
        
        except Exception as e:
            print(f"❌ Erreur lors de la validation de {file_path}: {e}")
    
    print("-" * 50)
    if remaining_issues == 0:
        print("✅ VALIDATION RÉUSSIE: Aucun problème d'encodage détecté")
        return True
    else:
        print(f"⚠️ PROBLÈMES RESTANTS: {remaining_issues} caractères dans {len(files_with_issues)} fichiers")
        return False

def main():
    """Fonction principale de correction d'encodage"""
    print("🎯 CORRECTION COMPLÈTE DES PROBLÈMES D'ENCODAGE")
    print("🏢 Cabinet d'Avocats - Django Railway")
    print("=" * 70)
    
    tasks = [
        ("Templates HTML", fix_encoding_in_templates),
        ("Fichiers Python", fix_encoding_in_python_files),
        ("Fichiers CSS", fix_encoding_in_css_files),
    ]
    
    total_corrections = 0
    
    for name, task_func in tasks:
        try:
            result = task_func()
            if result:
                total_corrections += 1
                print(f"\n✅ {name} - CORRIGÉ")
            else:
                print(f"\n✅ {name} - AUCUNE CORRECTION NÉCESSAIRE")
        except Exception as e:
            print(f"\n❌ {name} - ERREUR: {e}")
    
    # Validation finale
    validation_success = validate_encoding_fixes()
    
    print("\n" + "=" * 70)
    print(f"🎯 CORRECTION D'ENCODAGE TERMINÉE")
    
    if validation_success:
        print("🎉 TOUS LES PROBLÈMES D'ENCODAGE RÉSOLUS!")
        print("✨ Tous les caractères é ont été remplacés par é!")
        print("\n📋 CORRECTIONS APPLIQUÉES:")
        print("  ✅ Templates HTML corrigés")
        print("  ✅ Fichiers Python corrigés")
        print("  ✅ Fichiers CSS corrigés")
        print("  ✅ Validation réussie")
        return True
    else:
        print("⚠️ Certains problèmes d'encodage persistent")
        print("🔧 Vérifiez les fichiers signalés et corrigez manuellement si nécessaire")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)