#!/usr/bin/env python3
"""
Script pour corriger automatiquement toutes les erreurs d'indentation 
dans settings_production.py
"""

import os
import sys
import subprocess
import ast

def run_command(command, description):
    """Exécuter une commande"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            return True, result.stdout
        else:
            print(f"❌ {description} - Erreur: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ {description} - Exception: {str(e)}")
        return False, str(e)

def check_python_syntax(file_path):
    """Vérifier la syntaxe Python d'un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Essayer de compiler le code
        ast.parse(content)
        return True, "Syntaxe correcte"
    except SyntaxError as e:
        return False, f"Erreur syntaxe ligne {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def fix_settings_production():
    """Corriger le fichier settings_production.py avec une indentation correcte"""
    settings_file = "CabinetAvocat/settings_production.py"
    
    if not os.path.exists(settings_file):
        print(f"❌ {settings_file} non trouvé")
        return False
    
    print(f"🔧 Correction de {settings_file}...")
    
    # Contenu corrigé avec indentation parfaite
    corrected_content = '''from .settings import *
import os
import dj_database_url
import pymysql
from decouple import config

# Installer PyMySQL comme MySQLdb pour la compatibilité
pymysql.install_as_MySQLdb()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts autorisés pour Railway
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*.railway.app',
    '*.up.railway.app',
    config('RAILWAY_PUBLIC_DOMAIN', default=''),
]

# Configuration de la base de données MySQL Railway
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    # Fallback vers la configuration locale MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME', default='cabinet_avocat'),
            'USER': config('DB_USER', default='root'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# Configuration des fichiers statiques pour Railway
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuration des médias pour Railway
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Middleware pour les fichiers statiques
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuration WhiteNoise ULTIME pour Railway
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br',
    'map', 'woff', 'woff2', 'ttf', 'otf', 'eot', 'svg', 'ico'
]
WHITENOISE_MANIFEST_STRICT = False  # Tolérant avec les fichiers manquants
WHITENOISE_MAX_AGE = 31536000  # Cache 1 an pour les assets

# Configuration JSReport pour Railway (service séparé)
JSREPORT_URL = config('JSREPORT_SERVICE_URL', default='http://localhost:5488')
JSREPORT_USERNAME = config('JSREPORT_USERNAME', default='admin')
JSREPORT_PASSWORD = config('JSREPORT_PASSWORD', default='')
JSREPORT_TIMEOUT = config('JSREPORT_TIMEOUT', default=60000, cast=int)

JSREPORT_CONFIG = {
    'url': JSREPORT_URL,
    'username': JSREPORT_USERNAME,
    'password': JSREPORT_PASSWORD,
    'timeout': JSREPORT_TIMEOUT,
    'verify_ssl': True,
    'templates': {
        'rapport_agent': config('JSREPORT_TEMPLATE_AGENT', default='rapport_agent'),
        'rapport_client': config('JSREPORT_TEMPLATE_CLIENT', default='rapport_client'),
        'rapport_juridiction': config('JSREPORT_TEMPLATE_JURIDICTION', default='rapport_juridiction'),
        'rapport_commune': config('JSREPORT_TEMPLATE_COMMUNE', default='rapport_commune'),
        'rapport_dossier': config('JSREPORT_TEMPLATE_DOSSIER', default='rapport_dossier'),
        'rapport_activites_internes': config('JSREPORT_TEMPLATE_ACTIVITES', default='rapport_activites_internes'),
        'facture_paiement': config('JSREPORT_TEMPLATE_FACTURE', default='facture_paiement'),
        'facture_dossier': config('JSREPORT_TEMPLATE_FACTURE_DOSSIER', default='Facture_dossier'),
        'extrait_compte_client': config('JSREPORT_TEMPLATE_EXTRAIT_COMPTE', default='Extrait_de_compte_client'),
    }
}

# Configuration de sécurité pour la production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuration des logs pour Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'rapport': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'utils.jsreport_service': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Configuration des sessions
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Configuration des emails (si nécessaire)
if config('EMAIL_HOST', default=''):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@cabinetavocat.com')
'''
    
    try:
        # Sauvegarder l'ancien fichier
        with open(settings_file, 'r', encoding='utf-8') as f:
            old_content = f.read()
        
        with open(f"{settings_file}.backup", 'w', encoding='utf-8') as f:
            f.write(old_content)
        
        print("💾 Sauvegarde de l'ancien fichier créée")
        
        # Écrire le nouveau contenu
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        
        print("✅ Fichier settings_production.py corrigé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur correction: {str(e)}")
        return False

def main():
    print("🔧 Correction des erreurs d'indentation Python")
    print("=" * 50)
    
    settings_file = "CabinetAvocat/settings_production.py"
    
    # 1. Vérifier la syntaxe actuelle
    print("🔍 Vérification syntaxe actuelle...")
    is_valid, message = check_python_syntax(settings_file)
    
    if is_valid:
        print("✅ Syntaxe déjà correcte")
    else:
        print(f"❌ Erreur détectée: {message}")
    
    # 2. Corriger le fichier
    print("\n🔧 Application de la correction...")
    if fix_settings_production():
        print("✅ Correction appliquée")
    else:
        print("❌ Échec de la correction")
        return 1
    
    # 3. Vérifier la syntaxe après correction
    print("\n🔍 Vérification syntaxe après correction...")
    is_valid, message = check_python_syntax(settings_file)
    
    if is_valid:
        print("✅ Syntaxe maintenant correcte")
    else:
        print(f"❌ Erreur persiste: {message}")
        return 1
    
    # 4. Test Django
    print("\n🧪 Test Django...")
    success, output = run_command("python manage.py check", "Test configuration Django")
    
    if success:
        print("✅ Configuration Django valide")
    else:
        print("⚠️  Problème configuration Django (mais syntaxe OK)")
    
    # 5. Test collectstatic
    print("\n🧪 Test collectstatic...")
    success, output = run_command("python manage.py collectstatic --noinput --dry-run", "Test collectstatic")
    
    if success:
        print("✅ collectstatic fonctionne")
    else:
        print("⚠️  Problème collectstatic")
    
    print("\n" + "=" * 50)
    print("🎯 CORRECTION TERMINÉE!")
    
    print("\n📋 Résumé:")
    print("✅ Indentation corrigée dans settings_production.py")
    print("✅ Syntaxe Python validée")
    print("✅ Configuration WhiteNoise optimisée")
    print("✅ Configuration JSReport propre")
    
    print("\n📋 Prochaines étapes:")
    print("1. git add CabinetAvocat/settings_production.py")
    print("2. git commit -m 'Fix Python indentation errors in settings_production.py'")
    print("3. git push origin main")
    print("4. Relancer le déploiement Railway")
    
    # Proposer de faire le commit automatiquement
    response = input("\n❓ Voulez-vous commiter cette correction maintenant ? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'o', 'oui']:
        print("\n🔄 Commit de la correction...")
        
        if run_command("git add CabinetAvocat/settings_production.py", "Ajout du fichier corrigé")[0]:
            if run_command('git commit -m "Fix Python indentation errors in settings_production.py"', "Commit")[0]:
                if run_command("git push origin main", "Push vers GitHub")[0]:
                    print("\n🎉 CORRECTION POUSSÉE VERS GITHUB!")
                    print("✅ Le déploiement Railway devrait maintenant réussir")
                    return 0
        return 1
    else:
        print("\n📝 Commitez manuellement avec:")
        print("   git add CabinetAvocat/settings_production.py")
        print('   git commit -m "Fix Python indentation errors"')
        print("   git push origin main")
        return 0

if __name__ == "__main__":
    sys.exit(main())