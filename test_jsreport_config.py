#!/usr/bin/env python
"""
Test de la nouvelle configuration JSReport pour Railway
"""
import json
import os

def test_jsreport_config():
    """Teste la configuration JSReport"""
    print("🧪 TEST CONFIGURATION JSREPORT")
    print("=" * 40)
    
    # Vérifier que le fichier de configuration existe
    config_file = "jsreport.config.json"
    if os.path.exists(config_file):
        print(f"✅ Fichier {config_file} trouvé")
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print("✅ Configuration JSON valide")
            
            # Vérifier les éléments critiques
            checks = [
                ("httpPort", config.get("httpPort") == 5488),
                ("store.provider", config.get("store", {}).get("provider") == "fs"),
                ("store.dataDirectory", config.get("store", {}).get("dataDirectory") == "/app/data"),
                ("authentication.enabled", config.get("authentication", {}).get("enabled") == True),
                ("chrome-pdf args", "--no-sandbox" in str(config.get("extensions", {}).get("chrome-pdf", {}).get("launchOptions", {}).get("args", [])))
            ]
            
            print("\n📋 Vérifications de configuration:")
            for check_name, result in checks:
                status = "✅" if result else "❌"
                print(f"   {status} {check_name}")
            
            all_good = all(result for _, result in checks)
            
            if all_good:
                print("\n🎉 Configuration JSReport parfaite pour Railway !")
                return True
            else:
                print("\n⚠️ Quelques éléments à vérifier dans la configuration")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON: {e}")
            return False
    else:
        print(f"❌ Fichier {config_file} manquant")
        return False

def test_dockerfile():
    """Teste le Dockerfile JSReport"""
    print("\n🐳 TEST DOCKERFILE JSREPORT")
    print("=" * 40)
    
    dockerfile = "Dockerfile.jsreport"
    if os.path.exists(dockerfile):
        print(f"✅ Fichier {dockerfile} trouvé")
        
        with open(dockerfile, 'r') as f:
            content = f.read()
        
        # Vérifications critiques
        checks = [
            ("FROM jsreport/jsreport", "FROM jsreport/jsreport" in content),
            ("mkdir -p /app/data", "mkdir -p /app/data" in content),
            ("COPY jsreport.config.json", "COPY jsreport.config.json" in content),
            ("jsreport start command", '"jsreport", "start"' in content),
            ("config=jsreport.config.json", "config=jsreport.config.json" in content)
        ]
        
        print("📋 Vérifications Dockerfile:")
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
        
        all_good = all(result for _, result in checks)
        
        if all_good:
            print("🎉 Dockerfile JSReport parfait pour Railway !")
            return True
        else:
            print("⚠️ Quelques éléments à vérifier dans le Dockerfile")
            return False
    else:
        print(f"❌ Fichier {dockerfile} manquant")
        return False

def show_deployment_summary():
    """Affiche le résumé du déploiement"""
    print("\n📋 RÉSUMÉ DÉPLOIEMENT RAILWAY")
    print("=" * 40)
    print("1. Commitez les fichiers:")
    print("   git add jsreport.config.json Dockerfile.jsreport")
    print("   git commit -m 'Fix JSReport config for Railway'")
    print("   git push")
    print()
    print("2. Sur Railway:")
    print("   • New Project > Empty Project")
    print("   • New Service > GitHub Repo")
    print("   • Settings > Dockerfile Path: Dockerfile.jsreport")
    print("   • Networking > Generate Domain")
    print()
    print("3. Configurez Django avec la nouvelle URL JSReport")
    print()
    print("4. Importez vos templates dans JSReport Railway")
    print()
    print("🎯 Résultat: Impression des factures fonctionnelle en ligne !")

if __name__ == "__main__":
    print("🚀 TEST CONFIGURATION JSREPORT RAILWAY")
    print("=" * 50)
    
    config_ok = test_jsreport_config()
    dockerfile_ok = test_dockerfile()
    
    if config_ok and dockerfile_ok:
        print("\n🎉 CONFIGURATION PARFAITE !")
        print("Vous pouvez déployer sur Railway en toute confiance.")
        show_deployment_summary()
    else:
        print("\n⚠️ CONFIGURATION À CORRIGER")
        print("Vérifiez les éléments marqués ❌ ci-dessus.")
    
    print("\n📚 Documentation complète:")
    print("   • DÉPLOIEMENT_JSREPORT_CORRIGÉ.md")
    print("   • CORRECTION_ERREUR_JSREPORT.md")