from django.db import models
from Adresse.models import adresse, commune
from Structure.models import Cabinet,Activite,Juridiction
from parametre.models import taux
import datetime


# Create your models here.
class client (models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')], default='Homme')
    adresse=models.ForeignKey(adresse,on_delete=models.SET_NULL,null=True,related_name="client_adresse")
    nationalite = models.CharField(max_length=50)
    type_client= models.CharField(max_length=10, choices=[('Physique', 'Physique'), ('Morale', 'Morale')], default='Homme')

    profession = models.CharField(max_length=100, blank=True, null=True)
    representant_legal = models.CharField(max_length=150, blank=True, null=False, default='Aucun')

    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, related_name="clients")
    photo = models.ImageField(upload_to="clients_photos/", blank=True, null=True)
    date_enregistrement = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dossier_client'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'



class SecteurFoncier(models.Model):
    nom = models.CharField(max_length=100 )
    communes = models.ManyToManyField(commune, blank=True, related_name='secteurs')
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE,default=1, related_name="cabinet_secteur")

    class Meta:
        db_table = 'dossier_secteurfoncier'
        verbose_name = 'Secteur Foncier'
        verbose_name_plural = 'Secteurs Fonciers'

    def __str__(self):
        return self.nom

    
#Type de dossier
class type_dossier(models.Model):
    nom_type = models.CharField(max_length=100)
    date_ajouter = models.DateField(auto_now_add=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE,default=1, related_name="cabinet_type_dossier")

    class Meta:
        db_table = 'dossier_type_dossier'
        verbose_name = 'Type de dossier'
        verbose_name_plural = 'Types de dossiers'

    def __str__(self):
        return f""


#Tarif pour le dossier
class TarifHoraire(models.Model):
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, related_name="tarif_cabinet", null=True)
    type_dossier = models.ForeignKey(type_dossier,on_delete=models.CASCADE, related_name='tarifs_horaires_dossier')
    secteur = models.ForeignKey(SecteurFoncier,on_delete=models.CASCADE,related_name='tarifs_horaires_secteurs')
    montant_fc = models.DecimalField( max_digits=10,decimal_places=2,verbose_name="Montant par heure")
    description = models.TextField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    montant_dollars = models.DecimalField( max_digits=10, decimal_places=2,  blank=True,  null=True,verbose_name="Montant Forfaitaire de Base")
    taux_jour=models.DecimalField( max_digits=10,decimal_places=2, default=0.00)
   
    class Meta:
        db_table = 'dossier_tarifhoraire'
        verbose_name = "Tarif Horaire"
        verbose_name_plural = "Tarifs Horaires"
        unique_together = ('type_dossier', 'secteur')  # un tarif par type de dossier + secteur

    @property
    def taux_actuel(self):
        """
        Récupère le dernier taux pour ce cabinet depuis le modèle taux.
        """
        t = taux.objects.filter(cabinet=self.cabinet).order_by('-date_ajouter').first()
        return t.cout if t else self.taux_jour
    
    
    def save(self, *args, **kwargs):
        # Calcul automatique du montant en FC si montant_dollars et taux_jour sont renseignés
        if self.montant_dollars is not None and self.taux_jour is not None:
            self.montant_fc = self.montant_dollars * self.taux_jour
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_dossier.nom_type} - {self.secteur.nom}"


class TarifActivite(models.Model):
    tarif = models.ForeignKey(TarifHoraire, on_delete=models.CASCADE,related_name='activites_tarif')
    activite = models.ForeignKey(Activite,on_delete=models.CASCADE,related_name='tarifs_activites')
    prix_dollars = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Prix de l’activité (Fc)")
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE,default=1, related_name="cabinet_Tarifactivite")
    class Meta:
        db_table = 'dossier_tarifactivite'
        unique_together = ('tarif', 'activite')
        verbose_name = "Tarif par Activité"
        verbose_name_plural = "Tarifs par Activité"

    def save(self, *args, **kwargs):
        if self.prix_dollars is not None and self.tarif.taux_jour:
            self.prix_fc = self.prix_dollars * self.tarif.taux_jour
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.activite.nom_activite} ({self.prix_fc} Fc)"


class ReductionTarifForfaitaire(models.Model):
    dossier = models.ForeignKey('Dossier.Dossier', on_delete=models.CASCADE, related_name='reductions_forfaitaires')
    activite = models.ForeignKey(TarifActivite, on_delete=models.CASCADE)
    prix_reduit_dollars = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_reduit_fc = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dossier_reductiontarifforfaitaire'

    def __str__(self):
        return f"{self.dossier.numero_reference_dossier} - {self.activite.nom_activite}"


#Dossier
class dossier (models.Model):
    # État actuel du dossier (pour la gestion)
    STATUT_CHOICES = [
        ('Ouvert', 'Ouvert'),
        ('En Cours', 'En Cours'),
        ('Suspendu', 'Suspendu'),
        ('Clôturé', 'Clôturé'),
    ]
    MODE_HONORAIRE_CHOICES = [
        ('Forfait', 'Forfaitaire'),
        ('Normal', 'Normalisé'),
    ]
    client = models.ForeignKey('Client',on_delete=models.PROTECT, related_name="dossiers_client",verbose_name="Client associé")
    secteur_foncier = models.ForeignKey(SecteurFoncier, on_delete=models.SET_NULL, null=True, related_name="dossiers_secteur", verbose_name="Secteur Foncier")
    numero_reference_dossier = models.CharField(max_length=50, unique=True,verbose_name="N° de Dossier",help_text="Référence unique attribuée par le cabinet (ex: CABINET/ANNEE/CLIENT_ID)")  
    titre = models.CharField(max_length=200, verbose_name="Objet/Titre du Dossier")   
    type_affaire = models.ForeignKey(type_dossier, on_delete=models.CASCADE, related_name="dossier_type")    
    mode_honoraire = models.CharField(max_length=10,choices=MODE_HONORAIRE_CHOICES, null=True, default="Normal")
    forfait_defini = models.BooleanField(default=False) 
    mode_defini = models.BooleanField(default=False) 
    statut_dossier = models.CharField( max_length=20, choices=STATUT_CHOICES,default='Ouvert',verbose_name="Statut du Dossier")  
    partie_adverse_nom = models.CharField( max_length=200, blank=True, null=True, )
    juridiction = models.ForeignKey(Juridiction,on_delete=models.SET_NULL, related_name="dossiers_jridiction", null=True)   
    date_ouverture =models.DateTimeField(auto_now_add=True,blank=True,null=True)  
    date_cloture = models.DateTimeField(auto_now_add=True,blank=True,null=True)    
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, related_name="dossiers")  
    score=models.CharField(max_length=100, blank=True, null=True, verbose_name="Gagner ou perdu")
    # Honoraires ou Modalités de Paiement
    tarif_reference = models.ForeignKey(TarifHoraire ,on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Référence Tarifaire")
    #Montant copier et enregistrer
    montant_dollars_enreg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    montant_fc_enreg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    taux_enreg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    reference = models.CharField(max_length=50, blank=True, null=True, unique=True)
    observation=models.TextField(verbose_name="Dernier mot de l'avocat", default='')

    
    class Meta:
        db_table = 'dossier_dossier'
        verbose_name = "Dossier Client"
        verbose_name_plural = "Dossiers Clients"


    @staticmethod
    def generer_numero_dossier(cabinet, client_id):
       annee = datetime.date.today().year
       mois = datetime.date.today().month
       jour = datetime.date.today().day
       # On peut compter le nombre de dossiers déjà créés pour ce cabinet cette année
       count = dossier.objects.filter(cabinet=cabinet, date_ouverture__year=annee).count() + 1
       return f"{cabinet.nom}-{annee}{mois}{jour}{client_id}-{count:03d}"
    
    def __str__(self):
        return f"[{self.numero_reference_dossier}] {self.titre} - Client: {self.client.nom}"
    
    def get_montant_total_du_non_facture(self):
     montant_du = 0
     for activite in self.activites_temps.filter(facturee=False):
        montant_du += activite.calculer_cout_activite()
     return montant_du
    


class DeclarationDossier(models.Model):
    dossier = models.ForeignKey(dossier, on_delete=models.CASCADE,related_name="declarations",verbose_name="Dossier associé")
    contenu = models.TextField(verbose_name="Contenu de la Déclaration")
    date_ajout = models.DateTimeField(auto_now_add=True)
    ecrit_par = models.ForeignKey('Agent.agent',on_delete=models.SET_NULL,null=True,blank=True, verbose_name="Agent ayant ajouté la déclaration")
    auteur = models.CharField(max_length=100, null=False, default='')

    class Meta:
        db_table = 'dossier_declarationdossier'
        ordering = ['-date_ajout']  # Les plus récentes en premier

    def __str__(self):
        return f"Déclaration du {self.date_ajout.strftime('%d/%m/%Y')} - Dossier {self.dossier.id}"


#relier chaque avocat à un dossier
class AvocatDossier(models.Model):
    ROLE_CHOICES = [
        ('Principal', 'Avocat Principal'),
        ('Support', 'Avocat de Support'),
        ('Partenaire', 'Avocat Partenaire Externe'),
    ]
    dossier = models.ForeignKey(dossier, on_delete=models.CASCADE)
    avocat = models.ForeignKey('Agent.agent', on_delete=models.SET_NULL, null=True)  
    role = models.CharField( max_length=20,choices=ROLE_CHOICES,default='Support',verbose_name="Rôle dans le dossier")
    date_assignation = models.DateField(auto_now_add=True, verbose_name="Date d'assignation")
    
    # Pour s'assurer qu'un avocat n'est pas deux fois dans le même dossier
    class Meta:
        db_table = 'dossier_avocatdossier'
        unique_together = (('dossier', 'avocat'),) 
        verbose_name = "Assignation Avocat-Dossier"

    def __str__(self):
        return f"{self.avocat.nom} - {self.role} sur Dossier {self.dossier.numero_reference_dossier}"




#Pour enregistrer les activités durant le dossier enfin d'etre facturées
class ActiviteHeure(models.Model):
    dossier = models.ForeignKey(dossier, on_delete=models.CASCADE, related_name="activites_temps",verbose_name="Dossier concerné")
    # L'avocat qui a effectué le travail (votre modèle agent/utilisateur)
    avocat = models.ForeignKey('Agent.agent', on_delete=models.SET_NULL, null=True,verbose_name="Avocat/Agent")
    date_activite = models.DateField(verbose_name="Date de l'activité") 
    # Durée en heures et minutes (DecimalField ou TimeField, DecimalField est plus facile pour les calculs)
    duree_heures = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Durée (en heures, ex: 1.50)")
    description = models.TextField(verbose_name="Description de l'activité (pour la facture)")   
    facturee = models.BooleanField(default=False) # Pour marquer si l'heure a déjà été incluse dans une facture
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE,default=1, related_name="cabinet_activite")
    
    class Meta:
        db_table = 'dossier_activiteheure'
    
    def calculer_cout_activite(self):
        try:
            # 1. Récupérer l'objet TarifHoraire correspondant au Dossier
            # On utilise le type_affaire et le secteur_foncier du dossier
            tarif = TarifHoraire.objects.get(
                type_dossier=self.dossier.type_affaire,
                secteur=self.dossier.secteur_foncier
            )           
            # 2. Récupérer le taux horaire
            taux_horaire = tarif.montant_horaire
            
        except TarifHoraire.DoesNotExist:
            taux_horaire = 0.00
            
        # 3. Calcul du coût de l'activité
        cout_total = self.duree_heures * taux_horaire
        return cout_total
    
    def __str__(self):
        return f"{self.dossier.numero_reference_dossier} - {self.description[:50]}"



#il gere les pieces ou documents concernant les dossier
class PieceDossier(models.Model):
    dossier = models.ForeignKey( dossier, on_delete=models.CASCADE, related_name='pieces_dossier', verbose_name="Dossier concerné")
    titre = models.CharField( max_length=150, help_text="Exemple : Contrat, Jugement, Assignation, Preuve, etc.")
    fichier = models.FileField(upload_to='pieces_dossier/',verbose_name="Fichier à téléverser")
    date_ajout=models.DateField(auto_now_add=True)
    format_fichier=models.CharField( max_length=150, default='document')
    ajoute_par = models.ForeignKey('Agent.agent',on_delete=models.SET_NULL, null=True,blank=True, related_name="pieces_ajoutees", verbose_name="Ajouté par")
  
    class Meta:
        db_table = 'dossier_piecedossier'
        verbose_name = "Pièce du dossier"
        verbose_name_plural = "Pièces du dossier"
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.titre} ({self.dossier.numero_reference_dossier})"
    

class TypePiece(models.Model):
    nom_type=models.CharField( max_length=150, null=False)
    date_ajout=models.DateField(auto_now_add=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'dossier_typepiece'

    def __str__(self):
        return f"{self.nom_type}"
   
  