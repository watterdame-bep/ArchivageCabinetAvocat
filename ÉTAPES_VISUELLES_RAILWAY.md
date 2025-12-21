# 📸 GUIDE VISUEL - JSReport sur Railway

## 🎯 ÉTAPES AVEC CAPTURES D'ÉCRAN SIMULÉES

---

## 1️⃣ CRÉER LE PROJET RAILWAY

### Page d'accueil Railway
```
┌─────────────────────────────────────────────────────────────┐
│ 🚂 Railway                                    [Login] [Sign Up] │
│                                                               │
│         Deploy from GitHub in seconds                        │
│                                                               │
│              [New Project]                                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Cliquez sur "New Project"**

### Sélection du type de projet
```
┌─────────────────────────────────────────────────────────────┐
│ Create a new project                                          │
│                                                               │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│ │   Deploy    │  │    Empty    │  │  Template   │           │
│ │from GitHub  │  │   Project   │  │   Gallery   │           │
│ │     Repo    │  │      👈     │  │             │           │
│ └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Cliquez sur "Empty Project"**

### Nommer le projet
```
┌─────────────────────────────────────────────────────────────┐
│ Project Name: [cabinet-avocat-jsreport          ]            │
│                                                               │
│                              [Create]                        │
└─────────────────────────────────────────────────────────────┘
```
**👆 Tapez "cabinet-avocat-jsreport" et cliquez "Create"**

---

## 2️⃣ AJOUTER LE SERVICE JSREPORT

### Dashboard du projet vide
```
┌─────────────────────────────────────────────────────────────┐
│ 📁 cabinet-avocat-jsreport                                   │
│                                                               │
│     No services yet                                           │
│                                                               │
│              [New Service]                                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Cliquez sur "New Service"**

### Sélection de la source
```
┌─────────────────────────────────────────────────────────────┐
│ Add a service                                                 │
│                                                               │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│ │   GitHub    │  │   Docker    │  │    Empty    │           │
│ │    Repo     │  │    Image    │  │   Service   │           │
│ │     👈      │  │             │  │             │           │
│ └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Cliquez sur "GitHub Repo"**

### Sélection du repository
```
┌─────────────────────────────────────────────────────────────┐
│ Select Repository                                             │
│                                                               │
│ 🔍 Search repositories...                                    │
│                                                               │
│ ✓ votre-username/CabinetAvocat                               │
│                                                               │
│                              [Deploy]                        │
└─────────────────────────────────────────────────────────────┘
```
**👆 Sélectionnez votre repo et cliquez "Deploy"**

---

## 3️⃣ CONFIGURER LE SERVICE

### Settings du service
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Service Settings                                          │
│                                                               │
│ Build                                                         │
│ ├─ Root Directory: [/                    ]                   │
│ ├─ Build Command:  [                     ]                   │
│ └─ Dockerfile Path: [Dockerfile.jsreport ] 👈               │
│                                                               │
│ Deploy                                                        │
│ └─ Start Command:  [                     ]                   │
│                                                               │
│                              [Save]                          │
└─────────────────────────────────────────────────────────────┘
```
**👆 Ajoutez "Dockerfile.jsreport" et cliquez "Save"**

---

## 4️⃣ AJOUTER LES VARIABLES D'ENVIRONNEMENT

### Page Variables
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Variables                                                 │
│                                                               │
│ No variables yet                                              │
│                                                               │
│                         [New Variable]                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Cliquez sur "New Variable"**

### Ajouter une variable
```
┌─────────────────────────────────────────────────────────────┐
│ Add Variable                                                  │
│                                                               │
│ Name:  [JSREPORT_USERNAME                    ]               │
│ Value: [admin                                ]               │
│                                                               │
│                              [Add]                           │
└─────────────────────────────────────────────────────────────┘
```
**👆 Répétez pour chaque variable:**
- `JSREPORT_USERNAME` = `admin`
- `JSREPORT_PASSWORD` = `VotreMotDePasseSecurise123`
- `JSREPORT_COOKIE_SECRET` = `VotreCleSecrete456`
- `NODE_ENV` = `production`

### Variables configurées
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Variables                                                 │
│                                                               │
│ JSREPORT_USERNAME        admin                               │
│ JSREPORT_PASSWORD        ••••••••••••••••••••••             │
│ JSREPORT_COOKIE_SECRET   ••••••••••••••••••••••             │
│ NODE_ENV                 production                          │
│                                                               │
│                         [New Variable]                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 5️⃣ RÉCUPÉRER L'URL PUBLIQUE

### Settings > Networking
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Settings > Networking                                     │
│                                                               │
│ Public Networking                                             │
│ ├─ No public URL yet                                         │
│ └─ [Generate Domain]  👈                                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Cliquez sur "Generate Domain"**

### URL générée
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Settings > Networking                                     │
│                                                               │
│ Public Networking                                             │
│ ├─ https://cabinet-avocat-jsreport-production.up.railway.app │
│ └─ [📋 Copy URL]                                             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Copiez cette URL !**

---

## 6️⃣ CONFIGURER DJANGO

### Aller dans votre service Django
```
┌─────────────────────────────────────────────────────────────┐
│ 📁 Vos projets Railway                                       │
│                                                               │
│ ┌─────────────────────┐  ┌─────────────────────┐           │
│ │ cabinet-avocat      │  │ cabinet-avocat-     │           │
│ │ (Django Principal)  │  │ jsreport            │           │
│ │        👈           │  │ (Nouveau)           │           │
│ └─────────────────────┘  └─────────────────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Cliquez sur votre projet Django principal**

### Modifier les variables Django
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Variables Django                                          │
│                                                               │
│ JSREPORT_URL             http://localhost:5488  ❌          │
│ JSREPORT_USERNAME        admin                               │
│ JSREPORT_PASSWORD        admin123                            │
│                                                               │
│                         [Edit] [New Variable]               │
└─────────────────────────────────────────────────────────────┘
```
**👆 Cliquez "Edit" sur JSREPORT_URL**

### Nouvelle URL
```
┌─────────────────────────────────────────────────────────────┐
│ Edit Variable                                                 │
│                                                               │
│ Name:  JSREPORT_URL                                          │
│ Value: [https://cabinet-avocat-jsreport-production.up.railway.app] │
│                                                               │
│                              [Save]                          │
└─────────────────────────────────────────────────────────────┘
```
**👆 Remplacez par votre URL JSReport et cliquez "Save"**

---

## 7️⃣ TESTER LA CONFIGURATION

### Test dans le navigateur
```
URL: https://votre-jsreport-url.railway.app/api/ping

Résultat attendu:
┌─────────────────────────────────────────────────────────────┐
│ OK                                                            │
└─────────────────────────────────────────────────────────────┘
```

### Interface JSReport
```
URL: https://votre-jsreport-url.railway.app

┌─────────────────────────────────────────────────────────────┐
│ 📊 JSReport Studio                                           │
│                                                               │
│ Username: [admin                    ]                        │
│ Password: [••••••••••••••••••••••  ]                        │
│                                                               │
│                         [Login]                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎉 RÉSULTAT FINAL

### Dashboard Railway avec 2 services
```
┌─────────────────────────────────────────────────────────────┐
│ 📁 cabinet-avocat-jsreport                                   │
│                                                               │
│ ┌─────────────────────┐  ┌─────────────────────┐           │
│ │ 🐍 Django Service   │  │ 📊 JSReport Service │           │
│ │ Status: ✅ Active   │  │ Status: ✅ Active   │           │
│ │ URL: django-url...  │  │ URL: jsreport-url.. │           │
│ └─────────────────────┘  └─────────────────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Test d'impression dans votre app
```
┌─────────────────────────────────────────────────────────────┐
│ 🧾 Facture Paiement                                         │
│                                                               │
│ Client: Jean Dupont                                           │
│ Montant: 500 USD                                              │
│                                                               │
│                    [📄 Imprimer Facture]                    │
│                           👆                                 │
│                    ✅ Fonctionne !                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 RÉCAPITULATIF DES ÉTAPES

1. ✅ **Railway** → New Project → "cabinet-avocat-jsreport"
2. ✅ **New Service** → GitHub Repo → Votre repository
3. ✅ **Settings** → Dockerfile Path: "Dockerfile.jsreport"
4. ✅ **Variables** → Ajouter 4 variables JSReport
5. ✅ **Networking** → Generate Domain → Copier URL
6. ✅ **Service Django** → Variables → Modifier JSREPORT_URL
7. ✅ **Tester** → /api/ping → Login JSReport → Importer templates

**🎯 Temps total: 15-20 minutes**
**🎉 Résultat: Impression des factures fonctionne en ligne !**