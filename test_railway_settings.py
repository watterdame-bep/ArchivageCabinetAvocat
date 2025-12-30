#!/usr/bin/env python3
"""
Test pour vérifier que Railway utilise bien settings_production.py
"""

import os
import sys

def test_settings_detection():
    """Teste quelle configuration Django est utilisée"""
    print("🧪 Test de détection des settings Django\n")
    
    # Test 1: Sans DJANGO_SETTINGS_MODULE
    print("1️⃣ Test sans DJANGO_SETTINGS_MODULE:")
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        del os.environ['DJANGO_SETTINGS_MODULE']
    
    try:
        import django
        from django.conf import settings
        django.setup()
        
        # Vérifier si c'est settings.py ou settings_production.py
        if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
            print("  ✅ STATICFILES_DIRS configuré (probablement settings_production.py)")
        else:
            print("  ❌ STATICFILES_DIRS vide (probablement settings.py par défaut)")
        
        print(f"  DEBUG = {settings.DEBUG}")
        print(f"  STATICFILES_DIRS = {settings.STATICFILES_DIRS}")
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
    
    # Reset Django
    if hasattr(django, 'apps'):
        django.apps.apps.clear_cache()
    
    # Test 2: Avec DJANGO_SETTINGS_MODULE = settings_production
    print("\n2️⃣ Test avec DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production:")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
    
    try:
        # Recharger Django avec les nouveaux settings
        import importlib
        importlib.reload(django)
        from django.conf import settings
        django.setup()
        
        print(f"  DEBUG = {settings.DEBUG}")
        print(f"  STATICFILES_DIRS = {settings.STATICFILES_DIRS}")
        
        if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
            print("  ✅ STATICFILES_DIRS configuré correctement")
        else:
            print("  ❌ STATICFILES_DIRS toujours vide")
            
        # Vérifier WhiteNoise
        if 'whitenoise' in str(settings.MIDDLEWARE).lower():
            print("  ✅ WhiteNoise middleware présent")
        else:
            print("  ❌ WhiteNoise middleware absent")
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def test_start_railway_script():
    """Teste le script start_railway.py"""
    print("\n🚀 Test du script start_railway.py\n")
    
    # Lire le contenu du script
    try:
        with open('start_railway.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = []
        
        # Vérifier DJANGO_SETTINGS_MODULE
        if 'DJANGO_SETTINGS_MODULE' in content and 'settings_production' in content:
            checks.append("✅ DJANGO_SETTINGS_MODULE défini pour settings_production")
        else:
            checks.append("❌ DJANGO_SETTINGS_MODULE non défini ou incorrect")
        
        # Vérifier collectstatic avec settings
        if '--settings=CabinetAvocat.settings_production' in content:
            checks.append("✅ collectstatic utilise settings_production")
        else:
            checks.append("❌ collectstatic n'utilise pas settings_production")
        
        # Vérifier migrate avec settings
        if 'migrate --noinput --settings=CabinetAvocat.settings_production' in content:
            checks.append("✅ migrate utilise settings_production")
        else:
            checks.append("❌ migrate n'utilise pas settings_production")
        
        print("📋 Vérifications du script:")
        for check in checks:
            print(f"  {check}")
        
        return all("✅" in check for check in checks)
        
    except Exception as e:
        print(f"❌ Erreur lecture script: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔍 Test de configuration Railway Settings\n")
    
    try:
        test_settings_detection()
        script_ok = test_start_railway_script()
        
        print("\n" + "="*50)
        print("📋 RÉSULTAT FINAL")
        print("="*50)
        
        if script_ok:
            print("🎉 CONFIGURATION CORRECTE")
            print("✅ Railway utilisera settings_production.py")
            print("✅ STATICFILES_DIRS sera pris en compte")
            print("✅ WhiteNoise fonctionnera correctement")
        else:
            print("❌ PROBLÈMES DÉTECTÉS")
            print("⚠️ Railway pourrait utiliser settings.py par défaut")
        
        print(f"\n🚀 Prochaines étapes:")
        print(f"  1. Commit les corrections du script")
        print(f"  2. Déployer sur Railway")
        print(f"  3. Vérifier les logs Railway")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()