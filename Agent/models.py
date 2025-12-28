from django.db import models
from Adresse.models import adresse
from Structure.models import Cabinet, Specialite
from django.contrib.auth.models import Group
from Dossier.models import TypePiece

# Import du modèle ActivityLog sera fait après pour éviter l'import circulaire
# from .models_activity import ActivityLog, ActivityLogManager

class agent(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    numero_identification = models.CharField(max_length=50, unique=True, help_text="Numéro d’identification de l’avocat ou de l’agent")
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')], default='Homme')
    adresse=models.ForeignKey(adresse,on_delete=models.SET_NULL,null=True,related_name="agent_adresse")
    
    company = models.ForeignKey(Cabinet, on_delete=models.CASCADE,null=True, related_name="cabinet_agent")
    poste = models.CharField(
               max_length=100,
               blank=True,
               null=True,
               choices=[
                     ('Administrateur', 'Administrateur'),
                     ('Avocat', 'Avocat'),
                     ('Secretaire', 'Secrétaire'),
                     #('Juriste', 'Juriste')
                     ]
            )

    specialite = models.ForeignKey(Specialite,on_delete=models.SET_NULL,null=True,blank=True,related_name="agents"   ) 
    #budget_prevu = models.CharField(max_length=50, blank=True, null=True)
    annee_experience=models.CharField(max_length=5, blank=True, default=0)
    
    # À propos
    a_propos = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    photo=models.ImageField(upload_to='PhotoAgent/',blank=True,null=False)

    # Nouveau champ pour mémoriser le groupe lié au poste
    groupe_attribue = models.ForeignKey(Group,on_delete=models.SET_NULL,null=True,blank=True,related_name="groupe_agents")

    class Meta:
        db_table = 'agent_agent'
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class PieceJustificative(models.Model):
    agent = models.ForeignKey( agent,on_delete=models.SET_NULL,null=True, blank=True, related_name='pieces_agent')
    client = models.ForeignKey('Dossier.client',on_delete=models.SET_NULL,null=True, blank=True,related_name='pieces_client')
    type_piece= models.ForeignKey( TypePiece,on_delete=models.SET_NULL,null=True, blank=True, related_name='Type_pieces_Justificative')
    numero_piece = models.CharField(max_length=50, blank=True, null=True)
    fichier = models.FileField(upload_to='pieces_justificatives/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agent_piecejustificative'
        verbose_name = 'Pièce justificative'
        verbose_name_plural = 'Pièces justificatives'

    def __str__(self):
        cible = self.agent if self.agent else self.client
        return f"{self.type_piece} - {cible}"


