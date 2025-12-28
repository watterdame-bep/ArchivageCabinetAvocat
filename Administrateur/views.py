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
    dossiers = dossier.objects.filter(cabinet=request.user.cabinet)
    dossiers_non_clotures = dossiers.exclude(statut_dossier='Clôturé')

    today = date.today()

    # ---------- STATISTIQUES DE LA CAISSE ----------

    # Solde actuel
    total_entrees_usd = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='ENTREE'
    ).aggregate(total=Sum('montant_payer_dollars'))['total'] or 0
    total_sorties_usd = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='SORTIE'
    ).aggregate(total=Sum('montant_payer_dollars'))['total'] or 0
    solde_actuel_usd = total_entrees_usd - total_sorties_usd

    total_entrees_fc = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='ENTREE'
    ).aggregate(total=Sum('montant_payer_fc'))['total'] or 0
    total_sorties_fc = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='SORTIE'
    ).aggregate(total=Sum('montant_payer_fc'))['total'] or 0
    solde_actuel_fc = total_entrees_fc - total_sorties_fc

    # Solde du jour
    total_entrees_jour_usd = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='ENTREE',
        date_paiement__date=today
    ).aggregate(total=Sum('montant_payer_dollars'))['total'] or 0

    total_sorties_jour_usd = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='SORTIE',
        date_paiement__date=today
    ).aggregate(total=Sum('montant_payer_dollars'))['total'] or 0

    total_entrees_jour_fc = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='ENTREE',
        date_paiement__date=today
    ).aggregate(total=Sum('montant_payer_fc'))['total'] or 0

    total_sorties_jour_fc = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='SORTIE',
        date_paiement__date=today
    ).aggregate(total=Sum('montant_payer_fc'))['total'] or 0

    # Solde du mois
    total_entrees_mois_usd = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='ENTREE',
        date_paiement__year=today.year, date_paiement__month=today.month
    ).aggregate(total=Sum('montant_payer_dollars'))['total'] or 0

    total_sorties_mois_usd = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='SORTIE',
        date_paiement__year=today.year, date_paiement__month=today.month
    ).aggregate(total=Sum('montant_payer_dollars'))['total'] or 0

    total_entrees_mois_fc = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='ENTREE',
        date_paiement__year=today.year, date_paiement__month=today.month
    ).aggregate(total=Sum('montant_payer_fc'))['total'] or 0

    total_sorties_mois_fc = Paiement.objects.filter(
        cabinet=request.user.cabinet, type_operation='SORTIE',
        date_paiement__year=today.year, date_paiement__month=today.month
    ).aggregate(total=Sum('montant_payer_fc'))['total'] or 0

    solde_mois_usd = total_entrees_mois_usd - total_sorties_mois_usd
    solde_mois_fc = total_entrees_mois_fc - total_sorties_mois_fc

    # ---------- AUTRES STATISTIQUES EXISTANTES ----------
    lesdossiers = dossiers.count()
    dossiers_encours = dossier.objects.filter(
    cabinet=request.user.cabinet).exclude(statut_dossier='Clôturé')
    dossiers_regler = dossiers.filter(statut_dossier="Cloturé").count()
    dossiers_gagner = dossiers.filter(score="gagne").count()
    dossiers_perdu = dossiers.filter(score="perdu").count()

    pourcentage_gagner = (dossiers_gagner / lesdossiers * 100) if lesdossiers > 0 else 0
    pourcentage_perdu = (dossiers_perdu / lesdossiers * 100) if lesdossiers > 0 else 0
    pourcentage_regler = (dossiers_regler / lesdossiers * 100) if lesdossiers > 0 else 0

    #-----------------------------Stats pour l'agent------------------------------------
    nb_total_dossiers_agent = AvocatDossier.objects.filter(avocat=request.user.agent).count()
    nb_dossiers_clos_agent = AvocatDossier.objects.filter(avocat=request.user.agent, dossier__statut_dossier='Clôturé').count()
    dossiers_agent = AvocatDossier.objects.filter(avocat=request.user.agent,dossier__statut_dossier='Ouvert').order_by('-dossier__date_ouverture')[:4]
    nb_dossiers_agent_gagner = AvocatDossier.objects.filter(avocat=request.user.agent, dossier__statut_dossier='gagne').count()
    nb_dossiers_agent_perdu = AvocatDossier.objects.filter(avocat=request.user.agent, dossier__statut_dossier='perdu').count()
    
    pourcentage_agent_gagner = (nb_dossiers_agent_gagner / nb_total_dossiers_agent * 100) if nb_total_dossiers_agent > 0 else 0
    pourcentage_agent_perdu = (nb_dossiers_agent_perdu / nb_total_dossiers_agent * 100) if nb_total_dossiers_agent > 0 else 0
    pourcentage_agent_regler = (dossiers_regler / nb_total_dossiers_agent * 100) if nb_total_dossiers_agent > 0 else 0



    # Ajouter l'attribut avocat principal
    for d in dossiers:
        principal = AvocatDossier.objects.filter(dossier=d, role='Principal').first()
        d.avocat_principal = principal.avocat if principal else None

    for da in dossiers_agent:
        principal = AvocatDossier.objects.filter(dossier=da.dossier, role='Principal').first()
        da.avocat_principal = principal.avocat if principal else None


     # ------------------ STATISTIQUE REVENUS MENSUELS ------------------
    current_year = date.today().year
    revenus_mensuels = []

    for month in range(1, 13):
        total_entrees = Paiement.objects.filter(
            cabinet=request.user.cabinet,
            type_operation='ENTREE',
            date_paiement__year=current_year,
            date_paiement__month=month
        ).aggregate(total=Sum('montant_payer_dollars'))['total'] or 0

        total_sorties = Paiement.objects.filter(
            cabinet=request.user.cabinet,
            type_operation='SORTIE',
            date_paiement__year=current_year,
            date_paiement__month=month
        ).aggregate(total=Sum('montant_payer_dollars'))['total'] or 0

        # Revenu net du mois
        revenus_mensuels.append(total_entrees - total_sorties)

    
    context = {
        #cabinet
        'agents_recents': agents_recents,
        'dossiers': dossiers,
        'dossiers_regler': dossiers_regler,
        'dossiers_gagner': dossiers_gagner,
        'dossiers_perdu': dossiers_perdu,
        'pourcentage_gagner': pourcentage_gagner,
        'pourcentage_perdu': pourcentage_perdu,
        'pourcentage_regler': pourcentage_regler,

        #Stat agent
        "nb_total_dossiers_agent":nb_total_dossiers_agent,
        'dossiers_agent': dossiers_agent,
        "nb_dossiers_clos_agent":nb_dossiers_clos_agent,
        "nb_dossiers_agent_gagner":nb_dossiers_agent_gagner,
        "pourcentage_agent_gagner":pourcentage_agent_gagner,
        "pourcentage_agent_perdu":pourcentage_agent_perdu,

        # Solde caisse
        'solde_actuel': solde_actuel_usd,
        'solde_actuel_fc': solde_actuel_fc,
        'total_entrees_jour': total_entrees_jour_usd,
        'total_entrees_jour_fc': total_entrees_jour_fc,
        'total_sorties_jour': total_sorties_jour_usd,
        'total_sorties_jour_fc': total_sorties_jour_fc,
        'solde_mois': solde_mois_usd,
        'solde_mois_fc': solde_mois_fc,
    }

    context['revenus_mensuels'] = revenus_mensuels
    context['mois'] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    return render(request, "admin_template/index-1.html", context)


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
