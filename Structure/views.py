from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CabinetCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from Structure.models import Cabinet
from Adresse.models import adresse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def creer_cabinet(request):
    if request.method == 'POST':
        form = CabinetCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cabinet et compte administrateur créés avec succès.")
            return redirect('Creation_du_Cabinet')  # ou la page d'accueil admin
    else:
        form = CabinetCreationForm()
    return render(request, 'dev_template/index.html', {'form': form})



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Adresse.models import adresse

@login_required(login_url='Connexion')
def parametres_cabinet_ajax(request):
    user = request.user

    if not user.cabinet:
        return JsonResponse({'status': 'error', 'message': 'Aucun cabinet lié à cet utilisateur.'})

    cabinet = user.cabinet

    # RÉCUPÉRER OU CRÉER L’ADRESSE
    if cabinet.adresse:
        adr = cabinet.adresse
    else:
        adr = adresse.objects.create()
        cabinet.adresse = adr
        cabinet.save()

    # TRAITEMENT AJAX
    if request.method == 'POST':
        # ------------------------------
        #   1. INFOS DU CABINET
        # ------------------------------
        cabinet.nom = request.POST.get('nom_legal', cabinet.nom)
        cabinet.email = request.POST.get('email_general', cabinet.email)
        cabinet.telephone = request.POST.get('telephone_principal', cabinet.telephone)
        cabinet.telephone_secondaire = request.POST.get('telephone_secondaire', cabinet.telephone_secondaire)
        cabinet.forme_juridique_id = request.POST.get('forme_juridique', cabinet.forme_juridique_id)
        cabinet.num_id_fiscal = request.POST.get('num_id_fiscal', cabinet.num_id_fiscal)
        cabinet.reference = request.POST.get('reference', cabinet.reference)
        cabinet.site_web = request.POST.get('site_web', cabinet.site_web)
        cabinet.date_creations = request.POST.get('date_creations', cabinet.date_creations)
        cabinet.nom_fondateur =request.POST.get('nom_fondateur', cabinet.nom_fondateur)
        cabinet.numero_identification =request.POST.get('num_identification_rccm', cabinet.numero_identification)
        

        # Logo
        if request.FILES.get('logo'):
            cabinet.logo = request.FILES['logo']

        cabinet.save()

        # ------------------------------
        #   2. ADRESSE
        # ------------------------------
        adr.numero = request.POST.get('Numero', adr.numero)
        adr.avenue = request.POST.get('rue', adr.avenue)
        adr.quartier = request.POST.get('quartier', adr.quartier)
        adr.commune = request.POST.get('commune', adr.commune)  # texte
        adr.ville = request.POST.get('ville', adr.ville)        # texte
        adr.save()

        # ------------------------------
        #   3. RÉPONSE JSON
        # ------------------------------
        return JsonResponse({
            'status': 'success',
            'message': 'Paramètres du cabinet enregistrés avec succès.',
            'logo_url': cabinet.logo.url if cabinet.logo else ''
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})
