# 🚂 GUIDE DÉTAILLÉ - Déployer JSReport sur Railway

## 🎯 OBJECTIF
Créer un service JSReport séparé sur Railway pour que l'impression des factures fonctionne en ligne.

---

## 📋 ÉTAPE 1: PRÉPARER LES FICHIERS (Déjà fait ✅)

Vous avez déjà le fichier `Dockerfile.jsreport` qui contient:
```dockerfile
FROM jsreport/jsreport:4.7.0
ENV NODE_ENV=production
ENV httpPort=${PORT:-5488}
# ... configuration complète
```

---

## 🌐 ÉTAPE 2: CRÉER LE PROJET RAILWAY

### 2.1 Aller sur Railway
1. **Ouvrez votre navigateur**
2. **Allez sur**: https://railway.app
3. **Connectez-vous** avec votre compte (GitHub recommandé)

### 2.2 Créer un nouveau projet
1. **Cliquez sur**: `New Project`
2. **Sélectionnez**: `Empty Project`
3. **Nom du projet**: `cabinet-avocat-jsreport`
4. **Cliquez**: `Create`

![Railway New Project](https://railway.app/new)

---

## 🔧 ÉTAPE 3: AJOUTER LE SERVICE JSREPORT

### 3.1 Ajouter un service
1. **Dans votre projet Railway**, cliquez: `New Service`
2. **Sélectionnez**: `GitHub Repo`
3. **Choisissez**: Votre repository `CabinetAvocat`
4. **Cliquez**: `Deploy`

### 3.2 Configurer le service
1. **Allez dans**: `Settings` du service
2. **Section Build**: 
   - **Root Directory**: `/` (laisser vide)
   - **Dockerfile Path**: `Dockerfile.jsreport`
3. **Cliquez**: `Save`

---

## ⚙️ ÉTAPE 4: CONFIGURER LES VARIABLES D'ENVIRONNEMENT

### 4.1 Aller dans Variables
1. **Dans votre service JSReport**, cliquez: `Variables`
2. **Ajoutez ces variables une par une**:

```env
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=VotreMotDePasseSecurise123
JSREPORT_COOKIE_SECRET=VotreCleSecrete456
NODE_ENV=production
```

### 4.2 Comment ajouter chaque variable
1. **Cliquez**: `New Variable`
2. **Name**: `JSREPORT_USERNAME`
3. **Value**: `admin`
4. **Cliquez**: `Add`
5. **Répétez** pour chaque variable

---

## 🚀 ÉTAPE 5: DÉPLOYER ET RÉCUPÉRER L'URL

### 5.1 Déploiement automatique
1. **Railway déploie automatiquement** après configuration
2. **Attendez** que le statut passe à `Active` (2-3 minutes)
3. **Vérifiez les logs** en cliquant sur `Deployments`

### 5.2 Récupérer l'URL publique
1. **Dans votre service**, cliquez: `Settings`
2. **Section Networking**: 
   - **Cliquez**: `Generate Domain`
   - **Railway génère**: `https://cabinet-avocat-jsreport-production.up.railway.app`
3. **Copiez cette URL** (vous en aurez besoin)

### 5.3 Tester JSReport
1. **Ouvrez l'URL** dans votre navigateur
2. **Ajoutez** `/api/ping` à la fin
3. **Exemple**: `https://votre-url.railway.app/api/ping`
4. **Résultat attendu**: Page avec "OK"

---

## 🔗 ÉTAPE 6: CONFIGURER VOTRE SERVICE DJANGO

### 6.1 Aller dans votre service Django Railway
1. **Retournez** au dashboard Railway
2. **Sélectionnez** votre projet Django principal
3. **Cliquez** sur le service Django

### 6.2 Modifier les variables d'environnement Django
1. **Cliquez**: `Variables`
2. **Modifiez ou ajoutez**:

```env
JSREPORT_URL=https://votre-jsreport-url.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=VotreMotDePasseSecurise123
JSREPORT_TIMEOUT=120
```

**⚠️ IMPORTANT**: Remplacez `votre-jsreport-url.railway.app` par l'URL réelle générée à l'étape 5.2

### 6.3 Redéployer Django
1. **Railway redéploie automatiquement** après changement des variables
2. **Ou cliquez**: `Redeploy` manuellement
3. **Attendez** que le déploiement soit terminé

---

## 📁 ÉTAPE 7: IMPORTER VOS TEMPLATES

### 7.1 Accéder à JSReport en ligne
1. **Ouvrez**: `https://votre-jsreport-url.railway.app`
2. **Login**: `admin`
3. **Password**: `VotreMotDePasseSecurise123`

### 7.2 Exporter depuis JSReport local
1. **Ouvrez JSReport local**: `http://localhost:5488`
2. **Login**: `admin` / `admin123`
3. **Pour chaque template**:
   - Cliquez sur le template
   - `Actions` > `Export`
   - Sauvegardez le fichier `.json`

### 7.3 Importer dans JSReport Railway
1. **Dans JSReport Railway**, cliquez: `New` > `Template`
2. **Cliquez**: `Import`
3. **Sélectionnez** le fichier `.json` exporté
4. **Répétez** pour tous les templates

### 7.4 Templates requis
Assurez-vous d'avoir ces templates:
- ✅ `Facture_paiement_client`
- ✅ `Facture_dossier`
- ✅ `Extrait_de_compte_client`

---

## 🧪 ÉTAPE 8: TESTER LA CONFIGURATION

### 8.1 Test rapide
```bash
cd CabinetAvocat
python test_jsreport_quick.py
```
**Résultat attendu**: ✅ URL semble correcte pour la production

### 8.2 Test complet
```bash
python diagnostic_jsreport_railway.py
```
**Résultat attendu**: ✅ Connexion OK, ✅ Templates trouvés

### 8.3 Test réel d'impression
1. **Allez** sur votre application Railway
2. **Créez** un nouveau paiement
3. **Cliquez**: "Imprimer facture"
4. **Résultat**: Le PDF se télécharge ! 🎉

---

## 📊 RÉCAPITULATIF VISUEL

```
┌─────────────────┐    ┌─────────────────┐
│   Service       │    │   Service       │
│   Django        │───▶│   JSReport      │
│   (Principal)   │    │   (Nouveau)     │
└─────────────────┘    └─────────────────┘
         │                       │
         │                       │
    Variables:              Variables:
    JSREPORT_URL=...       JSREPORT_USERNAME=admin
    JSREPORT_USERNAME=...  JSREPORT_PASSWORD=...
    JSREPORT_PASSWORD=...  NODE_ENV=production
```

---

## 🔧 DÉPANNAGE COURANT

### Problème: "Service non accessible"
**Solution**:
1. Vérifiez que le service JSReport est `Active`
2. Vérifiez l'URL générée
3. Testez `/api/ping`

### Problème: "Erreur d'authentification"
**Solution**:
1. Vérifiez que les credentials sont identiques dans les 2 services
2. Pas d'espaces dans les variables
3. Respectez la casse

### Problème: "Template non trouvé"
**Solution**:
1. Connectez-vous à JSReport Railway
2. Vérifiez que tous les templates sont importés
3. Vérifiez les noms exacts (sensible à la casse)

---

## ✅ CHECKLIST FINALE

- [ ] Projet Railway créé
- [ ] Service JSReport ajouté avec Dockerfile.jsreport
- [ ] Variables d'environnement JSReport configurées
- [ ] URL publique générée et testée
- [ ] Variables Django mises à jour avec la nouvelle URL
- [ ] Service Django redéployé
- [ ] Templates exportés du local
- [ ] Templates importés dans Railway
- [ ] Test de connexion réussi
- [ ] Test d'impression réussi

**🎉 Après ces étapes, JSReport fonctionnera parfaitement en ligne !**

---

## 💡 CONSEILS PRATIQUES

1. **Gardez les mêmes credentials** dans les 2 services
2. **Notez l'URL JSReport** quelque part
3. **Testez toujours** `/api/ping` après déploiement
4. **Vérifiez les logs** en cas de problème
5. **Les templates sont critiques** - vérifiez qu'ils sont tous importés

**Temps total estimé**: 15-20 minutes
**Difficulté**: Facile (interface graphique Railway)