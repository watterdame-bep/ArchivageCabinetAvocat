from django.db.models.signals import post_save
from django.dispatch import receiver
from Dossier.models import taux, TarifHoraire

@receiver(post_save, sender=taux)
def update_tarif_with_new_taux(sender, instance, created, **kwargs):
    if created:
        # Nouveau taux ajouté → mettre à jour tous les anciens tarifs
        nouveau_taux = float(instance.cout)

        # Mise à jour de tous les objets tarif
        TarifHoraire.objects.filter(cabinet=instance.cabinet).update(taux_jour=nouveau_taux)
        
