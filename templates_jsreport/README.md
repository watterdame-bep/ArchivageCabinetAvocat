# Templates JSReport - Cabinet Avocat

## Vue d'ensemble

Ce dossier contient tous les templates JSReport pour la génération de rapports PDF dans l'application Cabinet Avocat.

## Structure des Templates

Chaque rapport a deux fichiers:
- **`.html`** - Template HTML avec syntaxe Handlebars
- **`.json`** - Configuration JSReport (engine, recipe, options PDF)

## Templates Disponibles

### 1. Rapport Agent (`rapport_agent`)
- **Fichiers**: `rapport_agent.html` + `rapport_agent.json`
- **Usage**: Génération de rapports pour les agents
- **Données**: Informations agent, statistiques, activités

### 2. Rapport Client (`rapport_client`)
- **Fichiers**: `rapport_client.html` + `rapport_client.json`
- **Usage**: Génération de rapports pour les clients
- **Données**: Informations client, dossiers, paiements

### 3. Rapport Juridiction (`rapport_juridiction`)
- **Fichiers**: `rapport_juridiction.html` + `rapport_juridiction.json`
- **Usage**: Génération de rapports par juridiction
- **Données**: Statistiques juridiction, dossiers associés

### 4. Rapport Commune (`rapport_commune`)
- **Fichiers**: `rapport_commune.html` + `rapport_commune.json`
- **Usage**: Génération de rapports par commune
- **Données**: Statistiques commune, activités locales

### 5. Rapport Dossier (`rapport_dossier`)
- **Fichiers**: `rapport_dossier.html` + `rapport_dossier.json`
- **Usage**: Génération de rapports détaillés de dossiers
- **Données**: Détails dossier, historique, documents

### 6. Rapport Activités Internes (`rapport_activites_internes`)
- **Fichiers**: `rapport_activites_internes.html` + `rapport_activites_internes.json`
- **Usage**: Génération de rapports d'activités internes
- **Données**: Activités internes, statistiques période

### 7. Facture Paiement (`facture_paiement`)
- **Fichiers**: `facture_paiement.html` + `facture_paiement.json`
- **Usage**: Génération de factures pour les clients
- **Données**: Détails facture, client, montants

### 8. Facture Dossier (`Facture_dossier`)
- **Fichiers**: `Facture_dossier.html` + `Facture_dossier.json`
- **Usage**: Génération de factures spécifiques à un dossier
- **Données**: Détails dossier, prestations, montants

### 9. Extrait de Compte Client (`Extrait_de_compte_client`)
- **Fichiers**: `Extrait_de_compte_client.html` + `Extrait_de_compte_client.json`
- **Usage**: Génération d'extraits de compte pour les clients
- **Données**: Mouvements de compte, soldes, historique

## Configuration des Templates

### Format JSON Standard
```json
{
  "name": "nom_template",
  "engine": "handlebars",
  "recipe": "chrome-pdf",
  "chrome": {
    "format": "A4",
    "marginTop": "1cm",
    "marginBottom": "1cm",
    "marginLeft": "1cm",
    "marginRight": "1cm",
    "landscape": false,
    "printBackground": true
  },
  "helpers": "",
  "data": {}
}
```

### Options Chrome PDF
- **format**: A4, A3, Letter, Legal, etc.
- **margins**: Top, Bottom, Left, Right (cm, mm, in)
- **landscape**: true/false pour orientation
- **printBackground**: true pour imprimer les couleurs de fond

## Syntaxe Handlebars

### Variables Simples
```html
<h1>{{titre}}</h1>
<p>Client: {{client.nom}} {{client.prenom}}</p>
```

### Conditions
```html
{{#if client}}
  <p>Client: {{client.nom}}</p>
{{else}}
  <p>Aucun client sélectionné</p>
{{/if}}
```

### Boucles
```html
{{#each dossiers}}
  <tr>
    <td>{{numero}}</td>
    <td>{{objet}}</td>
    <td>{{statut}}</td>
  </tr>
{{/each}}
```

### Helpers Personnalisés
```html
{{formatDate date_creation}}
{{formatCurrency montant}}
{{formatNumber total}}
```

## Personnalisation des Templates

### 1. Modifier le HTML
Éditez les fichiers `.html` pour:
- Ajouter votre contenu
- Personnaliser le design
- Ajouter des tableaux, graphiques
- Inclure logo et en-têtes

### 2. Ajuster la Configuration
Modifiez les fichiers `.json` pour:
- Changer le format de page
- Ajuster les marges
- Modifier l'orientation
- Ajouter des helpers

### 3. Tester Localement
```bash
# Démarrer JSReport local
jsreport start

# Importer les templates
python scripts/upload_jsreport_templates.py
```

## Upload vers Railway

### 1. Configuration
```bash
export JSREPORT_SERVICE_URL="https://votre-service.up.railway.app"
export JSREPORT_USERNAME="admin"
export JSREPORT_PASSWORD="votre-mot-de-passe"
```

### 2. Test de Connexion
```bash
python scripts/test_jsreport_connection.py
```

### 3. Upload des Templates
```bash
python scripts/upload_jsreport_templates.py
```

## Intégration Django

### Configuration dans settings_production.py
```python
JSREPORT_CONFIG = {
    'url': 'https://votre-service.up.railway.app',
    'username': 'admin',
    'password': 'votre-mot-de-passe',
    'templates': {
        'rapport_agent': 'rapport_agent',
        'rapport_client': 'rapport_client',
        'rapport_juridiction': 'rapport_juridiction',
        'rapport_commune': 'rapport_commune',
        'rapport_dossier': 'rapport_dossier',
        'rapport_activites_internes': 'rapport_activites_internes',
        'facture_paiement': 'facture_paiement',
        'facture_dossier': 'Facture_dossier',
        'extrait_compte_client': 'Extrait_de_compte_client',
        # ... autres templates
    }
}
```

### Utilisation dans les Vues
```python
from utils.jsreport_service import generate_pdf

def imprimer_rapport_agent(request):
    data = {
        'agents': Agent.objects.all(),
        'date_generation': timezone.now()
    }
    
    pdf_content = generate_pdf('rapport_agent', data)
    
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_agent.pdf"'
    return response
```

## Dépannage

### Erreurs Communes

1. **Template non trouvé**
   - Vérifier le nom dans JSREPORT_CONFIG
   - Vérifier l'upload du template

2. **Erreur de syntaxe Handlebars**
   - Vérifier les accolades {{}}
   - Tester avec des données simples

3. **Problème de connexion**
   - Vérifier JSREPORT_SERVICE_URL
   - Tester avec test_jsreport_connection.py

4. **PDF mal formaté**
   - Ajuster les marges dans .json
   - Vérifier les styles CSS

### Logs et Debug
```bash
# Voir les logs Railway
railway logs

# Tester un template spécifique
curl -u admin:password \
  -H "Content-Type: application/json" \
  -d '{"template":{"name":"rapport_agent"},"data":{}}' \
  https://votre-service.up.railway.app/api/report
```

## Bonnes Pratiques

1. **Toujours tester localement** avant l'upload
2. **Utiliser des données de test** réalistes
3. **Optimiser les images** pour réduire la taille PDF
4. **Prévoir les cas d'erreur** (données manquantes)
5. **Documenter les modifications** importantes

## Support

Pour toute question ou problème:
1. Consulter les logs Railway
2. Tester avec les scripts fournis
3. Vérifier la documentation JSReport officielle