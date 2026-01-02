
#!/usr/bin/env python
"""
Ajout de la variable MYSQLPORT manquante
"""
import os

# Ajouter MYSQLPORT si manquante
if not os.environ.get('MYSQLPORT'):
    os.environ['MYSQLPORT'] = '3306'
    print("✅ Variable MYSQLPORT ajoutée: 3306")
else:
    print(f"ℹ️ Variable MYSQLPORT déjà définie: {os.environ.get('MYSQLPORT')}")
