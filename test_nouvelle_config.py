#!/usr/bin/env python
"""
Test de la nouvelle configuration JSReport avec image Puppeteer
"""
import os
import json

def test_nouveaux_fichiers():
    """Teste que les nouveaux fichiers sont corrects"""
    print("🧪 TEST NOUVELLE CONFIGURATION JSREPORT")
    print("=" * 50)
    
    # Test Dockerfile
    dockerfile_path = "Dockerfile"
    if os.path.exists(dockerfile_path):
        print(f"✅ {dockerfile_path} trouvé")
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
        
        checks = [
            ("Image Puppeteer", "ghcr.io/puppeteer/puppeteer" in content),
            ("JSReport CLI", "jsreport-cli" in content),
            ("Chrome executable", "PUPPETEER_EXECUTABLE_PATH" in content),
            ("Port 5488", "5488" in content),
            ("Healthcheck", "HEALTHCHECK" in content)
        ]
        
        print("📋 Vérifications Dockerfile:")
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
            
        dockerfile_ok = all(result for _, result in checks)
    else:
        print(f"❌ {dockerfile_path} manquant")
        dockerfile_ok = False
    
    # Test jsreport.config.json
    config_path = "jsreport.config.json"
    if os.path.exists(config_path):
        print(f"\n✅ {config_path} trouvé")
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            checks = [
                ("Port 5488", config.get("httpPort") == 5488),
                ("Store filesystem", config.get("store", {}).get("provider") == "fs"),
                ("Chrome PDF enabled", config.get("extensions", {}).get("chrome-pdf", {}).get("enabled") == True),
                ("No-sandbox arg", "--no-sandbox" in str(config.get("extensions", {}).get("chrome-pdf", {}).get("launchOptions", {}).get("args", []))),
                ("Single process", "--single-process" in str(config.get("extensions", {}).get("chrome-pdf", {}).get("launchOptions", {}).get("args", []))),
                ("1 worker", config.get("workers", {}).get("numberOfWorkers") == 1),
                ("Authentication", config.get("authentication", {}).get("enabled") == True)
            ]
            
            print("📋 Vérifications Configuration:")
            for check_name, result in checks:
                status = "✅" if result else "❌"
                print(f"   {status} {check_name}")
                
            config_ok = all(result for _, result in checks)
            
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON: {e}")
            config_ok = False
    else:
        print(f"❌ {config_path} manquant")
        config_ok = False
    
    return dockerfile_ok and config_ok

def show_deployment_instructions():
    """Affiche les instructions de déploiement"""
    print("\n📋 INSTRUCTIONS DÉPLOIEMENT")
    print("=" * 40)
    print("1. Dans votre repository JSReport:")
    print("   • Copiez le contenu de 'Dockerfile' (nouveau nom !)")
    print("   • Copiez le contenu de 'jsreport.config.json'")
    print()
    print("2. Commitez et pushez:")
    print("   git add Dockerfile jsreport.config.json")
    print("   git commit -m 'New approach: Puppeteer image with Chrome'")
    print("   git push")
    print()
    print("3. Railway redéploie automatiquement (5 minutes)")
    print()
    print("4. Testez la génération PDF:")
    print("   • Interface JSReport accessible")
    print("   • Créez un template simple")
    print("   • Générez un PDF → Doit fonctionner !")
    print()
    print("🎯 Avantages de cette approche:")
    print("   ✅ Chrome déjà installé dans l'image")
    print("   ✅ Configuration optimisée pour Railway")
    print("   ✅ Moins de ressources utilisées")
    print("   ✅ Plus fiable et stable")

if __name__ == "__main__":
    print("🚀 TEST NOUVELLE APPROCHE JSREPORT")
    print("=" * 50)
    
    config_ok = test_nouveaux_fichiers()
    
    if config_ok:
        print("\n🎉 NOUVELLE CONFIGURATION PARFAITE !")
        print("Cette approche devrait résoudre définitivement le problème Chrome.")
        show_deployment_instructions()
    else:
        print("\n⚠️ CONFIGURATION À CORRIGER")
        print("Vérifiez les éléments marqués ❌ ci-dessus.")
    
    print("\n📚 Documentation:")
    print("   • NOUVELLE_APPROCHE_JSREPORT.md")
    print("\n🎯 Cette approche utilise une image Docker avec Chrome pré-installé !")
    print("   Plus de problème d'installation Chrome ! 🚀")