from django.db import models
from Dossier.models import dossier, client
from Agent.models import agent 
from Structure.models import Cabinet,Banque

class Paiement(models.Model):
    STATUT_CHOICES = [
        ("Reussi", "Réussi"),
        ("En_Attente", "En attente"),
        ("Echoue", "Échoué"),
    ]
    
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE,related_name='paiements')
    dossier = models.ForeignKey(dossier, on_delete=models.CASCADE, related_name='paiements', null=True)
    client = models.ForeignKey(client, on_delete=models.CASCADE, related_name='paiements_client', null=True)
    agent=models.ForeignKey(agent, on_delete=models.SET_NULL,default=1, null=True, related_name='paiements_agent')
    personne_qui_paie = models.CharField(max_length=200, blank=True, null=True)
    montant_payer_dollars= models.DecimalField(max_digits=15, decimal_places=2)
    montant_payer_fc= models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    montant_reste_dollars= models.DecimalField(max_digits=15, decimal_places=2,default=0.00)
    montant_reste_fc= models.DecimalField(max_digits=15, decimal_places=2,default=0.00)
    devise = models.CharField(max_length=10, choices=[('USD', 'USD'), ('FC', 'FC')])
    banque=models.ForeignKey(Banque, on_delete=models.SET_NULL, related_name='banque_paye', null=True)
    date_paiement = models.DateTimeField(auto_now_add=True)
    type_paiement = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    taux = models.TextField(blank=True, null=False)
    justificatif = models.FileField(upload_to='paiements/', blank=True, null=True)
    motif=models.CharField(max_length=100,null=False, default="Paiement du client")
    type_operation = models.CharField(max_length=20,choices=[("ENTREE", "Entrée"), ("SORTIE", "Sortie")],default="ENTREE")
    

    def __str__(self):
        return f"Paiement {self.id} | {self.client.nom} | {self.montant} {self.devise}"
