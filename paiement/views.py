from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Paiement
from Dossier.models import dossier, TarifHoraire
from Agent.models import agent

def gestion_paiements(request, dossier_id):

    doss = get_object_or_404(dossier, id=dossier_id)

    # récupérer automatiquement le client du dossier
    cli = doss.client  

    # historique depuis la BDD
    paiements = doss.paiements.all().order_by('-date_paiement')

    if request.method == "POST":

        montant = request.POST.get("montant")
        devise = request.POST.get("devise")
        type_paiement = request.POST.get("type_paiement")
        personne = request.POST.get("personne_paye")
        notes = request.POST.get("notes")

        # fichier
        justificatif = request.FILES.get("justificatif")

        # récupérer l’agent connecté
        try:
            agent_logged = request.user.agent
        except:
            messages.error(request, "Erreur : Aucun agent associé à cet utilisateur.")
            return redirect(request.path)
        
        tarif_horaire = TarifHoraire.objects.filter(cabinet=request.user.cabinet).first()

        Paiement.objects.create(
            cabinet=request.user.cabinet,
            dossier=doss,
            client=cli,
            agent=agent_logged,
            personne_qui_paie=personne,
            montant=montant,
            devise=devise,
            type_paiement=type_paiement,
            notes=notes,
            justificatif=justificatif,
            taux=tarif_horaire.taux_jour
        )

        messages.success(request, "Paiement enregistré avec succès.")
        return redirect('dossier_details',dossier_id)

    return render(request, "admin_template/dossier_details.html", {
        "dossier": doss,
        "paiements": paiements,
        "client":cli
    })
