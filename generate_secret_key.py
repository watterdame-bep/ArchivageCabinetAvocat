#!/usr/bin/env python
"""
Générateur de SECRET_KEY Django pour Railway
"""
import secrets
import string

def generate_secret_key(length=50):
    """Générer une SECRET_KEY Django sécurisée"""
    # Caractères autorisés pour Django SECRET_KEY
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    
    # Générer une clé aléatoire
    secret_key = ''.join(secrets.choice(chars) for _ in range(length))
    
    return secret_key

def main():
    print("🔑 Générateur de SECRET_KEY Django")
    print("=" * 40)
    
    # Générer une nouvelle clé
    new_key = generate_secret_key()
    
    print(f"✅ Nouvelle SECRET_KEY générée :")
    print(f"SECRET_KEY={new_key}")
    
    print("\n📋 Instructions :")
    print("1. Copiez la SECRET_KEY ci-dessus")
    print("2. Dans Railway Dashboard → Variables → Ajouter :")
    print("   Nom: SECRET_KEY")
    print(f"   Valeur: {new_key}")
    print("\n⚠️  IMPORTANT: Gardez cette clé secrète et ne la partagez jamais!")
    
    # Afficher aussi la clé actuelle du projet
    current_key = 'django-insecure-9nb+f!7lb30p1bxdd4pw+dbq_z7h%zn^8#i_=vpcbvw(-f$sd*'
    print(f"\n🔍 SECRET_KEY actuelle du projet :")
    print(f"SECRET_KEY={current_key}")
    print("\n💡 Vous pouvez utiliser l'actuelle ou la nouvelle selon vos préférences.")

if __name__ == '__main__':
    main()