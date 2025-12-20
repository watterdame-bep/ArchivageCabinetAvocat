from django.db import models
from django.contrib.auth.models import AbstractUser
from Structure.models import Cabinet
from Agent.models import agent

class CompteUtilisateur(AbstractUser):
    cabinet=models.ForeignKey(Cabinet, on_delete=models.SET_NULL, null=True, related_name="Cabine_Utilisateur")
    agent=models.ForeignKey(agent, on_delete=models.SET_NULL, null=True, related_name="Agent_Utilisateur")
    photo=models.ImageField(upload_to='PhotoProfilUser/',blank=True,null=False)
    statut=models.CharField(max_length=50,default='actif')
    type_compte=models.CharField(max_length=50,default='user')
   
    USERNAME_FIELD='username'
    
    class Meta:
        # SOLUTION: Forcer le nom de table en minuscules pour compatibilité avec import MySQL
        db_table = 'authentification_compteutilisateur'
        verbose_name = 'Compte Utilisateur'
        verbose_name_plural = 'Comptes Utilisateurs'
  
    def __str__(self):
      return self.username
    
    #pour hacher le mot de passe
    def save(self, *args, **kwargs):
    # Si le mot de passe n'est pas encore haché (en clair), on le hache
      if self.password and not self.password.startswith('pbkdf2_'):
        self.set_password(self.password)
      super().save(*args, **kwargs)

