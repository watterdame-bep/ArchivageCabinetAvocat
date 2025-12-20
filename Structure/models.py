from django.db import models
from django.contrib.auth.models import AbstractUser
from Adresse.models import commune

class Forme_juridiques(models.Model):
    nom = models.CharField(max_length=150, null=False)

    class Meta:
        db_table = 'structure_forme_juridiques'
        verbose_name = 'Forme juridique'
        verbose_name_plural = 'Formes juridiques'

    def __str__(self):
        return self.nom
    
class Cabinet(models.Model):
    adresse=models.ForeignKey('Adresse.adresse', on_delete=models.CASCADE, null=True, related_name="cabinet_adresse")
    nom=models.CharField(max_length=200,default=False)
    numero_identification=models.CharField(max_length=50, null=False,blank=True, default=False)
    telephone=models.CharField(max_length=50, null=False,blank=True, default=False)
    telephone_secondaire=models.CharField(max_length=50, null=False,blank=True, default=False)
    forme_juridique=models.ForeignKey(Forme_juridiques,on_delete=models.SET_NULL, null=True,blank=True, default=1)
    telephone=models.CharField(max_length=50, null=False,blank=True, default='')
    num_id_fiscal=models.CharField(max_length=50, null=False,blank=True, default=False)
    date_creations=models.DateField(null=True, blank=True)
    email=models.CharField(max_length=100, null=False,blank=True, default=False)
    reference=models.TextField(null=False,blank=True, default=False)
    site_web=models.CharField(max_length=100, null=False,blank=True, default=False)
    logo=models.ImageField(upload_to='LogoCabinet/',blank=True,null=True)
    nom_fondateur=models.CharField(max_length=100, null=False,blank=True, default=False)

    class Meta:
        # SOLUTION: Forcer le nom de table en minuscules pour compatibilité MySQL
        db_table = 'structure_cabinet'
        verbose_name = 'Cabinet'
        verbose_name_plural = 'Cabinets'

    def __str__(self):
      return f"Le nom du cabinet est:{self.nom}"
    

class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    date_ajouter = models.DateTimeField(auto_now_add=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE,default=1, related_name="cabinet_specialite")

    class Meta:
        db_table = 'structure_specialite'
        verbose_name = 'Spécialité'
        verbose_name_plural = 'Spécialités'

    def __str__(self):
        return self.nom


class Activite(models.Model):
    #dossier = models.ForeignKey('type_dossier', on_delete=models.CASCADE, related_name='activites')
    nom_activite = models.CharField(max_length=200)
    date_activite = models.DateTimeField(auto_now_add=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, related_name="cabinets_Activites")

    class Meta:
        db_table = 'structure_activite'
        verbose_name = 'Activité'
        verbose_name_plural = 'Activités'

    def __str__(self):
        return f"{self.nom_activite} "



class PosteAvocat(models.Model):
    nom_poste = models.CharField(max_length=100, unique=True)
    date_ajouter = models.DateTimeField(auto_now_add=True, null=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE,related_name="cabinets_poste")

    class Meta:
        db_table = 'structure_posteavocat'
        unique_together = ('nom_poste', 'cabinet')
        verbose_name = "Poste d'avocat"
        verbose_name_plural = "Postes d'avocats"

    def __str__(self):
        return self.nom_poste
    

class ServiceCabinet(models.Model):
    nom_service = models.CharField(max_length=100)
    date_ajouter = models.DateTimeField(auto_now_add=True, null=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE,related_name="services_cabinet")

    class Meta:
        db_table = 'structure_servicecabinet'
        unique_together = ('nom_service', 'cabinet')
        verbose_name = "Service cabinet"
        verbose_name_plural = "Services cabinet"

    def __str__(self):
        return self.nom_service


class Juridiction(models.Model):
    nom = models.CharField(max_length=150, null=False)
    lieu=models.ForeignKey(commune,on_delete=models.SET_NULL,null=True, default="Aucune adresse")
    date_creation = models.DateField(auto_now_add=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, default=1, related_name="Juridiction_cabinet")

    class Meta:
        db_table = 'structure_juridiction'
        verbose_name = 'Juridiction'
        verbose_name_plural = 'Juridictions'

    def __str__(self):
        return self.nom


class Banque(models.Model):
    nom_banque = models.CharField(max_length=255)
    numero_compte = models.CharField(max_length=255)
    date_ajouter = models.DateTimeField(auto_now_add=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, default=1, related_name="Banque_cabinet")
    
    class Meta:
        db_table = 'structure_banque'
        unique_together = ('nom_banque', 'cabinet')
        verbose_name = "Banque cabinet"
        verbose_name_plural = "Banques cabinet"

    def __str__(self):
        return self.nom_banque


