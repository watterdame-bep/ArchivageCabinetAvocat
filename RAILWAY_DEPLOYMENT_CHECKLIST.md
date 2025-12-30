# 🚀 Checklist Déploiement Railway - Cabinet Avocat

## ✅ Pré-déploiement (Local)

### 1. Vérifications des fichiers
- [ ] `nixpacks.toml` mis à jour avec diagnostics
- [ ] `railway.json` configuré avec buildCommand
- [ ] `start_railway.py` contient collectstatic
- [ ] `settings_production.py` WhiteNoise configuré
- [ ] `urls.py` sert les fichiers statiques en production

### 2. Test local
```bash
# Tester collectstatic local
python manage.py collectstatic --noinput --clear --settings=CabinetAvocat.settings_production

# Vérifier les fichiers critiques
ls staticfiles/css/style.css
ls staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css
```

## 🚀 Déploiement Railway

### 1. Push des modifications
```bash
git add .
git commit -m "Fix Railway static files with enhanced build configuration"
git push origin main
```

### 2. Variables Railway à vérifier
- [ ] `DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production`
- [ ] `DEBUG=False`
- [ ] Variables MySQL (auto-générées)
- [ ] `SECRET_KEY` (généré)

### 3. Surveillance du déploiement
- [ ] Logs Railway: "Collection des fichiers statiques..."
- [ ] Logs Railway: "X static files copied"
- [ ] Logs Railway: "MySQL est disponible!"
- [ ] Logs Railway: "Starting gunicorn"

## 🧪 Tests post-déploiement

### 1. Tests d'interface
- [ ] Page de login s'affiche correctement
- [ ] CSS Bootstrap chargé (design correct)
- [ ] Pas d'erreurs 404 dans la console navigateur

### 2. Tests d'URLs directes
```
https://votre-app.up.railway.app/static/css/style.css
https://votre-app.up.railway.app/static/assets/vendor_components/bootstrap/dist/css/bootstrap.css
https://votre-app.up.railway.app/test-static/ (si endpoint ajouté)
```

### 3. Tests fonctionnels
- [ ] Login utilisateur fonctionne
- [ ] Navigation dans l'application
- [ ] Génération de rapports (après upload JSReport)

## 🚨 Dépannage si problème persiste

### 1. Forcer un rebuild complet
```bash
# Dans Railway Dashboard
Settings > Deployments > Redeploy (force rebuild)
```

### 2. Vérifier les logs Railway
- Rechercher "collectstatic" dans les logs de build
- Vérifier qu'aucune erreur n'apparaît pendant la collection
- S'assurer que les fichiers sont bien copiés

### 3. Debug avancé
- Ajouter l'endpoint de test `/test-static/`
- Vérifier les variables d'environnement Railway
- Tester avec `WHITENOISE_AUTOREFRESH = True`

## 📞 Support
Si le problème persiste après toutes ces étapes, le problème peut venir de:
1. Configuration Railway spécifique
2. Problème de cache Railway
3. Configuration réseau Railway

Dans ce cas, contacter le support Railway avec les logs de build.
