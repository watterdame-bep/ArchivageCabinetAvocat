from .signals import set_current_request, set_current_user


class ActivityLogMiddleware:
    """
    Middleware pour capturer l'utilisateur et la requête courante
    pour les logs d'activités
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Stocker la requête et l'utilisateur dans le thread local
        set_current_request(request)
        
        if hasattr(request, 'user') and request.user.is_authenticated:
            set_current_user(request.user)
        else:
            set_current_user(None)
        
        response = self.get_response(request)
        
        # Nettoyer après la requête
        set_current_request(None)
        set_current_user(None)
        
        return response