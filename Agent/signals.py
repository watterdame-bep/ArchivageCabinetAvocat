from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from threading import local

# Import différé pour éviter les imports circulaires
def get_activity_models():
    from .models_activity import ActivityLog, ActivityLogManager
    return ActivityLog, ActivityLogManager

def get_current_user_model():
    from django.contrib.auth import get_user_model
    return get_user_model()

# Thread local storage pour stocker les informations de la requête
_thread_locals = local()


def set_current_request(request):
    """Stocke la requête courante dans le thread local"""
    _thread_locals.request = request


def get_current_request():
    """Récupère la requête courante depuis le thread local"""
    return getattr(_thread_locals, 'request', None)


def set_current_user(user):
    """Stocke l'utilisateur courant dans le thread local"""
    _thread_locals.user = user


def get_current_user():
    """Récupère l'utilisateur courant depuis le thread local"""
    return getattr(_thread_locals, 'user', None)


# Signaux pour les dossiers
@receiver(post_save, sender='Dossier.dossier')
def log_dossier_activity(sender, instance, created, **kwargs):
    """Log les activités sur les dossiers"""
    user = get_current_user()
    request = get_current_request()
    
    if user and user.is_authenticated:
        ActivityLog, ActivityLogManager = get_activity_models()
        if created:
            ActivityLogManager.log_dossier_created(user, instance, request)
        else:
            ActivityLogManager.log_dossier_updated(user, instance, request)


# Signaux pour les documents
@receiver(post_save, sender='Dossier.PieceDossier')
def log_document_added(sender, instance, created, **kwargs):
    """Log l'ajout de documents"""
    if created:
        user = get_current_user()
        request = get_current_request()
        
        if user and user.is_authenticated:
            ActivityLog, ActivityLogManager = get_activity_models()
            ActivityLogManager.log_document_added(user, instance, instance.dossier, request)


@receiver(pre_delete, sender='Dossier.PieceDossier')
def log_document_deletion_prep(sender, instance, **kwargs):
    """Prépare les données avant suppression du document"""
    _thread_locals.deleted_document_title = instance.titre
    _thread_locals.deleted_document_dossier = instance.dossier


@receiver(post_delete, sender='Dossier.PieceDossier')
def log_document_deleted(sender, **kwargs):
    """Log la suppression de documents"""
    user = get_current_user()
    request = get_current_request()
    
    if user and user.is_authenticated:
        document_title = getattr(_thread_locals, 'deleted_document_title', 'Document inconnu')
        dossier = getattr(_thread_locals, 'deleted_document_dossier', None)
        
        if dossier:
            ActivityLog, ActivityLogManager = get_activity_models()
            ActivityLogManager.log_document_deleted(user, document_title, dossier, request)


# Signaux pour les déclarations
@receiver(post_save, sender='Dossier.DeclarationDossier')
def log_declaration_activity(sender, instance, created, **kwargs):
    """Log les activités sur les déclarations"""
    user = get_current_user()
    request = get_current_request()
    
    if user and user.is_authenticated:
        ActivityLog, ActivityLogManager = get_activity_models()
        if created:
            ActivityLogManager.log_declaration_added(user, instance, request)
        else:
            ActivityLogManager.log_declaration_updated(user, instance, request)


# Signaux pour les paiements
@receiver(post_save, sender='paiement.Paiement')
def log_payment_activity(sender, instance, created, **kwargs):
    """Log les activités de paiement"""
    if created:
        user = get_current_user()
        request = get_current_request()
        
        if user and user.is_authenticated:
            ActivityLog, ActivityLogManager = get_activity_models()
            ActivityLogManager.log_payment_recorded(user, instance, request)


# Signaux pour les agents
@receiver(post_save, sender='Agent.agent')
def log_agent_activity(sender, instance, created, **kwargs):
    """Log les activités sur les agents"""
    user = get_current_user()
    request = get_current_request()
    
    if user and user.is_authenticated:
        ActivityLog, ActivityLogManager = get_activity_models()
        if created:
            ActivityLog.log_activity(
                user=user,
                action='create',
                entity_type='agent',
                title='Agent créé',
                description=f'Nouvel agent {instance.nom} {instance.prenom} ajouté',
                content_object=instance,
                request=request,
                agent_id=instance.id
            )
        else:
            ActivityLog.log_activity(
                user=user,
                action='update',
                entity_type='agent',
                title='Agent modifié',
                description=f'Informations de {instance.nom} {instance.prenom} mises à jour',
                content_object=instance,
                request=request,
                agent_id=instance.id
            )