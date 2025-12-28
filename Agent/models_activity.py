from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.conf import settings


class ActivityLog(models.Model):
    """
    Modèle pour tracker toutes les activités des agents dans le système
    """
    
    ACTION_CHOICES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
        ('view', 'Consultation'),
        ('payment', 'Paiement'),
        ('assign', 'Attribution'),
        ('close', 'Clôture'),
        ('reopen', 'Réouverture'),
    ]
    
    ENTITY_CHOICES = [
        ('dossier', 'Dossier'),
        ('declaration', 'Déclaration'),
        ('document', 'Document'),
        ('paiement', 'Paiement'),
        ('client', 'Client'),
        ('agent', 'Agent'),
        ('piece_justificative', 'Pièce justificative'),
    ]
    
    # Qui a fait l'action
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    
    # Quand l'action a été faite
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Type d'action
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    
    # Type d'entité concernée
    entity_type = models.CharField(max_length=30, choices=ENTITY_CHOICES)
    
    # Référence générique vers l'objet concerné
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Détails de l'activité
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Métadonnées
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # Données supplémentaires (JSON)
    extra_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['entity_type', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.title}"
    
    @property
    def icon(self):
        """Retourne l'icône appropriée selon le type d'action"""
        icon_map = {
            'create': 'mdi-plus-circle',
            'update': 'mdi-pencil-circle',
            'delete': 'mdi-delete-circle',
            'view': 'mdi-eye-circle',
            'payment': 'mdi-cash',
            'assign': 'mdi-account-arrow-right',
            'close': 'mdi-folder-check',
            'reopen': 'mdi-folder-open',
        }
        return icon_map.get(self.action, 'mdi-information-circle')
    
    @property
    def color(self):
        """Retourne la couleur appropriée selon le type d'action"""
        color_map = {
            'create': 'success',
            'update': 'primary',
            'delete': 'danger',
            'view': 'info',
            'payment': 'success',
            'assign': 'warning',
            'close': 'secondary',
            'reopen': 'info',
        }
        return color_map.get(self.action, 'secondary')
    
    @classmethod
    def log_activity(cls, user, action, entity_type, title, description, 
                     content_object=None, request=None, **extra_data):
        """
        Méthode utilitaire pour créer un log d'activité
        """
        activity = cls.objects.create(
            user=user,
            action=action,
            entity_type=entity_type,
            title=title,
            description=description,
            content_object=content_object,
            ip_address=cls._get_client_ip(request) if request else None,
            user_agent=request.META.get('HTTP_USER_AGENT', '') if request else '',
            extra_data=extra_data
        )
        return activity
    
    @staticmethod
    def _get_client_ip(request):
        """Récupère l'IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ActivityLogManager:
    """
    Manager pour simplifier la création de logs d'activités
    """
    
    @staticmethod
    def log_dossier_created(user, dossier, request=None):
        return ActivityLog.log_activity(
            user=user,
            action='create',
            entity_type='dossier',
            title='Dossier créé',
            description=f'Nouveau dossier {dossier.numero_reference_dossier} pour {dossier.client.nom} {dossier.client.prenom}',
            content_object=dossier,
            request=request,
            dossier_id=dossier.id,
            client_id=dossier.client.id
        )
    
    @staticmethod
    def log_dossier_updated(user, dossier, request=None, changes=None):
        return ActivityLog.log_activity(
            user=user,
            action='update',
            entity_type='dossier',
            title='Dossier modifié',
            description=f'Mise à jour du dossier {dossier.numero_reference_dossier}',
            content_object=dossier,
            request=request,
            dossier_id=dossier.id,
            changes=changes or {}
        )
    
    @staticmethod
    def log_document_added(user, document, dossier, request=None):
        return ActivityLog.log_activity(
            user=user,
            action='create',
            entity_type='document',
            title='Document ajouté',
            description=f'{document.titre} ajouté au dossier {dossier.numero_reference_dossier}',
            content_object=document,
            request=request,
            dossier_id=dossier.id,
            document_title=document.titre
        )
    
    @staticmethod
    def log_document_deleted(user, document_title, dossier, request=None):
        return ActivityLog.log_activity(
            user=user,
            action='delete',
            entity_type='document',
            title='Document supprimé',
            description=f'{document_title} supprimé du dossier {dossier.numero_reference_dossier}',
            request=request,
            dossier_id=dossier.id,
            document_title=document_title
        )
    
    @staticmethod
    def log_declaration_added(user, declaration, request=None):
        return ActivityLog.log_activity(
            user=user,
            action='create',
            entity_type='declaration',
            title='Déclaration ajoutée',
            description=f'Nouvelle déclaration pour le dossier {declaration.dossier.numero_reference_dossier}',
            content_object=declaration,
            request=request,
            dossier_id=declaration.dossier.id
        )
    
    @staticmethod
    def log_declaration_updated(user, declaration, request=None):
        return ActivityLog.log_activity(
            user=user,
            action='update',
            entity_type='declaration',
            title='Déclaration modifiée',
            description=f'Mise à jour de la déclaration du dossier {declaration.dossier.numero_reference_dossier}',
            content_object=declaration,
            request=request,
            dossier_id=declaration.dossier.id
        )
    
    @staticmethod
    def log_payment_recorded(user, paiement, request=None):
        return ActivityLog.log_activity(
            user=user,
            action='payment',
            entity_type='paiement',
            title='Paiement enregistré',
            description=f'{paiement.montant_payer_dollars} USD - {paiement.dossier.numero_reference_dossier if paiement.dossier else "Caisse"}',
            content_object=paiement,
            request=request,
            dossier_id=paiement.dossier.id if paiement.dossier else None,
            amount_usd=float(paiement.montant_payer_dollars),
            amount_fc=float(paiement.montant_payer_fc) if paiement.montant_payer_fc else 0
        )