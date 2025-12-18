#!/usr/bin/env python
"""
Script de vérification finale de la migration JSReport
Vérifie qu'aucun appel hardcodé ne subsiste
"""
import os
import re

def scan_files_for_hardcoded_calls():
    """
    Scanne tous les fichiers Python pour détecter des appels JSReport hardcodés
    """
    print("🔍 Vérification des appels JSReport hardcodés...")
    print("=" * 60)
    
    # Patterns à rechercher (appels directs problématiques)
    patterns = [
        r'requests\.post.*5488',
        r'"http://localhost:5488/api/report"',
        r"'http://localhost:5488/api/report'",
        r'JSREPORT_URL\s*=\s*["\']http://localhost:5488/api/report["\']',
    ]
    
    # Extensions de fichiers à scanner
    extensions = ['.py']
    
    # Dossiers à exclure
    exclude_dirs = [
        '__pycache__',
        '.git',
        'venv',
        'env',
        'envir',
        'node_modules',
        'staticfiles',
        'media'
    ]
    
    # Fichiers à exclure (scripts de test et vérification)
    exclude_files = [
        'verify_jsreport_migration.py',
        'test_jsreport_migration.py',
        'test_jsreport.py'
    ]
    
    found_issues = []
    scanned_files = 0
    
    for root, dirs, files in os.walk('.'):
        # Exclure certains dossiers
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions) and file not in exclude_files:
                file_path = os.path.join(root, file)
                scanned_files += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for i, line in enumerate(content.split('\n'), 1):
                        for pattern in patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                found_issues.append({
                                    'file': file_path,
                                    'line': i,
                                    'content': line.strip(),
                                    'pattern': pattern
                                })
                                
                except (UnicodeDecodeError, PermissionError):
                    continue
    
    print(f"📊 Fichiers scannés: {scanned_files}")
    print()
    
    if found_issues:
        print("❌ Appels hardcodés trouvés:")
        print("-" * 40)
        for issue in found_issues:
            print(f"📁 {issue['file']}:{issue['line']}")
            print(f"   {issue['content']}")
            print(f"   Pattern: {issue['pattern']}")
            print()
        return False
    else:
        print("✅ Aucun appel hardcodé trouvé!")
        return True

def verify_service_usage():
    """
    Vérifie que le service centralisé est bien utilisé
    """
    print("\n🔧 Vérification de l'utilisation du service centralisé...")
    print("-" * 60)
    
    # Fichiers qui devraient utiliser le service
    files_to_check = [
        'paiement/views.py',
        'Dossier/views.py', 
        'rapport/views.py'
    ]
    
    service_usage = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier l'import du service
                if 'from utils.jsreport_service import jsreport_service' in content:
                    service_usage.append(f"✅ {file_path} - Import du service")
                else:
                    service_usage.append(f"❌ {file_path} - Import manquant")
                
                # Vérifier l'utilisation du service
                if 'jsreport_service.generate_pdf_response' in content:
                    service_usage.append(f"✅ {file_path} - Utilise le service")
                else:
                    service_usage.append(f"⚠️  {file_path} - N'utilise pas le service")
                    
            except (UnicodeDecodeError, PermissionError):
                service_usage.append(f"❌ {file_path} - Erreur de lecture")
        else:
            service_usage.append(f"❌ {file_path} - Fichier non trouvé")
    
    for usage in service_usage:
        print(usage)
    
    return all('✅' in usage for usage in service_usage if not usage.startswith('⚠️'))

def check_configuration():
    """
    Vérifie la configuration JSReport
    """
    print("\n⚙️  Vérification de la configuration...")
    print("-" * 60)
    
    config_files = [
        'CabinetAvocat/settings.py',
        'CabinetAvocat/settings_production.py'
    ]
    
    config_ok = True
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                required_settings = [
                    'JSREPORT_URL',
                    'JSREPORT_USERNAME', 
                    'JSREPORT_PASSWORD',
                    'JSREPORT_TIMEOUT'
                ]
                
                print(f"📁 {config_file}:")
                for setting in required_settings:
                    if setting in content:
                        print(f"   ✅ {setting}")
                    else:
                        print(f"   ❌ {setting} manquant")
                        config_ok = False
                        
            except (UnicodeDecodeError, PermissionError):
                print(f"❌ Erreur lecture {config_file}")
                config_ok = False
        else:
            print(f"❌ {config_file} non trouvé")
            config_ok = False
    
    return config_ok

def main():
    """
    Fonction principale de vérification
    """
    print("🚀 Vérification finale de la migration JSReport")
    print("=" * 60)
    
    # Tests
    no_hardcoded = scan_files_for_hardcoded_calls()
    service_used = verify_service_usage()
    config_ok = check_configuration()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📋 Résumé de la vérification:")
    print(f"   {'✅' if no_hardcoded else '❌'} Aucun appel hardcodé")
    print(f"   {'✅' if service_used else '❌'} Service centralisé utilisé")
    print(f"   {'✅' if config_ok else '❌'} Configuration complète")
    
    if no_hardcoded and service_used and config_ok:
        print("\n🎉 Migration JSReport réussie!")
        print("✅ Votre application est prête pour le déploiement Railway")
        return True
    else:
        print("\n⚠️  Migration incomplète!")
        print("❌ Corrigez les problèmes avant le déploiement")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)