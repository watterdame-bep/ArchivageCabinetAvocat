from django.db import models

# Create your models here.
class adresse(models.Model):
    numero=models.CharField(max_length=100, blank=True,null=False)
    avenue=models.CharField(max_length=100, blank=True,null=False)
    quartier=models.CharField(max_length=100, blank=True,null=False)
    commune=models.CharField(max_length=100, blank=True,null=False)
    ville=models.CharField(max_length=100, blank=True,null=False)

    class Meta:
        db_table = 'adresse_adresse'
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'

    def __str__(self):
      return f"La commune:{self.commune}"

class commune(models.Model):
    nom=models.CharField(max_length=100, blank=True,null=False)
    date_ouverture =models.DateTimeField(auto_now_add=True,blank=True,null=True)  
    cabinet = models.ForeignKey('Structure.Cabinet', on_delete=models.CASCADE, related_name="communes")
    
    class Meta:
        db_table = 'adresse_commune'
        verbose_name = 'Commune'
        verbose_name_plural = 'Communes'
    
    def __str__(self):
      return f"La commune:{self.nom}"
    


class Ville(models.Model):
    nom_ville = models.CharField(max_length=100)
    province=models.CharField(max_length=100, blank=True,null=False)
    date_enregistre =models.DateTimeField(auto_now_add=True,blank=True,null=True)  
    cabinet = models.ForeignKey('Structure.Cabinet', on_delete=models.CASCADE)

    class Meta:
        db_table = 'adresse_ville'
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'

    def __str__(self):
        return f"{self.nom_ville} ({self.province})"
