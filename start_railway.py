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

def wait_for_mysql_individual_vars(max_attempts=30, delay=2):
    """Attend que MySQL soit disponible en utilisant les variables individuelles"""
    print("🔍 Vérification de la disponibilité MySQL (variables individuelles)...")
    
    # Récupérer les variables MySQL Railway
    host = os.environ.get('MYSQLHOST')
    port = int(os.environ.get('MYSQLPORT', '3306'))
    user = os.environ.get('MYSQLUSER')
    password = os.environ.get('MYSQLPASSWORD')
    database = os.environ.get('MYSQLDATABASE')
    
    if not all([host, user, password, database]):
        print("❌ Variables MySQL manquantes:")
        print(f"  MYSQLHOST: {host}")
        print(f"  MYSQLUSER: {user}")
        print(f"  MYSQLPASSWORD: {'***' if password else 'MANQUANT'}")
        print(f"  MYSQLDATABASE: {database}")
        print(f"  MYSQLPORT: {port}")
        return False
    
    print(f"📊 Connexion à MySQL: {user}@{host}:{port}/{database}")
    
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
    
    # CRITIQUE: Forcer l'utilisation de settings_production.py sur Railway
    os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
    print("✅ Utilisation forcée de settings_production.py")
    
    # Vérifier les variables d'environnement MySQL
    mysql_vars = ['MYSQLHOST', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLDATABASE', 'MYSQLPORT']
    missing_vars = []
    
    print("🔍 Vérification des variables MySQL Railway:")
    for var in mysql_vars:
        value = os.environ.get(var)
        if value:
            if 'PASSWORD' in var:
                print(f"  ✅ {var}=***")
            else:
                print(f"  ✅ {var}={value}")
        else:
            print(f"  ❌ {var}=MANQUANT")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables MySQL manquantes: {missing_vars}")
        print("🔍 Variables disponibles:")
        for key in sorted(os.environ.keys()):
            if 'MYSQL' in key or 'DATABASE' in key:
                value = os.environ[key]
                if 'PASSWORD' in key:
                    print(f"  {key}=***")
                else:
                    print(f"  {key}={value[:50]}...")
        sys.exit(1)
    
    # Attendre que MySQL soit prêt
    if not wait_for_mysql_individual_vars():
        print("🚨 Impossible de se connecter à MySQL")
        sys.exit(1)
    
    # Exécuter les migrations
    print("📋 Exécution des migrations...")
    run_django_command("python manage.py migrate --noinput --settings=CabinetAvocat.settings_production")
    
    # Collecter les fichiers statiques (CRITIQUE pour Railway)
    print("📁 Collection des fichiers statiques...")
    run_django_command("python manage.py collectstatic --noinput --clear --settings=CabinetAvocat.settings_production")
    
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