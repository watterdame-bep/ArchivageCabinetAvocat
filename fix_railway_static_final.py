#!/usr/bin/env python3
"""
Script final pour résoudre définitivement les problèmes de fichiers statiques sur Railway
"""

import os
import sys
import subprocess
from pathlib import Path

def create_railway_build_script():
    """Crée un script de build spécifique pour Railway"""
    print("🔧 Création du script de build Railway...")
    
    build_script = """#!/bin/bash
# Script de build Railway pour Cabinet Avocat

echo "🚀 Début du build Railway"

# Activer l'environnement virtuel
source /opt/venv/bin/activate

# Vérifier les variables d'environnement
echo "📊 Variables d'environnement:"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DEBUG: $DEBUG"

# Définir les settings de production
export DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production

# Collecter les fichiers statiques avec verbose
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput --clear --verbosity=2

# Vérifier que les fichiers ont été collectés
echo "🔍 Vérification des fichiers collectés:"
ls -la staticfiles/ || echo "❌ Dossier staticfiles non trouvé"
ls -la staticfiles/css/ || echo "❌ Dossier staticfiles/css non trouvé"
ls -la staticfiles/assets/ || echo "❌ Dossier staticfiles/assets non trouvé"

echo "✅ Build Railway terminé"
"""
    
    with open('build_railway.sh', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # Rendre le script exécutable
    os.chmod('build_railway.sh', 0o755)
    print("✅ Script build_railway.sh créé")

def update_nixpacks_config():
    """Met à jour la configuration nixpacks pour être plus robuste"""
    print("🔧 Mise à jour de nixpacks.toml...")
    
    nixpacks_content = """[phases.setup]
nixPkgs = ['python311', 'gcc', 'pkg-config']

[phases.install]
cmds = [
    'python -m venv --copies /opt/venv',
    '. /opt/venv/bin/activate && pip install --upgrade pip',
    '. /opt/venv/bin/activate && pip install -r requirements.txt'
]

[phases.build]
cmds = [
    '. /opt/venv/bin/activate && export DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production',
    '. /opt/venv/bin/activate && python manage.py collectstatic --noinput --clear --verbosity=2',
    'ls -la staticfiles/ || echo "Staticfiles directory not found"',
    'ls -la staticfiles/css/ || echo "CSS directory not found"'
]

[start]
cmd = '. /opt/venv/bin/activate && python start_railway.py'
"""
    
    with open('nixpacks.toml', 'w', encoding='utf-8') as f:
        f.write(nixpacks_content)
    
    print("✅ nixpacks.toml mis à jour avec diagnostics")

def create_railway_json():
    """Crée/met à jour railway.json avec configuration optimale"""
    print("🔧 Création de railway.json...")
    
    railway_config = """{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "nixpacks",
    "buildCommand": "python manage.py collectstatic --noinput --clear --settings=CabinetAvocat.settings_production"
  },
  "deploy": {
    "startCommand": "python start_railway.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}"""
    
    with open('railway.json', 'w', encoding='utf-8') as f:
        f.write(railway_config)
    
    print("✅ railway.json créé avec configuration optimale")

def verify_whitenoise_config():
    """Vérifie et optimise la configuration WhiteNoise"""
    print("🔧 Vérification de la configuration WhiteNoise...")
    
    settings_file = Path('CabinetAvocat/settings_production.py')
    if not settings_file.exists():
        print("❌ settings_production.py non trouvé")
        return False
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier que WhiteNoise est bien configuré
    whitenoise_checks = [
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'STATICFILES_STORAGE',
        'WHITENOISE_USE_FINDERS = True',
        'WHITENOISE_AUTOREFRESH = True'
    ]
    
    all_good = True
    for check in whitenoise_checks:
        if check in content:
            print(f"  ✅ {check}")
        else:
            print(f"  ❌ {check} manquant")
            all_good = False
    
    return all_good

def create_static_test_endpoint():
    """Crée un endpoint de test pour vérifier les fichiers statiques"""
    print("🔧 Création d'un endpoint de test pour les fichiers statiques...")
    
    test_view = """
# Ajouter à urls.py pour tester les fichiers statiques
from django.http import JsonResponse
from django.conf import settings
import os

def test_static_files(request):
    \"\"\"Endpoint pour tester la disponibilité des fichiers statiques\"\"\"
    static_root = settings.STATIC_ROOT
    
    test_files = [
        'css/style.css',
        'css/vendors_css.css',
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css'
    ]
    
    results = {}
    for file_path in test_files:
        full_path = os.path.join(static_root, file_path)
        results[file_path] = {
            'exists': os.path.exists(full_path),
            'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0,
            'full_path': full_path
        }
    
    return JsonResponse({
        'static_root': static_root,
        'static_url': settings.STATIC_URL,
        'files': results
    })

# Ajouter cette ligne à urlpatterns:
# path('test-static/', test_static_files, name='test_static'),
"""
    
    with open('test_static_endpoint.py', 'w', encoding='utf-8') as f:
        f.write(test_view)
    
    print("✅ Endpoint de test créé dans test_static_endpoint.py")

def create_deployment_checklist():
    """Crée une checklist de déploiement"""
    print("📋 Création de la checklist de déploiement...")
    
    checklist = """# 🚀 Checklist Déploiement Railway - Cabinet Avocat

## ✅ Pré-déploiement (Local)

### 1. Vérifications des fichiers
- [ ] `nixpacks.toml` mis à jour avec diagnostics
- [ ] `railway.json` configuré avec buildCommand
- [ ] `start_railway.py` contient collectstatic
- [ ] `settings_production.py` WhiteNoise configuré
- [ ] `urls.py` sert les fichiers statiques en production

### 2. Test local
```bash
# Tester collectstatic local
python manage.py collectstatic --noinput --clear --settings=CabinetAvocat.settings_production

# Vérifier les fichiers critiques
ls staticfiles/css/style.css
ls staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css
```

## 🚀 Déploiement Railway

### 1. Push des modifications
```bash
git add .
git commit -m "Fix Railway static files with enhanced build configuration"
git push origin main
```

### 2. Variables Railway à vérifier
- [ ] `DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production`
- [ ] `DEBUG=False`
- [ ] Variables MySQL (auto-générées)
- [ ] `SECRET_KEY` (généré)

### 3. Surveillance du déploiement
- [ ] Logs Railway: "Collection des fichiers statiques..."
- [ ] Logs Railway: "X static files copied"
- [ ] Logs Railway: "MySQL est disponible!"
- [ ] Logs Railway: "Starting gunicorn"

## 🧪 Tests post-déploiement

### 1. Tests d'interface
- [ ] Page de login s'affiche correctement
- [ ] CSS Bootstrap chargé (design correct)
- [ ] Pas d'erreurs 404 dans la console navigateur

### 2. Tests d'URLs directes
```
https://votre-app.up.railway.app/static/css/style.css
https://votre-app.up.railway.app/static/assets/vendor_components/bootstrap/dist/css/bootstrap.css
https://votre-app.up.railway.app/test-static/ (si endpoint ajouté)
```

### 3. Tests fonctionnels
- [ ] Login utilisateur fonctionne
- [ ] Navigation dans l'application
- [ ] Génération de rapports (après upload JSReport)

## 🚨 Dépannage si problème persiste

### 1. Forcer un rebuild complet
```bash
# Dans Railway Dashboard
Settings > Deployments > Redeploy (force rebuild)
```

### 2. Vérifier les logs Railway
- Rechercher "collectstatic" dans les logs de build
- Vérifier qu'aucune erreur n'apparaît pendant la collection
- S'assurer que les fichiers sont bien copiés

### 3. Debug avancé
- Ajouter l'endpoint de test `/test-static/`
- Vérifier les variables d'environnement Railway
- Tester avec `WHITENOISE_AUTOREFRESH = True`

## 📞 Support
Si le problème persiste après toutes ces étapes, le problème peut venir de:
1. Configuration Railway spécifique
2. Problème de cache Railway
3. Configuration réseau Railway

Dans ce cas, contacter le support Railway avec les logs de build.
"""
    
    with open('RAILWAY_DEPLOYMENT_CHECKLIST.md', 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print("✅ Checklist créée: RAILWAY_DEPLOYMENT_CHECKLIST.md")

def run_final_collectstatic():
    """Exécute collectstatic final pour vérifier que tout fonctionne"""
    print("📁 Test final de collectstatic...")
    
    try:
        # Nettoyer d'abord
        if Path('staticfiles').exists():
            import shutil
            shutil.rmtree('staticfiles')
            print("🗑️ Dossier staticfiles nettoyé")
        
        # Exécuter collectstatic
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear', '--verbosity=2',
            '--settings=CabinetAvocat.settings_production'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ collectstatic final réussi")
            
            # Vérifier les fichiers critiques
            critical_files = [
                'staticfiles/css/style.css',
                'staticfiles/css/vendors_css.css',
                'staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css'
            ]
            
            all_present = True
            for file_path in critical_files:
                if Path(file_path).exists():
                    size = Path(file_path).stat().st_size
                    print(f"  ✅ {file_path} ({size} bytes)")
                else:
                    print(f"  ❌ {file_path} MANQUANT")
                    all_present = False
            
            return all_present
        else:
            print(f"❌ Erreur collectstatic: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test collectstatic: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Correction finale des fichiers statiques Railway\n")
    
    # Étapes de correction
    steps = [
        ("Mise à jour nixpacks.toml", update_nixpacks_config),
        ("Création railway.json", create_railway_json),
        ("Script de build Railway", create_railway_build_script),
        ("Vérification WhiteNoise", verify_whitenoise_config),
        ("Endpoint de test", create_static_test_endpoint),
        ("Test collectstatic final", run_final_collectstatic),
        ("Checklist déploiement", create_deployment_checklist),
    ]
    
    all_success = True
    for name, func in steps:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            if not func():
                all_success = False
        except Exception as e:
            print(f"❌ Erreur: {e}")
            all_success = False
    
    # Résumé final
    print("\n" + "="*60)
    print("📋 RÉSUMÉ FINAL")
    print("="*60)
    
    if all_success:
        print("🎉 SUCCÈS: Toutes les corrections ont été appliquées!")
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("  1. git add .")
        print("  2. git commit -m 'Fix Railway static files with enhanced build configuration'")
        print("  3. git push origin main")
        print("  4. Surveiller les logs Railway")
        print("  5. Tester l'interface après déploiement")
        print("\n📖 Consultez RAILWAY_DEPLOYMENT_CHECKLIST.md pour le guide complet")
    else:
        print("❌ ÉCHEC: Certaines corrections ont échoué")
        print("🔧 Veuillez corriger les erreurs ci-dessus avant de déployer")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)