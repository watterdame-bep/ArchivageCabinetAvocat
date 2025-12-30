# Cabinet Avocat - Déploiement Railway avec JSReport

## 🚀 Déploiement Rapide

### 1. Préparer le Code

```bash
# Cloner ou naviguer vers le projet
cd CabinetAvocat

# Exécuter le script de déploiement (Linux/Mac)
./deploy.sh

# Ou manuellement (Windows/Linux/Mac)
git add .
git commit -m "Deploy to Railway"
git push origin main
```

### 2. Configuration Railway

#### A. Créer le Projet Principal
1. Aller sur [railway.app](https://railway.app)
2. Créer un nouveau projet depuis GitHub
3. Sélectionner votre repository

#### B. Ajouter les Services
1. **PostgreSQL Database**
   - Ajouter un service PostgreSQL
   - Railway configurera automatiquement `DATABASE_URL`

2. **Votre Service JSReport** (déjà déployé)
   - Notez l'URL de votre service JSReport
   - Format: `https://votre-jsreport.up.railway.app`

#### C. Variables d'Environnement

Dans Railway, configurer ces variables :

```env
# Django Configuration
DEBUG=False
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=votre-clé-secrète-très-longue-et-sécurisée-ici

# JSReport Service Connection
JSREPORT_SERVICE_URL=https://votre-jsreport-service.up.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=votre-mot-de-passe-jsreport
JSREPORT_TIMEOUT=60000
JSREPORT_VERIFY_SSL=True

# JSReport Templates
JSREPORT_TEMPLATE_AGENT=rapport_agent
JSREPORT_TEMPLATE_CLIENT=rapport_client
JSREPORT_TEMPLATE_JURIDICTION=rapport_juridiction
JSREPORT_TEMPLATE_COMMUNE=rapport_commune
JSREPORT_TEMPLATE_DOSSIER=rapport_dossier
JSREPORT_TEMPLATE_ACTIVITES=rapport_activites_internes
JSREPORT_TEMPLATE_FACTURE=facture_paiement
```

### 3. Vérification du Déploiement

#### A. Vérifier les Logs
```bash
# Dans Railway, onglet "Deployments" > "View Logs"
# Vérifier :
# ✅ Migration de la base de données
# ✅ Collection des fichiers statiques  
# ✅ Démarrage de Gunicorn
# ✅ Connexion JSReport
```

#### B. Tester l'Application
1. **Accès à l'application**
   - Ouvrir l'URL Railway de votre app
   - Vérifier la page de connexion

2. **Tester JSReport**
   - Se connecter à l'application
   - Aller dans les rapports
   - Tester l'impression d'un rapport
   - Vérifier que le PDF se génère correctement

## 🔧 Configuration JSReport

### Templates Requis dans votre Service JSReport

Assurez-vous que votre service JSReport Railway contient ces templates :

| Template | Usage |
|----------|-------|
| `rapport_agent` | Rapports des agents |
| `rapport_client` | Rapports des clients |
| `rapport_juridiction` | Rapports des juridictions |
| `rapport_commune` | Rapports des communes |
| `rapport_dossier` | Rapports des dossiers |
| `rapport_activites_internes` | Rapports d'activités internes |
| `facture_paiement` | Factures de paiement |

### Structure des Données Envoyées

Chaque template recevra des données au format JSON avec cette structure :

```json
{
  "cabinet": { /* Informations du cabinet */ },
  "user": { /* Informations utilisateur */ },
  "agents": [ /* Liste des agents (pour rapport_agent) */ ],
  "clients": [ /* Liste des clients (pour rapport_client) */ ],
  "filtres": { /* Filtres appliqués */ },
  "date_generation": "2024-01-01T12:00:00Z"
}
```

## 🚨 Dépannage

### Erreur de Connexion JSReport

**Symptôme :** "Service JSReport indisponible"

**Solutions :**
1. Vérifier que `JSREPORT_SERVICE_URL` est correcte
2. Vérifier que le service JSReport Railway est démarré
3. Vérifier les credentials (`JSREPORT_USERNAME`, `JSREPORT_PASSWORD`)
4. Tester la connexion manuellement

### Erreur de Template JSReport

**Symptôme :** "Template not found"

**Solutions :**
1. Vérifier que les templates existent dans JSReport
2. Vérifier les noms des templates dans les variables d'environnement
3. Vérifier les permissions des templates

### Erreur de Base de Données

**Symptôme :** "Database connection failed"

**Solutions :**
1. Vérifier que le service PostgreSQL est ajouté
2. Vérifier que `DATABASE_URL` est configurée automatiquement
3. Exécuter les migrations : `railway run python manage.py migrate`

### Erreur de Fichiers Statiques

**Symptôme :** CSS/JS ne se chargent pas

**Solutions :**
1. Vérifier que `collectstatic` s'exécute dans les logs de build
2. Vérifier la configuration WhiteNoise
3. Redéployer l'application

## 📞 Support

Pour toute question sur le déploiement :

1. Vérifier les logs Railway
2. Consulter la documentation Railway
3. Tester la connexion JSReport séparément
4. Vérifier les variables d'environnement

## 🔄 Mise à Jour

Pour mettre à jour l'application :

```bash
# Faire les modifications
git add .
git commit -m "Description des changements"
git push origin main

# Railway redéploiera automatiquement
```