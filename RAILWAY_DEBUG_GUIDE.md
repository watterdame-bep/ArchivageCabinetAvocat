# 🔧 Guide Debug Railway - Connection Refused

## 🚨 Problème: Site Déployé mais Inaccessible

**Symptômes:**
- ✅ Build Railway réussi
- ❌ Application inaccessible
- ❌ Erreur "Connection refused" dans les logs
- ❌ Timeout ou 500 Internal Server Error

---

## 🔍 **Étape 1: Vérifier les Logs Railway**

```bash
# Dans Railway Dashboard → Service Django → Deployments → View Logs
# Ou via CLI:
railway logs --follow
```

**Chercher ces erreurs:**
```
❌ Can't connect to MySQL server
❌ Connection refused
❌ MYSQL_HOST manquante
❌ Access denied for user
❌ Unknown database
```

---

## 🔍 **Étape 2: Vérifier le Service MySQL**

### Dans Railway Dashboard:
1. **Vérifier qu'un service "MySQL" existe**
   - Si absent: `Add Service → Database → MySQL`
   
2. **Vérifier que MySQL est "Running"**
   - Status doit être vert avec "Running"
   - Si "Crashed" ou "Deploying": attendre ou redémarrer

3. **Vérifier les Variables Auto-générées**
   ```
   Service MySQL → Variables:
   ✅ MYSQL_HOST=containers-us-west-xxx.railway.app
   ✅ MYSQL_PORT=3306
   ✅ MYSQL_DATABASE=railway
   ✅ MYSQL_USER=root
   ✅ MYSQL_PASSWORD=xxx-auto-generated
   ✅ MYSQL_URL=mysql://root:xxx@containers...
   ```

---

## 🔍 **Étape 3: Vérifier la Connexion des Services**

### Service Django doit voir les variables MySQL:
```bash
# Railway Dashboard → Service Django → Variables
# Vérifier que ces variables sont visibles:
MYSQL_HOST (référencée depuis MySQL service)
MYSQL_DATABASE (référencée depuis MySQL service)
MYSQL_USER (référencée depuis MySQL service)
MYSQL_PASSWORD (référencée depuis MySQL service)
MYSQL_PORT (référencée depuis MySQL service)
```

**Si les variables ne sont pas visibles:**
1. Railway Dashboard → Service Django → Settings
2. Service Variables → Connect Variable
3. Sélectionner le service MySQL
4. Connecter toutes les variables MYSQL_*

---

## 🔍 **Étape 4: Tester la Configuration**

### Test 1: Script de Diagnostic
```bash
# Localement avec les variables Railway:
export MYSQL_HOST="containers-us-west-xxx.railway.app"
export MYSQL_DATABASE="railway"
export MYSQL_USER="root"
export MYSQL_PASSWORD="xxx-from-railway"
export MYSQL_PORT="3306"

python diagnose_railway.py
```

### Test 2: Connexion Directe
```python
# Test de connexion PyMySQL direct
import pymysql
import os

pymysql.install_as_MySQLdb()
conn = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
    port=int(os.environ['MYSQL_PORT'])
)
print("✅ Connexion MySQL directe réussie!")
conn.close()
```

---

## 🔧 **Solutions par Type d'Erreur**

### ❌ **"MYSQL_HOST manquante"**
```bash
# Cause: Service MySQL pas créé ou variables pas connectées
# Solution:
1. Railway Dashboard → Add Service → Database → MySQL
2. Attendre 2-3 minutes que Railway génère les variables
3. Service Django → Settings → Service Variables → Connect MySQL variables
4. Redéployer Django
```

### ❌ **"Connection refused"**
```bash
# Cause: Django démarre avant MySQL ou mauvaise configuration
# Solution:
1. Vérifier que MySQL service est "Running"
2. Utiliser le nouveau start.sh avec wait_for_mysql.py
3. Redéployer avec: railway redeploy
```

### ❌ **"Access denied"**
```bash
# Cause: MYSQL_PASSWORD incorrecte ou corrompue
# Solution:
1. Railway Dashboard → Service MySQL → Variables
2. Copier la vraie valeur de MYSQL_PASSWORD
3. Service Django → Variables → Vérifier MYSQL_PASSWORD
4. Si différente, reconnecter la variable
```

### ❌ **"Unknown database"**
```bash
# Cause: MYSQL_DATABASE incorrecte
# Solution:
1. Vérifier que MYSQL_DATABASE="railway" (valeur par défaut Railway)
2. Ou utiliser la valeur exacte du service MySQL
```

---

## 🚀 **Procédure de Fix Complète**

### Étape 1: Reset Complet
```bash
# 1. Supprimer le service MySQL actuel (si problématique)
# 2. Créer un nouveau service MySQL
# 3. Attendre 3 minutes que Railway génère tout
```

### Étape 2: Reconnecter les Variables
```bash
# Railway Dashboard → Service Django → Settings → Service Variables
# Supprimer toutes les connexions MySQL existantes
# Reconnecter une par une:
# - MYSQL_HOST → MySQL Service
# - MYSQL_DATABASE → MySQL Service  
# - MYSQL_USER → MySQL Service
# - MYSQL_PASSWORD → MySQL Service
# - MYSQL_PORT → MySQL Service
```

### Étape 3: Forcer le Redéploiement
```bash
# Railway Dashboard → Service Django → Deployments → Redeploy
# Ou via CLI:
railway redeploy
```

### Étape 4: Surveiller les Logs
```bash
# Logs attendus avec le nouveau start.sh:
🚀 Démarrage de l'application Cabinet Avocat...
⏳ Vérification de MySQL Railway...
🔗 Tentative de connexion: root@containers-us-west-xxx.railway.app:3306/railway
✅ MySQL Railway prêt!
📊 Exécution des migrations...
✅ Migrations appliquées
📁 Collection des fichiers statiques...
✅ Fichiers statiques collectés
✅ Application prête à démarrer!
```

---

## 🎯 **Checklist de Validation**

### Avant Redéploiement:
- [ ] Service MySQL existe et est "Running"
- [ ] Variables MYSQL_* auto-générées dans MySQL service
- [ ] Variables MYSQL_* connectées au service Django
- [ ] start.sh et wait_for_mysql.py présents
- [ ] Procfile utilise start.sh

### Après Redéploiement:
- [ ] Logs montrent "✅ MySQL Railway prêt!"
- [ ] Migrations s'exécutent sans erreur
- [ ] Application démarre sans "Connection refused"
- [ ] Site accessible sur l'URL Railway

---

## 🆘 **Si Ça Ne Marche Toujours Pas**

### Debug Avancé:
```bash
# 1. Vérifier la région Railway
# MySQL et Django doivent être dans la même région

# 2. Vérifier les quotas Railway
# Compte gratuit: limites de ressources

# 3. Tester avec une DB externe
# Utiliser une DB MySQL externe temporairement

# 4. Contacter le support Railway
# Si problème de réseau/infrastructure
```

### Configuration Alternative:
```python
# settings_production.py - Configuration de secours
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',  # Temporaire pour test
    }
} if not os.environ.get('MYSQL_HOST') else {
    # Configuration MySQL normale
}
```

---

## ✅ **Résultat Final Attendu**

Avec toutes ces corrections:
- ✅ **Pas de fallback localhost** (erreur immédiate si MySQL manque)
- ✅ **Attente automatique** de MySQL avant démarrage Django
- ✅ **Validation stricte** des variables d'environnement
- ✅ **Logs détaillés** pour debug facile
- ✅ **Retry automatique** si MySQL temporairement indisponible

**Ton site sera accessible dès que MySQL sera prêt! 🚀**