from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Paiement
from Dossier.models import dossier, TarifHoraire
from Agent.models import agent
import requests
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Sum
from parametre.models import taux
from datetime import datetime
import requests
from Structure.models import ServiceCabinet,Banque 
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.core.paginator import Paginator


def gestion_paiements(request, dossier_id):
    doss = get_object_or_404(dossier, id=dossier_id)
    cli = doss.client
    paiements = doss.paiements.all().order_by('-date_paiement')

    now = datetime.now()
   

    # récupérer le taux du cabinet
    tarif_horaire = TarifHoraire.objects.filter(cabinet=request.user.cabinet).first()

    t = taux.objects.filter(cabinet=request.user.cabinet).order_by('-date_ajouter').first()
    if not t:
        messages.error(request, "Aucun taux de change n'est défini pour ce cabinet.")
        return redirect('dossier_details', dossier_id=dossier_id)

    taux_fc = float(t.cout)

    montant_enreg_dollars = float(doss.montant_dollars_enreg or 0)
    montant_enreg_fc = float(doss.montant_fc_enreg or 0)

    # calculer le total déjà payé
    total_deja_paye_fc = float(paiements.aggregate(total=Sum("montant_payer_fc"))["total"] or 0)
    total_deja_paye_dollars = float(paiements.aggregate(total=Sum("montant_payer_dollars"))["total"] or 0)

    if request.method == "POST":
        montant = float(request.POST.get("montant", 0))
        devise = request.POST.get("devise")
        type_paiement = request.POST.get("type_paiement")
        personne = request.POST.get("personne_paye")
        notes = request.POST.get("notes")
        justificatif = request.FILES.get("justificatif")

        try:
            agent_logged = request.user.agent
        except:
            messages.error(request, "Erreur : Aucun agent associé à cet utilisateur.")
            return redirect(request.path)

        # Calcul du montant en FC si paiement en USD
        if devise == "USD":
            montant_dollars = montant
            montant_fc = montant * taux_fc
        else:
            montant_fc = montant
            montant_dollars = montant / taux_fc

        # Calcul du reste
        reste_dollars = montant_enreg_dollars - (total_deja_paye_dollars + montant_dollars)
        reste_fc = montant_enreg_fc - (total_deja_paye_fc + montant_fc)

        paiement = Paiement.objects.create(
            cabinet=request.user.cabinet,
            dossier=doss,
            client=cli,
            agent=agent_logged,
            personne_qui_paie=personne,
            montant_payer_dollars=montant_dollars,
            montant_payer_fc=montant_fc,
            montant_reste_dollars=reste_dollars,
            montant_reste_fc=reste_fc,
            devise=devise,
            type_paiement=type_paiement,
            notes=notes,
            justificatif=justificatif,
            taux=taux_fc,
            
        )

        # Si requête AJAX, renvoyer JSON avec URL de la facture
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            url_facture = reverse('imprimer_facture_paiement', args=[paiement.id])
            return JsonResponse({"success": True, "url_facture": url_facture})

        messages.success(request, "Paiement enregistré avec succès.")
        return redirect('dossier_details', dossier_id=dossier_id)

    return render(request, "admin_template/dossier_details.html", {
        "dossier": doss,
        "paiements": paiements,
        "client": cli
    })




def imprimer_facture_paiement(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)
    doss = paiement.dossier
    client = doss.client
    cabinet = request.user.cabinet
    today = datetime.now().strftime("%d/%m/%Y")  # Format français de la date

    JSREPORT_URL = "http://localhost:5488/api/report"

    # Fonction pour convertir Decimal en float pour JSON
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)

    # Récupérer la devise depuis la query string
    devise_choisie = request.GET.get("devise", paiement.devise)  # défaut à la devise du paiement

    if devise_choisie.upper() == "USD":
        montant_affiche = safe_float(paiement.montant_payer_dollars)
        reste_affiche = safe_float(paiement.montant_reste_dollars)
        devise_affiche = "USD"
    else:
        montant_affiche = safe_float(paiement.montant_payer_fc)
        reste_affiche = safe_float(paiement.montant_reste_fc)
        devise_affiche = "CDF"

    payload = {
    "template": {"name": "Facture_paiement_client"},
    "data": {
        "paiement": {
            "today": today,
            "date": paiement.date_paiement.strftime("%d/%m/%Y %H:%M"),
            "type_paiement": safe_str(paiement.type_paiement),
            "personne_qui_paie": safe_str(paiement.personne_qui_paie) if paiement.personne_qui_paie else f"{client.nom} {client.prenom}" ,
            "notes": safe_str(paiement.notes),
            "montant_USD": montant_affiche if devise_affiche=="USD" else 0,
            "montant_CDF": montant_affiche if devise_affiche=="CDF" else 0,
            "reste_affiche":reste_affiche,
        },
        "dossier": {
            "numero_dossier": safe_str(doss.numero_reference_dossier),
            "num_facture":doss.reference,
        },

        "client": {
            "nom": safe_str(client.nom),
            "prenom": safe_str(client.prenom),
            "telephone": safe_str(client.telephone),
            "email": safe_str(client.email),
            "adresse": f"{client.adresse.numero}, {client.adresse.avenue}, {client.adresse.quartier}, {client.adresse.commune}, {client.adresse.ville}"
        },
        "cabinet": {
            "nom": safe_str(cabinet.nom),
            "telephone": safe_str(cabinet.telephone),
            "email": safe_str(cabinet.email),
            "adresse": f"{cabinet.adresse.numero}, {cabinet.adresse.avenue}, {cabinet.adresse.quartier}, {cabinet.adresse.commune}, {cabinet.adresse.ville}",
            "logo": cabinet.logo.url if cabinet.logo else None,
        },
       
    }
}

    try:
        response = requests.post(JSREPORT_URL, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        return HttpResponse(f"Erreur lors de la génération du PDF : {e}", status=500)

    pdf = response.content
    return HttpResponse(pdf, content_type="application/pdf")



def caisse(request):
    cabinet = request.user.cabinet  # Cabinet de l’utilisateur connecté

    if request.method == "POST" and request.POST.get("type") == "sortie":
        
        montant = request.POST.get("montant")
        motif = request.POST.get("categorie")   # ex: frais électricité / achat meuble
        notes = request.POST.get("notes")
        date = request.POST.get("date")
        piece = request.FILES.get("piece")

        Paiement.objects.create(
            cabinet=cabinet,
            dossier=None,
            client=None,
            agent=request.user,      # l’utilisateur qui enregistre la sortie
            type_operation="SORTIE",
            montant_payer_dollars=montant,
            devise="USD",            # ou à récupérer dans ton formulaire
            montant_reste_dollars=0,
            type_paiement="SORTIE",
            motif=motif,
            notes=notes,
            date_paiement=date if date else timezone.now(),
            justificatif=piece
        )

        return redirect("caisse")  # retourne sur la même page

    paiements = Paiement.objects.filter(cabinet=cabinet).order_by("-date_paiement")

    return render(request, "caisse.html", {"paiements": paiements})



@login_required
def gerer_caisse(request):
    cabinet = request.user.cabinet
    devise = "USD"  # ou récupérer selon ton cabinet

    # 1. Récupération du dernier taux
    t = taux.objects.filter(cabinet=request.user.cabinet).order_by('-date_ajouter').first()
    taux_fc = Decimal(t.cout) 
    if t:
      taux_change =taux_fc   # Decimal
    else:
      taux_change = 0.0   # par défaut
    
    #Recuperations des mouvements
    mouvements = Paiement.objects.filter(cabinet=cabinet).order_by("-date_paiement")


    # Pagination : 10 mouvements par page
    paginator = Paginator(mouvements,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # =======================
    #  2. Calcul des entrées/sorties
    # =======================

    # Total entrées jour
    total_entrees_jour = Paiement.objects.filter(
        cabinet=cabinet,
        type_operation="ENTREE",
        date_paiement__date=timezone.now().date(),
    ).aggregate(total=Sum("montant_payer_dollars"))["total"] or 0
    total_entrees_jour_fc=total_entrees_jour*taux_change

    # Total sorties jour
    total_sorties_jour = Paiement.objects.filter(
        cabinet=cabinet,
        type_operation="SORTIE",
        date_paiement__date=timezone.now().date(),
    ).aggregate(total=Sum("montant_payer_dollars"))["total"] or 0
    total_sorties_jour_fc=total_sorties_jour*taux_change

    # Entrées totales
    total_entrees = Paiement.objects.filter(
        cabinet=cabinet,
        type_operation="ENTREE"
    ).aggregate(total=Sum("montant_payer_dollars"))["total"] or 0

    # Sorties totales
    total_sorties = Paiement.objects.filter(
        cabinet=cabinet,
        type_operation="SORTIE"
    ).aggregate(total=Sum("montant_payer_dollars"))["total"] or 0

    # =======================
    # 📌 3. Solde actuel
    # =======================
    solde_actuel = total_entrees - total_sorties
    solde_actuel_fc=solde_actuel* taux_change

    # =======================
    # 📌 4. Solde du mois
    # =======================
    today = timezone.now()
    total_entrees_mois = Paiement.objects.filter(
        cabinet=cabinet,
        type_operation="ENTREE",
        date_paiement__year=today.year,
        date_paiement__month=today.month,
    ).aggregate(total=Sum("montant_payer_dollars"))["total"] or 0
    total_entrees_mois_fc=total_entrees_mois*taux_change

    total_sorties_mois = Paiement.objects.filter(
        cabinet=cabinet,
        type_operation="SORTIE",
        date_paiement__year=today.year,
        date_paiement__month=today.month,
    ).aggregate(total=Sum("montant_payer_dollars"))["total"] or 0
    total_sortie_mois_fc=total_sorties_mois*taux_change

    solde_mois = total_entrees_mois - total_sorties_mois
    solde_mois_fc=solde_mois* taux_change
     
    dossiers = dossier.objects.select_related("client").all()

    # =======================
    # 📌 5. Contexte
    # =======================
    context = {
        "now": date.today(),
        "mouvements": mouvements,
        "total_entrees_jour": total_entrees_jour,
        "total_entrees_jour_fc":total_entrees_jour_fc,
        "total_sorties_jour": total_sorties_jour,
        "total_sorties_jour_fc":total_sorties_jour_fc,
        "solde_actuel": solde_actuel,
        "solde_actuel_fc":solde_actuel_fc,
        "solde_mois": solde_mois,
        "solde_mois_fc":solde_mois_fc,
        "devise": devise,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "dossiers": dossiers,
    }

    return render(request, "admin_template/gere_caisse.html", context)


from datetime import date
@login_required
def ajouter_sortie(request):
    if request.method == "POST":
        cabinet = request.user.cabinet
        
        # Récupération des données du formulaire
        montant = request.POST.get('montant')
        devise = request.POST.get('devise')
        motif = request.POST.get('categorie') or "Autre"
        notes = request.POST.get('notes', '')
        date_str = request.POST.get('date')
        type_paiement = request.POST.get('', 'Divers')
        #taux = request.POST.get('taux')
        justificatif = request.FILES.get('piece')

        t = taux.objects.filter(cabinet=request.user.cabinet).order_by('-date_ajouter').first()
        if not t:
           messages.error(request, "Aucun taux de change n'est défini pour ce cabinet.")
           
        taux_fc = float(t.cout)

        # Gestion de la date
        if date_str:
            from datetime import datetime
            try:
                date_paiement = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                date_paiement = timezone.now()
        else:
            date_paiement = timezone.now()

        # Conversion montant
        try:
            montant = float(montant)
        except (TypeError, ValueError):
            messages.error(request, "Montant invalide.")
            return redirect('caisse_dashboard')

        # Conversion en FC si nécessaire
        if devise == "USD":
            montant_dollars = montant
            montant_fc = montant * taux_fc
        else:
            montant_fc = montant
            montant_dollars = montant / taux_fc

        # Création du paiement
        paiement = Paiement.objects.create(
            cabinet=cabinet,
            dossier=None,  # pas lié à un dossier client ici
            client=None,   # pas lié à un client
            agent=request.user.agent if hasattr(request.user, 'agent') else '',
            montant_payer_dollars=montant_dollars,
            montant_payer_fc=montant_fc,
            devise=devise,
            motif=motif,
            notes=notes,
            type_paiement=type_paiement,
            taux=taux,
            date_paiement=date_paiement,
            type_operation="SORTIE",
            justificatif=justificatif
        )
       
        messages.success(request, f"Sortie de {montant} {devise} enregistrée avec succès !")
        return redirect('Gerer_caisse')
    else:
        messages.error(request, "Méthode non autorisée.")
        return redirect('Gerer_caisse')

    
def caisse_detail(request, id):
    mvt = Paiement.objects.get(id=id)
    return render(request, "admin_template/caisse_detail.html", {"mvt": mvt})

def caisse_edit(request, id):
    return HttpResponse("Édition à développer...")

def caisse_delete(request, id):
    return HttpResponse("Suppression à développer...")



def gestion_paiements_cabinet_client(request, dossier_id=None):
    """
    Gère tous les paiements :
    - Paiements liés à un client/dossier (dossier_id fourni)
    - Entrées pour le cabinet (dossier_id None ou via modal)
    """

    # Si dossier_id fourni, récupération du dossier et client
    doss = get_object_or_404(dossier, id=dossier_id) if dossier_id else None
    cli = doss.client if doss else None

    # Paiements liés au dossier ou vide si cabinet
    paiements = doss.paiements.all() if doss else Paiement.objects.none()

    # Taux courant du cabinet
    t = taux.objects.filter(cabinet=request.user.cabinet).order_by('-date_ajouter').first()
    if not t:
        messages.error(request, "Aucun taux de change n'est défini pour ce cabinet.")
        return redirect('dossier_details', dossier_id=dossier_id) if dossier_id else redirect('dashboard')

    taux_fc = float(t.cout)

    montant_enreg_dollars = float(doss.montant_dollars_enreg or 0) if doss else 0
    montant_enreg_fc = float(doss.montant_fc_enreg or 0) if doss else 0

    # Total déjà payé
    total_deja_paye_dollars = float(paiements.aggregate(total=Sum("montant_payer_dollars"))["total"] or 0)
    total_deja_paye_fc = float(paiements.aggregate(total=Sum("montant_payer_fc"))["total"] or 0)

    if request.method == "POST":
       
        montant_str = request.POST.get("montant_hidden", "0").strip()
        
        try:
            montant = float(montant_str) if montant_str else 0.0
        except ValueError:
            messages.error(request, "Le montant doit être un nombre valide.")
            return redirect(request.path)
        entry_type = request.POST.get("entry_type", "client")  # 'client' ou 'cabinet'
        devise = request.POST.get("devise_client") if entry_type=="client" else request.POST.get("devise")
        type_paiement = request.POST.get("type_paiement")
        notes = request.POST.get("notes")
        justificatif = request.FILES.get("justificatif")    
        motif = request.POST.get("motif") or ("Paiement du client" if entry_type=="client" else "Entrée cabinet")
        
       


        # Personne qui paie, uniquement si client
        personne = request.POST.get("personne_paye") if entry_type == "client" else None


        banque_id = request.POST.get("banque_hidden")
        banque_instance = None
        if banque_id:
           try:
              banque_instance = Banque.objects.get(id=banque_id, cabinet=request.user.cabinet)
           except Banque.DoesNotExist:
              banque_instance = None  # si l'ID n'appartient pas au cabinet ou invalide

        if type_paiement == "Virement Bancaire" and not banque_instance:
           messages.error(request, "Veuillez sélectionner une banque pour le virement.")
           return redirect(request.path)



        # ---------------- Vérification agent ----------------
        try:
            agent_logged = request.user.agent
        except:
            messages.error(request, "Erreur : Aucun agent associé à cet utilisateur.")
            return redirect('dossier_details', dossier_id=dossier_id) if dossier_id else redirect('dashboard')

        # ---------------- Calcul montants ----------------
        if devise == "USD":
            montant_dollars = montant
            montant_fc = montant * taux_fc
        else:
            montant_fc = montant
            montant_dollars = montant / taux_fc

        # Reste à payer uniquement si dossier lié
        reste_dollars = montant_enreg_dollars - (total_deja_paye_dollars + montant_dollars) if doss else 0
        reste_fc = montant_enreg_fc - (total_deja_paye_fc + montant_fc) if doss else 0

        # ---------------- Création du paiement ----------------
        paiement = Paiement.objects.create(
            cabinet=request.user.cabinet,
            dossier=doss if entry_type == "client" else None,
            client=cli if entry_type == "client" else None,
            agent=agent_logged,
            personne_qui_paie=personne,
            montant_payer_dollars=montant_dollars,
            montant_payer_fc=montant_fc,
            montant_reste_dollars=reste_dollars,
            montant_reste_fc=reste_fc,
            devise=devise,
            type_paiement=type_paiement,
            notes=notes,
            justificatif=justificatif,
            taux=taux_fc,
            motif=motif,
            type_operation="ENTREE",
            banque=banque_instance
        )

       # ignorer si banque invalide

        # ---------------- Gestion AJAX ----------------
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            url_facture = reverse('imprimer_facture_paiement', args=[paiement.id])
            return JsonResponse({"success": True, "url_facture": url_facture})

        messages.success(request, "Paiement enregistré avec succès.")
        # Redirection selon le type d'entrée
        if entry_type == "client" and dossier_id:
            return redirect('dossier_details', dossier_id=dossier_id)
        elif entry_type == "cabinet" and not dossier_id:
            return redirect('Gerer_caisse')
        else:
            return redirect('Gerer_caisse')  # pour entrée cabinet

    # ---------------- Render ----------------
    context = {
        "dossier": doss,
        "paiements": paiements,
        "client": cli,
        "taux_du_jour": taux_fc,
        "banques": request.user.cabinet.Banque_cabinet.all()
    }
    return render(request, "admin_template/dossier_details.html", context)
