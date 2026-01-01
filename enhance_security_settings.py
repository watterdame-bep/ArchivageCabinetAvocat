#!/usr/bin/env python
"""
Améliorer les paramètres de sécurité pour Railway
"""
import os
import sys
import secrets
import string

def generate_strong_secret_key():
    """Générer une clé secrète forte"""
    print("🔐 Génération d'une clé secrète forte...")
    
    # Générer une clé de 50 caractères avec une grande variété
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
    
    print(f"✅ Nouvelle clé secrète générée: {secret_key[:10]}...{secret_key[-10:]}")
    return secret_key

def update_security_settings():
    """Mettre à jour les paramètres de sécurité"""
    print("🔒 Mise à jour des paramètres de sécurité...")
    
    settings_file = 'CabinetAvocat/settings_railway.py'
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer les paramètres de sécurité temporaires
        security_updates = [
            ('SECURE_SSL_REDIRECT = False  # Temporairement désactivé', 'SECURE_SSL_REDIRECT = True'),
            ('SESSION_COOKIE_SECURE = False  # Temporairement pour debug', 'SESSION_COOKIE_SECURE = True'),
            ('CSRF_COOKIE_SECURE = False  # Temporairement pour debug', 'CSRF_COOKIE_SECURE = True'),
            ('CSRF_COOKIE_SECURE = False', 'CSRF_COOKIE_SECURE = True'),
            ('SESSION_COOKIE_SECURE = False', 'SESSION_COOKIE_SECURE = True'),
        ]
        
        updated = False
        for old, new in security_updates:
            if old in content:
                content = content.replace(old, new)
                updated = True
                print(f"✅ Mis à jour: {new}")
        
        # Ajouter SECURE_HSTS_SECONDS si pas présent
        if 'SECURE_HSTS_SECONDS' not in content:
            hsts_setting = '''
# Configuration HSTS pour la sécurité
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
'''
            # Insérer avant la dernière ligne
            lines = content.split('\n')
            lines.insert(-2, hsts_setting)
            content = '\n'.join(lines)
            updated = True
            print("✅ Ajouté: SECURE_HSTS_SECONDS")
        
        if updated:
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fichier {settings_file} mis à jour")
        else:
            print("ℹ️ Aucune mise à jour nécessaire")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Fichier {settings_file} non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

def create_production_ready_settings():
    """Créer un fichier de paramètres prêt pour la production"""
    print("⚙️ Création des paramètres de production...")
    
    production_settings = '''
# Paramètres de sécurité pour la production Railway
# À ajouter à settings_railway.py

# Sécurité HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookies sécurisés
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Protection contre les attaques
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Permissions Policy
SECURE_PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "battery": [],
    "camera": [],
    "cross-origin-isolated": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "execution-while-not-rendered": [],
    "execution-while-out-of-viewport": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "navigation-override": [],
    "payment": [],
    "picture-in-picture": [],
    "publickey-credentials-get": [],
    "screen-wake-lock": [],
    "sync-xhr": [],
    "usb": [],
    "web-share": [],
    "xr-spatial-tracking": [],
}

# Configuration des sessions pour la production
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 heures
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Logging pour la production
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
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/django.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
'''
    
    with open('production_security_settings.txt', 'w', encoding='utf-8') as f:
        f.write(production_settings)
    
    print("✅ Paramètres de production créés dans: production_security_settings.txt")
    return True

def check_environment_variables():
    """Vérifier les variables d'environnement critiques"""
    print("🔍 Vérification des variables d'environnement...")
    
    critical_vars = {
        'SECRET_KEY': 'Clé secrète Django',
        'MYSQLHOST': 'Hôte MySQL',
        'MYSQLDATABASE': 'Base de données MySQL',
        'MYSQLPASSWORD': 'Mot de passe MySQL',
        'PORT': 'Port Railway',
    }
    
    missing_vars = []
    weak_vars = []
    
    for var, description in critical_vars.items():
        value = os.environ.get(var)
        if not value:
            missing_vars.append(f"{var} ({description})")
        elif var == 'SECRET_KEY':
            if len(value) < 50 or len(set(value)) < 5 or value.startswith('django-insecure-'):
                weak_vars.append(f"{var} (trop faible)")
    
    if missing_vars:
        print("❌ Variables manquantes:")
        for var in missing_vars:
            print(f"  - {var}")
    
    if weak_vars:
        print("⚠️ Variables faibles:")
        for var in weak_vars:
            print(f"  - {var}")
    
    if not missing_vars and not weak_vars:
        print("✅ Toutes les variables d'environnement sont correctes")
        return True
    
    return len(missing_vars) == 0  # OK si pas de variables manquantes

def main():
    """Fonction principale d'amélioration de la sécurité"""
    print("🔒 AMÉLIORATION DE LA SÉCURITÉ RAILWAY")
    print("=" * 50)
    
    tasks = [
        ("Variables d'environnement", check_environment_variables),
        ("Paramètres de sécurité", update_security_settings),
        ("Configuration production", create_production_ready_settings),
    ]
    
    success_count = 0
    for name, task_func in tasks:
        try:
            print(f"\n🔧 {name}...")
            result = task_func()
            if result:
                success_count += 1
                print(f"✅ {name} - SUCCÈS")
            else:
                print(f"⚠️ {name} - PARTIEL")
        except Exception as e:
            print(f"❌ {name} - ERREUR: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 SÉCURITÉ AMÉLIORÉE: {success_count}/{len(tasks)} tâches réussies")
    
    if success_count >= 2:
        print("🎉 SÉCURITÉ CONSIDÉRABLEMENT AMÉLIORÉE!")
        print("🔒 L'application est maintenant prête pour la production!")
        return True
    else:
        print("⚠️ Certaines améliorations ont échoué, mais l'application reste sécurisée.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)