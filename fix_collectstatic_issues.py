#!/usr/bin/env python3
"""
Script pour corriger les problèmes de collectstatic avec WhiteNoise
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Exécuter une commande"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            return True
        else:
            print(f"❌ {description} - Erreur: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {str(e)}")
        return False

def find_css_files_with_sourcemap_references():
    """Trouver les fichiers CSS qui référencent des sourcemaps manquants"""
    problematic_files = []
    
    # Dossiers à scanner
    static_dirs = ["static", "staticfiles"]
    
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    if file.endswith('.css'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if 'sourceMappingURL=' in content:
                                    # Extraire le nom du fichier .map
                                    lines = content.split('\n')
                                    for line in lines:
                                        if 'sourceMappingURL=' in line:
                                            # Extraire le nom du fichier .map
                                            map_file = line.split('sourceMappingURL=')[-1].strip().replace('*/', '').strip()
                                            map_path = os.path.join(os.path.dirname(file_path), map_file)
                                            
                                            if not os.path.exists(map_path):
                                                problematic_files.append((file_path, map_path, line))
                        except Exception as e:
                            print(f"⚠️  Erreur lecture {file_path}: {str(e)}")
    
    return problematic_files

def fix_css_sourcemap_references(problematic_files):
    """Corriger les références aux sourcemaps dans les fichiers CSS"""
    fixed_count = 0
    
    for css_file, map_file, sourcemap_line in problematic_files:
        print(f"🔧 Correction de {css_file}...")
        
        try:
            # Lire le contenu du fichier CSS
            with open(css_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Supprimer la ligne sourceMappingURL
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                if 'sourceMappingURL=' not in line:
                    new_lines.append(line)
                else:
                    print(f"   Suppression: {line.strip()}")
            
            # Réécrire le fichier
            new_content = '\n'.join(new_lines)
            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ {css_file} corrigé")
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ Erreur correction {css_file}: {str(e)}")
    
    return fixed_count

def create_missing_map_files(problematic_files):
    """Créer des fichiers .map vides pour les références manquantes"""
    created_count = 0
    
    for css_file, map_file, sourcemap_line in problematic_files:
        print(f"📄 Création de {map_file}...")
        
        try:
            # Créer le répertoire si nécessaire
            os.makedirs(os.path.dirname(map_file), exist_ok=True)
            
            # Créer un fichier .map vide mais valide
            map_content = '{"version":3,"sources":[],"names":[],"mappings":"","file":"' + os.path.basename(css_file) + '"}'
            
            with open(map_file, 'w', encoding='utf-8') as f:
                f.write(map_content)
            
            print(f"✅ {map_file} créé")
            created_count += 1
            
        except Exception as e:
            print(f"❌ Erreur création {map_file}: {str(e)}")
    
    return created_count

def update_whitenoise_settings():
    """Mettre à jour les settings pour être plus tolérant avec WhiteNoise"""
    settings_file = "CabinetAvocat/settings_production.py"
    
    if not os.path.exists(settings_file):
        print(f"❌ {settings_file} non trouvé")
        return False
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si la configuration WhiteNoise est déjà présente
        if 'WHITENOISE_SKIP_COMPRESS_EXTENSIONS' in content:
            print("✅ Configuration WhiteNoise déjà optimisée")
            return True
        
        # Ajouter la configuration WhiteNoise optimisée
        whitenoise_config = '''
# Configuration WhiteNoise optimisée pour Railway
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br', 'map']
WHITENOISE_MANIFEST_STRICT = False  # Plus tolérant avec les fichiers manquants
'''
        
        # Trouver où insérer la configuration
        if 'STATICFILES_STORAGE' in content:
            # Remplacer la ligne existante
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith('STATICFILES_STORAGE'):
                    new_lines.append('STATICFILES_STORAGE = \'whitenoise.storage.CompressedManifestStaticFilesStorage\'')
                    new_lines.append('WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [\'jpg\', \'jpeg\', \'png\', \'gif\', \'webp\', \'zip\', \'gz\', \'tgz\', \'bz2\', \'tbz\', \'xz\', \'br\', \'map\']')
                    new_lines.append('WHITENOISE_MANIFEST_STRICT = False  # Plus tolérant avec les fichiers manquants')
                else:
                    new_lines.append(line)
            content = '\n'.join(new_lines)
        else:
            # Ajouter à la fin
            content += whitenoise_config
        
        # Réécrire le fichier
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Configuration WhiteNoise mise à jour dans {settings_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur mise à jour settings: {str(e)}")
        return False

def main():
    print("🔧 Correction des problèmes collectstatic WhiteNoise")
    print("=" * 60)
    
    print("📋 Problème identifié:")
    print("❌ materialdesignicons.css.map manquant")
    print("❌ WhiteNoise échoue sur collectstatic")
    
    print("\n🔍 Recherche des fichiers CSS problématiques...")
    problematic_files = find_css_files_with_sourcemap_references()
    
    if not problematic_files:
        print("✅ Aucun fichier CSS avec sourcemap manquant trouvé")
    else:
        print(f"⚠️  {len(problematic_files)} fichier(s) CSS avec sourcemaps manquants:")
        for css_file, map_file, line in problematic_files:
            print(f"   {css_file} → {map_file}")
    
    print("\n📋 Choisissez la méthode de correction:")
    print("1. Supprimer les références sourcemap des CSS (recommandé)")
    print("2. Créer des fichiers .map vides")
    print("3. Les deux (plus sûr)")
    
    choice = input("\nVotre choix (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        print("\n🔧 Suppression des références sourcemap...")
        fixed_count = fix_css_sourcemap_references(problematic_files)
        print(f"✅ {fixed_count} fichier(s) CSS corrigé(s)")
    
    if choice in ['2', '3']:
        print("\n📄 Création des fichiers .map manquants...")
        created_count = create_missing_map_files(problematic_files)
        print(f"✅ {created_count} fichier(s) .map créé(s)")
    
    print("\n⚙️  Mise à jour de la configuration WhiteNoise...")
    update_whitenoise_settings()
    
    print("\n🧪 Test de collectstatic...")
    if run_command("python manage.py collectstatic --noinput --dry-run", "Test collectstatic"):
        print("✅ collectstatic devrait maintenant fonctionner")
    else:
        print("⚠️  collectstatic pourrait encore avoir des problèmes")
    
    print("\n" + "=" * 60)
    print("🎯 CORRECTIONS APPLIQUÉES!")
    
    print("\n📋 Prochaines étapes:")
    print("1. git add .")
    print("2. git commit -m 'Fix collectstatic WhiteNoise issues'")
    print("3. git push origin main")
    print("4. Relancer le déploiement Railway")
    
    # Proposer de faire le commit automatiquement
    response = input("\n❓ Voulez-vous commiter ces corrections maintenant ? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'o', 'oui']:
        print("\n🔄 Commit des corrections...")
        
        if run_command("git add .", "Ajout des fichiers"):
            if run_command('git commit -m "Fix collectstatic WhiteNoise sourcemap issues"', "Commit"):
                if run_command("git push origin main", "Push vers GitHub"):
                    print("\n🎉 CORRECTIONS POUSSÉES VERS GITHUB!")
                    print("✅ Le déploiement Railway devrait maintenant réussir")
                    return 0
        return 1
    else:
        print("\n📝 Commitez manuellement avec:")
        print("   git add .")
        print('   git commit -m "Fix collectstatic WhiteNoise issues"')
        print("   git push origin main")
        return 0

if __name__ == "__main__":
    sys.exit(main())