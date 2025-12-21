@echo off
echo 🚀 Démarrage du serveur Django avec fichiers statiques
echo.

echo 📦 Collecte des fichiers statiques...
python manage.py collectstatic --noinput

echo.
echo 🌐 Démarrage du serveur...
echo Ouvrez votre navigateur sur: http://127.0.0.1:8000
echo.
echo ⚠️ Si les styles ne s'affichent pas:
echo 1. Appuyez sur Ctrl+F5 pour vider le cache
echo 2. Ou fermez ce serveur et exécutez: python manage.py runserver --insecure
echo.

python manage.py runserver
