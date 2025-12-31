#!/usr/bin/env python3
"""
Script de démarrage simple pour Railway - Approche YouTube Tutorial
"""

import os
import sys
import subprocess

def main():
    """Fonction principale de démarrage simple"""
    print("🚀 Démarrage Cabinet Avocat sur Railway")
    
    # Forcer l'utilisation de settings_production.py
    os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
    
    # Migrations
    print("📋 Migrations...")
    subprocess.run(['python', 'manage.py', 'migrate', '--noinput'], check=True)
    
    # Collectstatic
    print("📁 Collectstatic...")
    subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], check=True)
    
    # Démarrer Gunicorn
    port = os.environ.get('PORT', '8000')
    print(f"🌐 Démarrage Gunicorn sur port {port}")
    
    os.execvp('gunicorn', [
        'gunicorn', 
        'CabinetAvocat.wsgi:application',
        '--bind', f'0.0.0.0:{port}'
    ])

if __name__ == "__main__":
    main()