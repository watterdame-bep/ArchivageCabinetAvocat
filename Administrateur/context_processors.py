# admin_template/context_processors.py

from Dossier.models import SecteurFoncier, commune, Activite, type_dossier, TarifHoraire,TypePiece
from Adresse.models import  Ville,adresse
from Structure.models import Specialite, PosteAvocat,Juridiction,Cabinet, Forme_juridiques,ServiceCabinet,Banque
from parametre.models import taux

def modales_data(request):
    """
    Variables globales pour les modales.
    Disponibles dans tous les templates.
    Filtre selon le cabinet de l'utilisateur connecté.
    """
    forme_juridiques =None
    cabinet = None  # objet unique
    adr = None    # objet adresse
    
    if request.user.is_authenticated and hasattr(request.user, 'cabinet') and request.user.cabinet:
        user_cabinet = request.user.cabinet

        secteurs = SecteurFoncier.objects.filter(cabinet=user_cabinet)
        types_affaires = type_dossier.objects.filter(cabinet=user_cabinet)
        communes = commune.objects.filter(cabinet=user_cabinet)
        types_dossier = type_dossier.objects.filter(cabinet=user_cabinet)
        activites = Activite.objects.filter(cabinet=user_cabinet)
        types_dossiers = type_dossier.objects.filter(cabinet=user_cabinet)
        tarifs = TarifHoraire.objects.select_related('secteur', 'type_dossier').filter(cabinet=user_cabinet)
        specs = Specialite.objects.filter(cabinet=user_cabinet)
        postes = PosteAvocat.objects.filter(cabinet=user_cabinet)
        villes = Ville.objects.filter(cabinet=user_cabinet)
        type_pieces = TypePiece.objects.filter()
        juridictions=Juridiction.objects.filter(cabinet=user_cabinet)
        dernier_taux = taux.objects.filter(cabinet=user_cabinet).order_by('-date_ajouter').first()
        liste_taux = taux.objects.filter(cabinet=request.user.cabinet).order_by('-id')
        cabinet = user_cabinet  # objet unique
        adr = cabinet.adresse    # objet adresse
        services=ServiceCabinet.objects.filter(cabinet=user_cabinet)
        forme_juridiques =Forme_juridiques.objects.all().order_by('id')
        banques=Banque.objects.filter(cabinet=request.user.cabinet).order_by('date_ajouter')
       
        


        
    else:
        # Aucun utilisateur connecté : on retourne des QuerySets vides
        secteurs = SecteurFoncier.objects.none()
        types_affaires = type_dossier.objects.none()
        communes = commune.objects.none()
        types_dossier = type_dossier.objects.none()
        activites = Activite.objects.none()
        types_dossiers = type_dossier.objects.none()
        tarifs = TarifHoraire.objects.none()
        specs = Specialite.objects.none()
        postes = PosteAvocat.objects.none()
        villes = Ville.objects.none()
        type_pieces = TypePiece.objects.none()
        juridictions=Juridiction.objects.none()
        dernier_taux=taux.objects.none()
        liste_taux=taux.objects.none()
        services=ServiceCabinet.objects.none()
        banques=Banque.objects.none()
        

    return {
        'secteurs': secteurs,
        'types_affaires': types_affaires,
        'communes': communes,
        'types_dossier': types_dossier,
        'activites': activites,
        'types_dossiers': types_dossiers,
        'tarifs': tarifs,
        'specialites': specs,
        'postes': postes,
        'villes': villes,
        'type_pieces':type_pieces,
        'juridictions':juridictions,
        'dernier_taux':dernier_taux,
        'liste_taux':liste_taux,
        'forme_juridiques': forme_juridiques,
        'cabinet': cabinet,
        'adr': adr,
        'services':services,
        'banques':banques,
       
    }


