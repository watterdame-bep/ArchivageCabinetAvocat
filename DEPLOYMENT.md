# Guide de Déploiement Railway - Cabinet Avocat

## Prérequis

1. **Service JSReport déployé sur Railway**
   - Votre service JSReport doit être accessible via une URL Railway
   - Notez l'URL de votre service JSReport (ex: `https://jsreport-service.up.railway.app`)
   - Configurez les templates nécessaires dans JSReport

2. **Base de données PostgreSQL**
   - Railway fournira automatiquement une base de données PostgreSQL
   - L'URL sera disponible via la variable `DATABASE_URL`

## Étapes de Déploiement

### 1. Préparer le Repository Git

```bash
# Initialiser git si pas encore fait
git init

# Ajouter tous les fichiers
git add .

# Commit initial
git commit -m "Initial commit - Cabinet Avocat with JSReport integration"

# Ajouter le remote GitHub
git remote add origin https://github.com/votre-username/cabinet-avocat.git

# Pousser vers GitHub
git push -u origin main
```

### 2. Déployer sur Railway

1. **Connecter le Repository**
   - Aller sur [railway.app](https://railway.app)
   - Créer un nouveau projet
   - Connecter votre repository GitHub

2. **Configurer les Variables d'Environnement**
   
   Dans Railway, ajouter ces variables d'environnement :

   ```
   DEBUG=False
   DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
   SECRET_KEY=votre-clé-secrète-très-longue-et-sécurisée
   
   # JSReport Service (IMPORTANT)
   JSREPORT_SERVICE_URL=https://votre-jsreport-service.up.railway.app
   JSREPORT_USERNAME=admin
   JSREPORT_PASSWORD=votre-mot-de-passe-jsreport
   
   # Templates JSReport
   JSREPORT_TEMPLATE_AGENT=rapport_agent
   JSREPORT_TEMPLATE_CLIENT=rapport_client
   JSREPORT_TEMPLATE_JURIDICTION=rapport_juridiction
   JSREPORT_TEMPLATE_COMMUNE=rapport_commune
   JSREPORT_TEMPLATE_DOSSIER=rapport_dossier
   JSREPORT_TEMPLATE_ACTIVITES=rapport_activites_internes
   JSREPORT_TEMPLATE_FACTURE=facture_paiement
   ```

3. **Ajouter la Base de Données**
   - Dans Railway, ajouter un service PostgreSQL
   - Railway configurera automatiquement `DATABASE_URL`

### 3. Configuration JSReport

Assurez-vous que votre service JSReport Railway contient les templates suivants :

- `rapport_agent` - Pour les rapports d'agents
- `rapport_client` - Pour les rapports de clients  
- `rapport_juridiction` - Pour les rapports de juridictions
- `rapport_commune` - Pour les rapports de communes
- `rapport_dossier` - Pour les rapports de dossiers
- `rapport_activites_internes` - Pour les rapports d'activités internes
- `facture_paiement` - Pour les factures de paiement

### 4. Vérification du Déploiement

1. **Vérifier les logs Railway**
   - Vérifier que l'application démarre sans erreur
   - Vérifier la connexion à la base de données
   - Vérifier la connexion au service JSReport

2. **Tester les fonctionnalités**
   - Connexion utilisateur
   - Génération de rapports
   - Impression via JSReport

## Variables d'Environnement Importantes

| Variable | Description | Exemple |
|----------|-------------|---------|
| `JSREPORT_SERVICE_URL` | URL de votre service JSReport Railway | `https://jsreport.up.railway.app` |
| `JSREPORT_USERNAME` | Nom d'utilisateur JSReport | `admin` |
| `JSREPORT_PASSWORD` | Mot de passe JSReport | `votre-password` |
| `DATABASE_URL` | URL PostgreSQL (auto-configurée) | `postgresql://...` |
| `RAILWAY_PUBLIC_DOMAIN` | Domaine de votre app (auto-configuré) | `app.up.railway.app` |

## Dépannage

### Erreur de connexion JSReport
- Vérifier que `JSREPORT_SERVICE_URL` pointe vers le bon service
- Vérifier les credentials JSReport
- Vérifier que le service JSReport est démarré

### Erreur de base de données
- Vérifier que le service PostgreSQL est ajouté
- Vérifier que `DATABASE_URL` est configurée
- Exécuter les migrations : `python manage.py migrate`

### Erreur de fichiers statiques
- Vérifier que `collectstatic` s'exécute dans le build
- Vérifier la configuration WhiteNoise

## Commandes Utiles

```bash
# Voir les logs Railway
railway logs

# Exécuter des commandes sur Railway
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic

# Redéployer
git push origin main
```