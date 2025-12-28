from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver

#Signals pour creer le groupe
@receiver(post_migrate)
def creer_groupes_et_permissions(sender, **kwargs):
    # Liste des groupes à créer
    groupes = {
        "Administrateur": [],
        "Avocat": ["add_dossier", "view_dossier", "change_dossier"],
        "Secrétaire": ["add_client", "view_client", "change_client"],
        "Stagiaire": ["view_dossier", "view_client"],
    }

    for nom_groupe, permissions_codenames in groupes.items():
        groupe, created = Group.objects.get_or_create(name=nom_groupe)
        if created:
            print(f"Groupe créé : {nom_groupe}")

        # Ajouter les permissions existantes (ne pas échouer si elles n'existent pas encore)
        perms = Permission.objects.filter(codename__in=permissions_codenames)
        groupe.permissions.set(perms)
        groupe.save()

        groupe.save()
