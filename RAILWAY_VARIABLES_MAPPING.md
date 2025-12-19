# 🔗 Correspondance Variables Railway

## 🎯 **Problème Résolu**

**Problème:** Variables Railway ne correspondaient pas aux noms utilisés dans `settings_production.py`

**Solution:** Correction des noms de variables pour correspondre exactement à Railway

---

## ✅ **Variables Railway Exactes**

### **Variables MySQL Railway:**
```bash
MYSQL_HOST=containers-us-west-xxx.railway.app
MYSQL_DATABASE=railway
MYSQL_PASSWORD=xxx-auto-generated-xxx
MYSQL_PORT=3306
MYSQLUSER=root  # ⚠️ ATTENTION: MYSQLUSER (pas MYSQL_USER)
```

### **Autres Variables Railway:**
```bash
ALLOWED_HOSTS=.railway.app,.up.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app
DEBUG=False
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=xxx-secret-key-xxx

# JSReport
JSREPORT_URL=https://votre-jsreport.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=xxx
JSREPORT_TIMEOUT=120
```

---

## 🔧 **Corrections Appliquées**

### **settings_production.py:**
```python
# ❌ AVANT (noms incorrects)
MYSQLHOST = os.environ.get('MYSQL_HOST')
MYSQLUSER = os.environ.get('MYSQLUSER')

# ✅ APRÈS (noms corrects)
MYSQL_HOST_VAR = os.environ.get('MYSQL_HOST')
MYSQL_USER_VAR = os.environ.get('MYSQLUSER')  # Railway utilise MYSQLUSER
```

### **start.sh:**
```bash
# ❌ AVANT
if [ -z "$MYSQLHOST" ]; then

# ✅ APRÈS  
if [ -z "$MYSQL_HOST" ]; then
```

### **wait_for_mysql.py:**
```python
# ❌ AVANT
required_vars = ['MYSQLHOST', 'MYSQLUSER', ...]

# ✅ APRÈS
required_vars = ['MYSQL_HOST', 'MYSQLUSER', ...]
```

---

## 🧪 **Test de Validation**

### **Script de Test Variables:**
```python
import os

# Variables Railway attendues
railway_vars = {
    'MYSQL_HOST': os.environ.get('MYSQL_HOST'),
    'MYSQL_DATABASE': os.environ.get('MYSQL_DATABASE'),
    'MYSQLUSER': os.environ.get('MYSQLUSER'),  # Attention: MYSQLUSER
    'MYSQL_PASSWORD': os.environ.get('MYSQL_PASSWORD'),
    'MYSQL_PORT': os.environ.get('MYSQL_PORT'),
}

print("🔍 Variables Railway:")
for var, value in railway_vars.items():
    if value:
        if 'PASSWORD' in var:
            print(f"✅ {var}: [MASQUÉ - {len(value)} caractères]")
        else:
            print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: MANQUANTE")
```

---

## 🚀 **Redéploiement**

### **Étapes:**
```bash
git add .
git commit -m "Fix: Correct Railway variable names mapping"
git push origin main
```

### **Logs Attendus:**
```
🔗 Connexion à la base de données Railway: root@containers-us-west-xxx.railway.app:3306/railway
✅ MySQL Railway connecté!
🔹 Step 1: Création des migrations Django...
🔹 Step 2: Application des migrations avec --run-syncdb...
✅ Superutilisateur créé: admin / Admin123!
[INFO] Starting gunicorn 23.0.0
```

---

## 📋 **Checklist Variables Railway**

### **Variables MySQL (Auto-générées):**
- [ ] `MYSQL_HOST` (généré par Railway)
- [ ] `MYSQL_DATABASE` (généré par Railway)
- [ ] `MYSQLUSER` (généré par Railway - attention au nom!)
- [ ] `MYSQL_PASSWORD` (généré par Railway)
- [ ] `MYSQL_PORT` (généré par Railway)

### **Variables Django (À configurer manuellement):**
- [ ] `DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production`
- [ ] `SECRET_KEY=votre-cle-secrete`
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS=.railway.app,.up.railway.app`
- [ ] `CSRF_TRUSTED_ORIGINS=https://*.railway.app`

### **Variables JSReport (Optionnelles):**
- [ ] `JSREPORT_URL=https://votre-jsreport.railway.app`
- [ ] `JSREPORT_USERNAME=admin`
- [ ] `JSREPORT_PASSWORD=votre-password`
- [ ] `JSREPORT_TIMEOUT=120`

---

## ⚠️ **Points d'Attention**

### **Nom de Variable Spécial:**
```bash
# Railway génère:
MYSQLUSER=root  # ⚠️ Pas MYSQL_USER!

# Donc dans le code:
os.environ.get('MYSQLUSER')  # ✅ Correct
os.environ.get('MYSQL_USER')  # ❌ Incorrect
```

### **Variables Sensibles:**
```bash
# Ne jamais exposer en clair:
SECRET_KEY=xxx
MYSQL_PASSWORD=xxx
JSREPORT_PASSWORD=xxx
```

---

## ✅ **Résultat Final**

Avec les noms de variables corrects:
- ✅ **Correspondance parfaite Railway ↔ Django**
- ✅ **Connexion MySQL garantie**
- ✅ **Plus d'erreur de variable manquante**
- ✅ **Déploiement Railway robuste**

**Les variables correspondent maintenant parfaitement! 🎉**