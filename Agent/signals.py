# signals.py (Version Corrigée)
"""from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import agent

@receiver(post_save, sender=agent)
def assigner_groupe_agent(sender, instance, created, **kwargs):
  
    if created and instance.poste:
        try:
            groupe = Group.objects.get(name=instance.poste)
            if instance.groupe_attribue != groupe:
                
                instance.groupe_attribue = groupe
                post_save.disconnect(assigner_groupe_agent, sender=agent)
                instance.save()
                post_save.connect(assigner_groupe_agent, sender=agent)
                
        except Group.DoesNotExist:
            print(f"ATTENTION : Le groupe '{instance.poste}' n'existe pas dans Django Group.")"""
        
  