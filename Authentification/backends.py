from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class Sensible_Case(ModelBackend):
    """
    Authentifie les utilisateurs en respectant strictement la casse du nom d'utilisateur.
    Ce backend remplace complètement le backend par défaut de Django.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Récupérer TOUS les utilisateurs avec ce nom (insensible à la casse)
            users = User.objects.filter(username__iexact=username)
            
            # Vérifier manuellement la casse EXACTE
            matching_user = None
            for user in users:
                if user.username == username:  # Comparaison stricte de la casse
                    matching_user = user
                    break
            
            if matching_user is None:
                # Aucun utilisateur trouvé avec cette casse exacte
                return None
                
        except User.DoesNotExist:
            return None
        except Exception:
            return None

        # Vérifie le mot de passe ET que l'utilisateur peut s'authentifier
        if matching_user.check_password(password) and self.user_can_authenticate(matching_user):
            return matching_user
        
        return None
    
    def get_user(self, user_id):
        """
        Récupère un utilisateur par son ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
