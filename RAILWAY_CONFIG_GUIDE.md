# 🚨 Guide de Configuration Railway - Résolution du problème "localhost"

## 🔍 Problème identifié

Django essaie de se connecter à `localhost` au lieu du serveur MySQL Railway. Cela indique que les variables d'environnement MySQL ne sont pas correctement injectées.

## ✅ Solution étape par étape

### 1. **Vérifier la connexion MySQL ↔ Django dans Railway**

Dans Railway Dashboard :

1. **Allez dans votre projet Railway**
2. **Cliquez sur votre service Django**
3. **Onglet "Variables"**
4. **Vérifiez que ces variables existent :**
   - `MYSQLHOST`
   - `MYSQLUSER`
   - `MYSQLPASSWORD`
   - `MYSQLDATABASE`
   - `MYSQLPORT`

### 2. **Si les variables sont manquantes :**

1. **Cliquez sur "Add Variable Reference"**
2. **Sélectionnez votre service MySQL**
3. **Railway va automatiquement ajouter toutes les variables MySQL**
4. **Redéployez le service Django**

### 3. **Forcer l'utilisation de settings_production**

Dans l'onglet "Variables" de votre service Django, ajoutez :
```
DJANGO_SETTINGS_MODULE = CabinetAvocat.settings_production
```

### 4. **Variables recommandées à ajouter**

```bash
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
DEBUG=False
DJANGO_LOG_LEVEL=INFO
```

## 🔧 Scripts de diagnostic inclus

Le déploiement inclut maintenant des scripts de diagnostic :

1. **`debug_railway_env.py`** - Diagnostic complet des variables
2. **`force_production_settings.py`** - Force la bonne configuration
3. **`test_mysql_connection.py`** - Test direct de MySQL

## 📋 Checklist de vérification

- [ ] Service MySQL créé dans Railway
- [ ] Service Django créé dans Railway
- [ ] Variables MySQL connectées au service Django
- [ ] `DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production` défini
- [ ] Redéploiement effectué après changement de variables

## 🚀 Après correction

Une fois les variables correctement configurées, vous devriez voir dans les logs :

```
🔗 Connexion MySQL Railway: user@host:3306/database
🔍 Debug - MYSQLHOST: [votre_host_railway]
✅ MySQL Railway prêt!
✅ Base de données connectée!
```

## 🆘 Si le problème persiste

1. **Vérifiez les logs Railway** pour voir les messages de diagnostic
2. **Contactez le support Railway** si les variables ne s'injectent pas
3. **Vérifiez que le service MySQL est bien démarré**

## 📞 Commandes de debug utiles

Dans Railway Console (si disponible) :
```bash
echo $MYSQLHOST
echo $DJANGO_SETTINGS_MODULE
python debug_railway_env.py
```