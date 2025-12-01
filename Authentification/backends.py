from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class Sensible_Case(ModelBackend):
    """
    Authentifie les utilisateurs en respectant la casse du nom d'utilisateur.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # On recherche l’utilisateur AVEC respect strict de la casse
            user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            return None

        # Vérifie le mot de passe
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
