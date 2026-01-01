# 🚨 Guide de Dépannage Railway

## Problème: Health Check Failed

### 🔍 Diagnostic

1. **Vérifier les logs Railway:**
   ```bash
   railway logs --tail
   ```

2. **Tester le health check:**
   ```bash
   railway run python railway_diagnostic.py
   ```

3. **Vérifier les variables d'environnement:**
   ```bash
   railway variables
   ```

### ✅ Solutions par étapes

#### Étape 1: Variables d'environnement
Assurez-vous que ces variables sont définies dans Railway:

```env
SECRET_KEY=E_bTBQ3&GN&rV9n)6+r)j#DxdOr%ceTWOshQiLt!A!BXb^49PX
DEBUG=False
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
```

#### Étape 2: Connexion MySQL
Vérifiez que le service MySQL est connecté au service backend:
- Railway Dashboard → Votre projet → Services
- Cliquez sur votre service Backend
- Onglet "Variables" → Vérifiez la présence de MYSQLHOST, MYSQLPORT, etc.

#### Étape 3: Test de santé
Accédez à: `https://votre-app.railway.app/health/`

Réponse attendue:
```json
{
  "status": "OK",
  "database": "OK",
  "debug": false,
  "environment": {
    "MYSQLHOST": "mysql.railway.internal",
    "MYSQLPORT": "3306",
    "MYSQLDATABASE": "railway",
    "SECRET_KEY": "Set"
  }
}
```

### 🔧 Commandes de debug

```bash
# Diagnostic complet
railway run python railway_diagnostic.py

# Test de connexion MySQL
railway run python test_mysql_connection.py

# Shell Django
railway run python manage.py shell

# Migrations
railway run python manage.py migrate

# Collecte des fichiers statiques
railway run python manage.py collectstatic --noinput

# Vérification Django
railway run python manage.py check --deploy
```

### 🚨 Erreurs communes

#### 1. "DisallowedHost"
```
Invalid HTTP_HOST header: 'xxx.railway.app'
```
**Solution:** Vérifier ALLOWED_HOSTS dans settings_production.py

#### 2. "Can't connect to MySQL server"
```
(2003, "Can't connect to MySQL server")
```
**Solution:** Vérifier la connexion entre services Railway

#### 3. "SECRET_KEY setting must not be empty"
```
ImproperlyConfigured: The SECRET_KEY setting must not be empty
```
**Solution:** Ajouter SECRET_KEY dans les variables Railway

#### 4. "No module named 'MySQLdb'"
```
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module
```
**Solution:** Vérifier que PyMySQL est installé et configuré

### 📊 Monitoring

#### Métriques à surveiller:
- CPU Usage < 80%
- Memory Usage < 512MB
- Response Time < 2s
- Error Rate < 1%

#### Logs importants:
```bash
# Erreurs Django
railway logs | grep ERROR

# Connexions base de données
railway logs | grep MySQL

# Health checks
railway logs | grep health
```

### 🔄 Redéploiement

Si les corrections ne fonctionnent pas:

1. **Redéploiement complet:**
   ```bash
   railway up --detach
   ```

2. **Forcer la reconstruction:**
   - Railway Dashboard → Service → Settings → Redeploy

3. **Vérifier après redéploiement:**
   ```bash
   railway logs --tail
   curl https://votre-app.railway.app/health/
   ```

### 📞 Support

Si le problème persiste:
1. Exécutez `railway run python railway_diagnostic.py`
2. Copiez les logs d'erreur
3. Vérifiez la documentation Railway
4. Contactez le support Railway avec les logs