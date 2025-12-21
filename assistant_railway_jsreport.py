#!/usr/bin/env python
"""
Assistant interactif pour déployer JSReport sur Railway
"""
import os
import sys

def print_header():
    print("🚂" + "="*60 + "🚂")
    print("    ASSISTANT DÉPLOIEMENT JSREPORT SUR RAILWAY")
    print("🚂" + "="*60 + "🚂")
    print()

def etape_1_creation_projet():
    print("1️⃣ CRÉATION DU PROJET RAILWAY")
    print("-" * 40)
    print("📋 Actions à faire:")
    print("   • Allez sur: https://railway.app")
    print("   • Cliquez: 'New Project'")
    print("   • Sélectionnez: 'Empty Project'")
    print("   • Nom: 'cabinet-avocat-jsreport'")
    print("   • Cliquez: 'Create'")
    print()
    
    input("✅ Appuyez sur Entrée quand c'est fait...")
    print()

def etape_2_ajout_service():
    print("2️⃣ AJOUT DU SERVICE JSREPORT")
    print("-" * 40)
    print("📋 Actions à faire:")
    print("   • Dans votre projet, cliquez: 'New Service'")
    print("   • Sélectionnez: 'GitHub Repo'")
    print("   • Choisissez votre repository CabinetAvocat")
    print("   • Cliquez: 'Deploy'")
    print()
    
    input("✅ Appuyez sur Entrée quand c'est fait...")
    print()

def etape_3_configuration_dockerfile():
    print("3️⃣ CONFIGURATION DU DOCKERFILE")
    print("-" * 40)
    print("📋 Actions à faire:")
    print("   • Allez dans: 'Settings' du service")
    print("   • Section 'Build':")
    print("   • Dockerfile Path: 'Dockerfile.jsreport'")
    print("   • Cliquez: 'Save'")
    print()
    
    input("✅ Appuyez sur Entrée quand c'est fait...")
    print()

def etape_4_variables_environnement():
    print("4️⃣ VARIABLES D'ENVIRONNEMENT")
    print("-" * 40)
    print("📋 Variables à ajouter (une par une):")
    
    variables = [
        ("JSREPORT_USERNAME", "admin"),
        ("JSREPORT_PASSWORD", "VotreMotDePasseSecurise123"),
        ("JSREPORT_COOKIE_SECRET", "VotreCleSecrete456"),
        ("NODE_ENV", "production")
    ]
    
    for name, value in variables:
        print(f"   • {name} = {value}")
    
    print()
    print("📋 Actions à faire:")
    print("   • Allez dans: 'Variables'")
    print("   • Pour chaque variable:")
    print("     - Cliquez: 'New Variable'")
    print("     - Name: [nom de la variable]")
    print("     - Value: [valeur de la variable]")
    print("     - Cliquez: 'Add'")
    print()
    
    input("✅ Appuyez sur Entrée quand toutes les variables sont ajoutées...")
    print()

def etape_5_url_publique():
    print("5️⃣ GÉNÉRATION DE L'URL PUBLIQUE")
    print("-" * 40)
    print("📋 Actions à faire:")
    print("   • Allez dans: 'Settings' > 'Networking'")
    print("   • Cliquez: 'Generate Domain'")
    print("   • Railway génère une URL comme:")
    print("     https://cabinet-avocat-jsreport-production.up.railway.app")
    print()
    
    url = input("📝 Collez ici l'URL générée: ")
    
    if url.strip():
        print(f"✅ URL enregistrée: {url}")
        
        # Test de l'URL
        print()
        print("🧪 TESTEZ VOTRE URL:")
        print(f"   • Ouvrez: {url}/api/ping")
        print("   • Résultat attendu: 'OK'")
        print()
        
        test_ok = input("✅ Le test /api/ping fonctionne-t-il ? (o/n): ").lower().startswith('o')
        
        if test_ok:
            print("🎉 Parfait ! JSReport est accessible.")
            return url
        else:
            print("❌ Problème détecté. Vérifiez:")
            print("   • Le service est bien 'Active'")
            print("   • Les variables sont correctes")
            print("   • Attendez 2-3 minutes et réessayez")
            return None
    else:
        print("❌ URL manquante. Recommencez cette étape.")
        return None

def etape_6_configuration_django(jsreport_url):
    print("6️⃣ CONFIGURATION DU SERVICE DJANGO")
    print("-" * 40)
    print("📋 Actions à faire:")
    print("   • Allez dans votre AUTRE projet Railway (Django principal)")
    print("   • Allez dans: 'Variables'")
    print("   • Modifiez ou ajoutez ces variables:")
    print()
    print(f"   JSREPORT_URL = {jsreport_url}")
    print("   JSREPORT_USERNAME = admin")
    print("   JSREPORT_PASSWORD = VotreMotDePasseSecurise123")
    print("   JSREPORT_TIMEOUT = 120")
    print()
    print("⚠️ IMPORTANT: Utilisez exactement la même password que dans JSReport")
    print()
    
    input("✅ Appuyez sur Entrée quand c'est fait...")
    
    print("🔄 Railway va redéployer automatiquement votre service Django...")
    print("   Attendez que le statut redevienne 'Active'")
    print()
    
    input("✅ Appuyez sur Entrée quand Django est redéployé...")
    print()

def etape_7_templates():
    print("7️⃣ IMPORT DES TEMPLATES")
    print("-" * 40)
    print("📋 Actions à faire:")
    print()
    print("🔹 ÉTAPE A: Exporter depuis JSReport local")
    print("   • Ouvrez: http://localhost:5488")
    print("   • Login: admin / admin123")
    print("   • Pour chaque template:")
    print("     - Cliquez sur le template")
    print("     - Actions > Export")
    print("     - Sauvegardez le fichier .json")
    print()
    
    input("✅ Appuyez sur Entrée quand l'export local est fait...")
    
    print("🔹 ÉTAPE B: Importer dans JSReport Railway")
    print(f"   • Ouvrez votre JSReport Railway")
    print("   • Login: admin / VotreMotDePasseSecurise123")
    print("   • Pour chaque template:")
    print("     - New > Template")
    print("     - Import")
    print("     - Sélectionnez le fichier .json")
    print()
    print("📋 Templates requis:")
    print("   ✅ Facture_paiement_client")
    print("   ✅ Facture_dossier")
    print("   ✅ Extrait_de_compte_client")
    print()
    
    input("✅ Appuyez sur Entrée quand tous les templates sont importés...")
    print()

def etape_8_test_final():
    print("8️⃣ TEST FINAL")
    print("-" * 40)
    print("🧪 Tests à effectuer:")
    print()
    
    print("🔹 Test 1: Configuration")
    print("   cd CabinetAvocat")
    print("   python test_jsreport_quick.py")
    print("   Résultat attendu: ✅ URL semble correcte")
    print()
    
    test1 = input("✅ Test 1 réussi ? (o/n): ").lower().startswith('o')
    
    if test1:
        print("🔹 Test 2: Impression réelle")
        print("   • Allez sur votre application Railway")
        print("   • Créez un paiement")
        print("   • Cliquez 'Imprimer facture'")
        print("   • Le PDF doit se télécharger")
        print()
        
        test2 = input("✅ Test 2 réussi ? (o/n): ").lower().startswith('o')
        
        if test2:
            print("🎉🎉🎉 FÉLICITATIONS ! 🎉🎉🎉")
            print("JSReport fonctionne parfaitement en ligne !")
            return True
        else:
            print("❌ Problème d'impression détecté.")
            return False
    else:
        print("❌ Problème de configuration détecté.")
        return False

def diagnostic_problemes():
    print("🔧 DIAGNOSTIC DES PROBLÈMES")
    print("-" * 40)
    print("📋 Vérifications à faire:")
    print()
    print("1. Service JSReport:")
    print("   • Status: Active ?")
    print("   • URL accessible ?")
    print("   • Variables correctes ?")
    print()
    print("2. Service Django:")
    print("   • JSREPORT_URL mise à jour ?")
    print("   • Credentials identiques ?")
    print("   • Service redéployé ?")
    print()
    print("3. Templates:")
    print("   • Tous importés ?")
    print("   • Noms exacts ?")
    print("   • Pas d'erreurs dans JSReport ?")
    print()
    print("🛠️ Scripts de diagnostic:")
    print("   python diagnostic_jsreport_railway.py")
    print("   python test_jsreport_production.py")

def main():
    print_header()
    
    print("Cet assistant va vous guider étape par étape pour déployer JSReport sur Railway.")
    print("Suivez chaque étape attentivement.")
    print()
    
    continuer = input("🚀 Prêt à commencer ? (o/n): ").lower().startswith('o')
    
    if not continuer:
        print("👋 À bientôt ! Relancez quand vous êtes prêt.")
        return
    
    print()
    
    # Étapes du déploiement
    etape_1_creation_projet()
    etape_2_ajout_service()
    etape_3_configuration_dockerfile()
    etape_4_variables_environnement()
    
    jsreport_url = etape_5_url_publique()
    if not jsreport_url:
        print("❌ Impossible de continuer sans URL JSReport.")
        print("💡 Relancez l'assistant après avoir résolu le problème.")
        return
    
    etape_6_configuration_django(jsreport_url)
    etape_7_templates()
    
    success = etape_8_test_final()
    
    if success:
        print()
        print("🎯 MISSION ACCOMPLIE !")
        print("Votre JSReport fonctionne maintenant en production Railway.")
        print("Les factures peuvent être imprimées en ligne ! 🎉")
    else:
        print()
        print("🔧 DIAGNOSTIC NÉCESSAIRE")
        diagnostic_problemes()
    
    print()
    print("📚 Documentation complète:")
    print("   • GUIDE_JSREPORT_RAILWAY_DÉTAILLÉ.md")
    print("   • ÉTAPES_VISUELLES_RAILWAY.md")
    print("   • RÉSOLUTION_JSREPORT_FINAL.md")

if __name__ == "__main__":
    main()