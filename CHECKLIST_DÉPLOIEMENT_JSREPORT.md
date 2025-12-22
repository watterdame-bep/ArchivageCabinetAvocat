# ✅ CHECKLIST - Déploiement JSReport Repository Séparé

## 📋 ÉTAPES À SUIVRE

### ✅ 1. REPOSITORY JSREPORT (FAIT)
- [x] Nouveau repository GitHub créé
- [x] `Dockerfile` ajouté
- [x] `jsreport.config.json` ajouté
- [x] Repository poussé sur GitHub

### 🔄 2. DÉPLOIEMENT RAILWAY
- [ ] Railway Dashboard → New Project → Empty Project
- [ ] Nom : `cabinet-avocat-jsreport`
- [ ] New Service → GitHub Repo
- [ ] Sélectionner votre repository JSReport
- [ ] Attendre le déploiement (2-3 minutes)
- [ ] Vérifier status : `Active`

### 🔄 3. URL PUBLIQUE
- [ ] Settings → Networking → Generate Domain
- [ ] Copier l'URL générée
- [ ] Tester : `https://votre-url/api/ping` → doit retourner "OK"
- [ ] Tester interface : `https://votre-url` → page de login JSReport

### 🔄 4. CONFIGURATION DJANGO
Dans votre service Django Railway, modifier les variables :
- [ ] `JSREPORT_URL` = `https://votre-jsreport-url.railway.app`
- [ ] `JSREPORT_USERNAME` = `admin`
- [ ] `JSREPORT_PASSWORD` = `admin123`
- [ ] `JSREPORT_TIMEOUT` = `120`
- [ ] Attendre redéploiement Django

### 🔄 5. IMPORT DES TEMPLATES
- [ ] JSReport local (`localhost:5488`) → Exporter tous les templates
- [ ] JSReport Railway → Login avec `admin`/`admin123`
- [ ] Importer chaque template :
  - [ ] `Facture_paiement_client`
  - [ ] `Facture_dossier`
  - [ ] `Extrait_de_compte_client`

### 🔄 6. TESTS FINAUX
- [ ] Test configuration : `python test_jsreport_quick.py`
- [ ] Test connexion : `python diagnostic_jsreport_railway.py`
- [ ] Test impression réelle :
  - [ ] Aller sur Django Railway
  - [ ] Créer un paiement
  - [ ] Cliquer "Imprimer facture"
  - [ ] PDF se télécharge ✅

## 🚨 POINTS D'ATTENTION

### ⚠️ Nom du fichier Dockerfile
- ✅ Dans le repository séparé : `Dockerfile` (pas `Dockerfile.jsreport`)
- ✅ Railway détecte automatiquement le Dockerfile à la racine

### ⚠️ Configuration JSON
- ✅ Fichier `jsreport.config.json` à la racine du repository
- ✅ Configuration avec `"provider": "fs"` pour éviter l'erreur store

### ⚠️ Credentials identiques
- ✅ Même username/password dans JSReport et Django
- ✅ Par défaut : `admin` / `admin123`

## 🎯 RÉSULTAT ATTENDU

Après toutes ces étapes :
```
✅ JSReport accessible : https://votre-url.railway.app
✅ Interface de login fonctionnelle
✅ Templates importés et visibles
✅ Django connecté à JSReport Railway
✅ Impression des factures opérationnelle ! 🎉
```

## 🔧 DÉPANNAGE RAPIDE

### Si JSReport ne démarre pas
1. Vérifiez les logs Railway
2. Cherchez "server started on port 5488"
3. Pas d'erreur "rootOptions.store should be object"

### Si Django ne se connecte pas
1. Vérifiez l'URL JSReport dans les variables Django
2. Testez manuellement : `https://votre-url/api/ping`
3. Vérifiez les credentials

### Si l'impression ne fonctionne pas
1. Vérifiez que tous les templates sont importés
2. Testez avec `diagnostic_jsreport_railway.py`
3. Consultez les logs Django pour les erreurs

---

## 📞 SUPPORT

Si vous rencontrez un problème à une étape :
1. **Notez** à quelle étape vous êtes bloqué
2. **Copiez** les messages d'erreur des logs Railway
3. **Testez** les URLs manuellement dans le navigateur

**Vous êtes sur la bonne voie ! Cette approche va fonctionner parfaitement ! 🚀**