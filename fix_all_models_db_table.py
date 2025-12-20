#!/usr/bin/env python3
"""
Script pour ajouter automatiquement db_table à tous les modèles manquants
"""
import os
import re

def add_db_table_to_model(file_path, class_name, app_name):
    """Ajouter db_table à un modèle spécifique"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Calculer le nom de table en minuscules
    table_name = f"{app_name.lower()}_{class_name.lower()}"
    
    # Pattern pour trouver la classe et sa Meta (si elle existe)
    class_pattern = rf'class {class_name}\(.*?\):(.*?)(?=class|\Z)'
    
    match = re.search(class_pattern, content, re.DOTALL)
    if not match:
        print(f"  ❌ Classe {class_name} non trouvée")
        return False
    
    class_content = match.group(1)
    
    # Vérifier si db_table existe déjà
    if 'db_table' in class_content:
        print(f"  ✅ {class_name} a déjà db_table")
        return True
    
    # Chercher une classe Meta existante
    meta_pattern = r'class Meta:(.*?)(?=def|\Z|class [^M])'
    meta_match = re.search(meta_pattern, class_content, re.DOTALL)
    
    if meta_match:
        # Meta existe, ajouter db_table
        meta_content = meta_match.group(1)
        new_meta_content = f"class Meta:\n        db_table = '{table_name}'{meta_content}"
        
        # Remplacer dans le contenu complet
        old_meta = f"class Meta:{meta_content}"
        content = content.replace(old_meta, new_meta_content)
        
    else:
        # Pas de Meta, en créer une
        # Trouver la fin des champs (avant def ou class suivante)
        def_pattern = r'(    def __str__\(self\):.*?)(?=    def|\Z|class)'
        def_match = re.search(def_pattern, class_content, re.DOTALL)
        
        if def_match:
            # Insérer Meta avant __str__
            str_method = def_match.group(1)
            new_content = f"\n    class Meta:\n        db_table = '{table_name}'\n        verbose_name = '{class_name}'\n        verbose_name_plural = '{class_name}s'\n\n{str_method}"
            content = content.replace(str_method, new_content)
        else:
            print(f"  ⚠️ Structure non standard pour {class_name}")
            return False
    
    # Écrire le fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ {class_name} → {table_name}")
    return True

def process_app_models():
    """Traiter tous les modèles des apps"""
    
    models_to_fix = [
        # Dossier (modèles restants)
        ('CabinetAvocat/Dossier/models.py', [
            'ReductionTarifForfaitaire',
            'DeclarationDossier', 
            'AvocatDossier',
            'ActiviteHeure',
            'PieceDossier',
            'TypePiece'
        ], 'dossier'),
        
        # Paiement
        ('CabinetAvocat/paiement/models.py', [
            # À déterminer après lecture
        ], 'paiement'),
        
        # Parametre  
        ('CabinetAvocat/parametre/models.py', [
            # À déterminer après lecture
        ], 'parametre'),
    ]
    
    for file_path, class_names, app_name in models_to_fix:
        if not os.path.exists(file_path):
            print(f"❌ Fichier non trouvé: {file_path}")
            continue
            
        print(f"\n📁 App: {app_name}")
        print(f"📄 Fichier: {file_path}")
        
        for class_name in class_names:
            add_db_table_to_model(file_path, class_name, app_name)

if __name__ == '__main__':
    print("🔧 Correction automatique des db_table")
    print("=" * 45)
    
    # D'abord, finir manuellement les modèles Dossier restants
    print("\n📋 Modèles Dossier restants à corriger manuellement:")
    remaining_dossier_models = [
        'ReductionTarifForfaitaire',
        'DeclarationDossier', 
        'AvocatDossier',
        'ActiviteHeure',
        'PieceDossier',
        'TypePiece'
    ]
    
    for model in remaining_dossier_models:
        table_name = f"dossier_{model.lower()}"
        print(f"  - {model} → {table_name}")
    
    print("\n💡 Continuez manuellement avec ces modèles,")
    print("   puis nous traiterons les apps Paiement et Parametre")