from django.db import models
from Structure.models import Cabinet 
# Create your models here.
class taux(models.Model):
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    cout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_ajouter = models.DateTimeField(auto_now=True)