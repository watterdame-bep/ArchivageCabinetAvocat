# 📋 Guide Étape par Étape - Migration Templates JSReport

## 🎯 Ce que VOUS devez faire (je ne peux pas le faire à votre place)

### ✅ **Étape 1: Vérifier vos Templates Locaux**

```bash
# Exécuter le script de vérification
python check_templates.py

# Choisir option 1: Vérifier JSReport local
# Résultat attendu: Liste de vos 4 templates
```

**Si JSReport local n'est pas accessible :**
```bash
# Démarrer JSReport local
docker run -p 5488:5488 jsreport/jsreport:4.7.0

# Puis accéder à: http://localhost:5488/studio
```

### ✅ **Étape 2: Exporter vos Templates**

#### **Option A: Export Manuel (RECOMMANDÉ)**
1. **Ouvrir JSReport Studio local** : `http://localhost:5488/studio`
2. **Cliquer sur ⚙️ (Settings)** en haut à droite
3. **Sélectionner "Export"**
4. **Cocher toutes les options** :
   - ✅ Include templates
   - ✅ Include assets  
   - ✅ Include data
5. **Cliquer "Export"**
6. **Télécharger le fichier .zip**
7. **Sauvegarder le fichier** (ex: `jsreport-export-backup.zip`)

#### **Option B: Script Automatisé**
```bash
# Utiliser le script de migration
python migrate_templates.py

# Suivre les instructions du script
```

### ✅ **Étape 3: Déployer JSReport sur Railway**

```bash
# Exécuter le script de déploiement
chmod +x deploy-jsreport.sh
./deploy-jsreport.sh
```

**Suivre les instructions du script :**
1. Créer un nouveau projet Railway
2. Nommer le projet "cabinet-avocat-jsreport"
3. Utiliser le Dockerfile.jsreport
4. Configurer les variables d'environnement :
   ```
   JSREPORT_USERNAME=admin
   JSREPORT_PASSWORD=VotreMotDePasseSecurise123
   JSREPORT_COOKIE_SECRET=VotreCleSecrete456
   NODE_ENV=production
   ```
5. Noter l'URL générée (ex: `https://cabinet-avocat-jsreport-production.up.railway.app`)

### ✅ **Étape 4: Importer les Templates en Production**

1. **Accéder à JSReport Production** : `https://votre-jsreport-url.railway.app/studio`
2. **Se connecter** :
   - Username: `admin`
   - Password: `VotreMotDePasseSecurise123`
3. **Cliquer sur ⚙️ (Settings)**
4. **Sélectionner "Import"**
5. **Choisir le fichier .zip exporté à l'étape 2**
6. **Cliquer "Import"**
7. **Vérifier que tous les templates apparaissent**

### ✅ **Étape 5: Configurer Django pour la Production**

Dans Railway, configurer les variables d'environnement Django :
```
JSREPORT_URL=https://votre-jsreport-url.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=VotreMotDePasseSecurise123
JSREPORT_TIMEOUT=120
```

### ✅ **Étape 6: Tester la Configuration**

```bash
# Tester la connexion Django → JSReport
python manage.py test_jsreport --verbose

# Résultat attendu :
✅ Connexion JSReport réussie!
✅ Trouvé 4 template(s):
   ✅ Facture_paiement_client
   ✅ Extrait_de_compte_client  
   ✅ Facture_dossier
   ✅ Rapport
```

```bash
# Tester la génération PDF
python manage.py test_jsreport --test-pdf

# Résultat attendu :
✅ PDF généré avec succès! Taille: XXXX bytes
```

### ✅ **Étape 7: Déployer Django sur Railway**

1. **Pousser le code sur GitHub**
2. **Créer un projet Railway pour Django**
3. **Connecter le repository GitHub**
4. **Configurer les variables d'environnement** (voir étape 5)
5. **Railway déploiera automatiquement**

### ✅ **Étape 8: Test Final End-to-End**

1. **Accéder à votre application Django en production**
2. **Tester chaque fonction qui génère un PDF** :
   - Facture de paiement
   - Extrait de compte client
   - Facture de dossier
   - Rapport client
3. **Vérifier que les PDF se génèrent correctement**

## 🆘 **Si vous avez des Problèmes**

### ❌ **Problème: Templates non trouvés**
```bash
# Vérifier les templates en production
python check_templates.py
# Option 2: Comparer local et production
```

### ❌ **Problème: Erreur d'authentification**
```bash
# Tester la connexion manuellement
curl -u admin:password https://votre-jsreport.railway.app/api/ping
```

### ❌ **Problème: PDF non généré**
1. Vérifier les logs Railway JSReport
2. Tester le template individuellement dans JSReport Studio
3. Vérifier les données envoyées par Django

## 📞 **Support**

Si vous rencontrez des difficultés :

1. **Exécutez les scripts de diagnostic** :
   ```bash
   python check_templates.py
   python verify_jsreport_migration.py
   ```

2. **Vérifiez les logs Railway** :
   - Logs du service Django
   - Logs du service JSReport

3. **Testez étape par étape** :
   - Connexion JSReport local ✅
   - Export templates ✅  
   - JSReport production accessible ✅
   - Import templates ✅
   - Connexion Django → JSReport ✅
   - Génération PDF ✅

## 🎯 **Résumé des Actions VOUS**

| Étape | Action | Outil | Durée |
|-------|--------|-------|-------|
| 1 | Vérifier templates locaux | `check_templates.py` | 2 min |
| 2 | Exporter templates | JSReport Studio | 5 min |
| 3 | Déployer JSReport Railway | `deploy-jsreport.sh` | 10 min |
| 4 | Importer templates | JSReport Studio | 5 min |
| 5 | Configurer Django | Railway Dashboard | 3 min |
| 6 | Tester configuration | `test_jsreport.py` | 2 min |
| 7 | Déployer Django | Railway | 5 min |
| 8 | Test final | Application web | 5 min |

**Total estimé : 37 minutes** ⏱️

**Une fois terminé, votre application sera 100% opérationnelle en production ! 🚀**