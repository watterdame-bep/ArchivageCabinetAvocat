#!/usr/bin/env python3
"""
Script de démarrage robuste pour Railway
Attend que MySQL soit prêt avant de lancer Django
"""

import os
import sys
import time
import subprocess
import pymysql
from urllib.parse import urlparse

def wait_for_mysql(database_url, max_attempts=30, delay=2):
    """Attend que MySQL soit disponible"""
    print("🔍 Vérification de la disponibilité MySQL...")
    
    # Parser l'URL de la base de données
    try:
        parsed = urlparse(database_url)
        host = parsed.hostname
        port = parsed.port or 3306
        user = parsed.username
        password = parsed.password
        database = parsed.path.lstrip('/')
        
        print(f"📊 Connexion à MySQL: {user}@{host}:{port}/{database}")
    except Exception as e:
        print(f"❌ Erreur parsing DATABASE_URL: {e}")
        return False
    
    for attempt in range(max_attempts):
        try:
            print(f"Tentative {attempt + 1}/{max_attempts} de connexion à MySQL...")
            
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connect_timeout=10,
                charset='utf8mb4'
            )
            connection.close()
            print("✅ MySQL est disponible!")
            return True
            
        except Exception as e:
            print(f"❌ MySQL pas encore prêt: {e}")
            if attempt < max_attempts - 1:
                print(f"⏳ Attente {delay} secondes...")
                time.sleep(delay)
            else:
                print("🚨 Timeout: MySQL n'est pas disponible")
                return False
    
    return False

def run_django_command(command):
    """Exécute une commande Django"""
    print(f"🚀 Exécution: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Erreur lors de l'exécution: {command}")
        sys.exit(result.returncode)
    print(f"✅ Succès: {command}")

def main():
    """Fonction principale de démarrage"""
    print("🚀 Démarrage de l'application Cabinet Avocat sur Railway")
    
    # Vérifier les variables d'environnement
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL non définie")
        print("🔍 Variables disponibles:")
        for key in os.environ:
            if 'MYSQL' in key or 'DATABASE' in key:
                print(f"  {key}={os.environ[key][:50]}...")
        sys.exit(1)
    
    print(f"📊 DATABASE_URL configurée: {database_url[:50]}...")
    
    # Attendre que MySQL soit prêt
    if not wait_for_mysql(database_url):
        print("🚨 Impossible de se connecter à MySQL")
        sys.exit(1)
    
    # Exécuter les migrations
    print("📋 Exécution des migrations...")
    run_django_command("python manage.py migrate --noinput")
    
    # Collecter les fichiers statiques (optionnel, déjà fait au build)
    print("📁 Collection des fichiers statiques...")
    run_django_command("python manage.py collectstatic --noinput")
    
    # Démarrer Gunicorn
    port = os.environ.get('PORT', '8000')
    print(f"🌐 Démarrage de Gunicorn sur le port {port}...")
    
    gunicorn_cmd = f"gunicorn CabinetAvocat.wsgi --bind 0.0.0.0:{port} --workers 2 --timeout 120"
    print(f"🚀 Commande: {gunicorn_cmd}")
    
    # Exécuter Gunicorn (ne retourne pas)
    os.execvp("gunicorn", [
        "gunicorn", 
        "CabinetAvocat.wsgi",
        "--bind", f"0.0.0.0:{port}",
        "--workers", "2",
        "--timeout", "120",
        "--log-level", "info"
    ])

if __name__ == "__main__":
    main()