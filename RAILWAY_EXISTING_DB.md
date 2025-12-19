# 🔄 Utilisation de la base de données existante sur Railway

## 📋 Configuration actuelle

L'application est configurée pour utiliser une base de données MySQL existante sur Railway qui contient déjà :
- ✅ Toutes les tables nécessaires
- ✅ Les utilisateurs existants
- ✅ Les données de l'application

## 🚀 Processus de démarrage

Le script `start.sh` effectue les étapes suivantes :

1. **Vérification MySQL** - Connexion au service MySQL Railway
2. **Vérification BDD** - Contrôle que les données existantes sont accessibles
3. **Migrations** - Application uniquement des nouvelles migrations (pas de recréation)
4. **Fichiers statiques** - Collection des assets
5. **Démarrage** - Lancement du serveur Gunicorn

## 🔍 Vérifications automatiques

Au démarrage, l'application vérifie :
- La connexion à la base de données
- Le nombre d'utilisateurs existants
- Le nombre d'administrateurs disponibles

## 📝 Variables d'environnement requises

Assurez-vous que ces variables sont configurées dans Railway :

```bash
MYSQLHOST=<host_mysql_railway>
MYSQLDATABASE=<nom_base_donnees>
MYSQLUSER=<utilisateur_mysql>
MYSQLPASSWORD=<mot_de_passe_mysql>
MYSQLPORT=3306
```

## ⚠️ Important

- **Pas de création de superutilisateur** - Utilise les comptes existants
- **Pas de --run-syncdb** - Préserve les données existantes
- **Migrations seulement** - Applique uniquement les nouveaux changements

## 🔗 Accès à l'application

Une fois déployée, l'application sera accessible via :
- **URL principale:** `https://votre-app.railway.app/`
- **Administration:** `https://votre-app.railway.app/admin/`

Utilisez vos identifiants existants pour vous connecter.