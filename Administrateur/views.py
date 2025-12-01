from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from Structure.models import Specialite,Activite
from Agent.models import agent
from Authentification.models import CompteUtilisateur
from Dossier.models import client,dossier,AvocatDossier,SecteurFoncier,type_dossier,TarifHoraire
from Adresse.models import commune
from paiement.models import Paiement 
from datetime import date
from django.db.models import Sum
from Dossier.models import TarifHoraire
# Create your views here.

@login_required(login_url='Connexion') 
def dashboard_admin(request):
    agents_recents = agent.objects.filter(company=request.user.cabinet).order_by('-date_creation')[:5]
    dossiers=dossier.objects.filter(cabinet=request.user.cabinet)
    dossiers_agent=AvocatDossier.objects.filter(avocat=request.user.agent)
    tarif_horaire = TarifHoraire.objects.filter(cabinet=request.user.cabinet).first()
    #taux=tarif_horaire.taux_jour
    today = date.today()
    # Total des bouteilles jetées ce mois
    gain_de_ce_mois = Paiement.objects.filter(
        cabinet=request.user.cabinet,
        date_paiement__year=today.year,
        date_paiement__month=today.month,
        devise='USD'
    ).aggregate(total=Sum('montant'))['total'] or 0

    gain_de_ce_mois_fc = Paiement.objects.filter(
        cabinet=request.user.cabinet,
        date_paiement__year=today.year,
        date_paiement__month=today.month,
        devise='FC'
    ).aggregate(total=Sum('montant'))['total'] or 0
    #gain_de_ce_mois_fc=gain_de_ce_mois*taux

    lesdossiers=dossier.objects.filter(cabinet=request.user.cabinet).count()

    dossiers_regler=dossier.objects.filter(cabinet=request.user.cabinet,statut_dossier="regler").count()
    dossiers_gagner = dossier.objects.filter(cabinet=request.user.cabinet,score="gagner").count()
    dossiers_perdu = dossier.objects.filter(cabinet=request.user.cabinet,score="perdu").count()

    # Calcul des pourcentages (éviter division par zéro)
    pourcentage_gagner = (dossiers_gagner / lesdossiers * 100) if lesdossiers > 0 else 0
    pourcentage_perdu = (dossiers_perdu / lesdossiers * 100) if lesdossiers > 0 else 0
    pourcentage_regler = (dossiers_regler / lesdossiers * 100) if lesdossiers > 0 else 0


    for d in dossiers:
        principal = AvocatDossier.objects.filter(dossier=d, role='Principal').first()
        d.avocat_principal = principal.avocat if principal else None
    
    for da in dossiers_agent:
        principal = AvocatDossier.objects.filter(
            dossier=da.dossier,
            role='Principal'
        ).first()
        da.avocat_principal = principal.avocat if principal else None

    
    
    context = {
        'agents_recents': agents_recents,
        'dossiers':dossiers,
        'dossiers_regler':dossiers_regler,
        'dossiers_gagner': dossiers_gagner,
        'dossiers_perdu': dossiers_perdu,
        'pourcentage_gagner': pourcentage_gagner,
        'pourcentage_perdu': pourcentage_perdu,
        'pourcentage_regler': pourcentage_regler,
        'dossiers_agent':dossiers_agent,
        'gain_de_ce_mois':gain_de_ce_mois,
        'gain_de_ce_mois_fc':gain_de_ce_mois_fc
        
    }
    return render(request, "admin_template/index-1.html",context)

@login_required(login_url='Connexion') 
def agent_interface(request):
    agents = agent.objects.filter(company=request.user.cabinet)
    specialites = Specialite.objects.all()  

    return render(request, 'admin_template/attorney_list.html', {
        'agents': agents,
        'specialites': specialites,  
    })


@login_required(login_url='Connexion') 
def dashboard_Avocat(request):
    
    return render(request, "avocat_template/index.html")


@login_required(login_url='Connexion') 
def Interface_Client(request):
    clients = clients = client.objects.filter(cabinet=request.user.cabinet)
    return render(request, 'admin_template/cases.html', {'clients':clients})




def parametrage_view(request):
    secteurs = SecteurFoncier.objects.all()
    types_affaires = type_dossier.objects.all()
    communes = commune.objects.all().order_by('-date_ouverture')
    #activites = Activite.objects.all()

    context = {
        'secteurs': secteurs,
        'types_affaires': types_affaires,
        'communes': communes,
        #'activites': activites,
    }
    return render(request, 'admin_template/index-1.html', context)
