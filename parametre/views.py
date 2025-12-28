from django.shortcuts import get_object_or_404,render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Adresse.models import commune,Ville
from Dossier.models import SecteurFoncier, type_dossier,TarifHoraire,TarifActivite,TypePiece
from Structure.models import Activite, Specialite
from Structure.models import Cabinet,PosteAvocat,Juridiction, ServiceCabinet,Banque
from Adresse.models import adresse
from django.urls import reverse
from decimal import Decimal, InvalidOperation
from parametre.models import taux



# -------------------- COMMUNE --------------------
@login_required(login_url='Connexion')
def liste_communes(request):
    communes = commune.objects.filter(cabinet=request.user.cabinet)
    data = [
        {
            'id': c.id,
            'nom': c.nom,
            'date': c.date_ouverture.strftime('%d/%m/%Y')
        } for c in communes
    ]
    return JsonResponse({'communes': data})

@login_required(login_url='Connexion')
def ajouter_commune_ajax(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()

        if not nom:
            return JsonResponse({'success': False, 'message': 'Le nom est obligatoire.'})

        if commune.objects.filter(nom__iexact=nom,cabinet=request.user.cabinet).exists():
            return JsonResponse({'success': False, 'message': 'Cette commune existe déjà !'})

        c = commune.objects.create(nom=nom, cabinet=request.user.cabinet)

        row_html = f'''
        <tr id="commune{c.id}">
            <td>{c.id}</td>
            <td>{c.nom}</td>
            <td>{c.date_ouverture.strftime("%d/%m/%Y")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="commune{c.id}" data-msg="msgCommune"
                    data-url="{reverse('modifier_commune_ajax', args=[c.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="commune{c.id}" data-url="{reverse('supprimer_commune_ajax', args=[c.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''

        return JsonResponse({'success': True, 'row_html': row_html})


# -------------------- MODIFIER COMMUNE --------------------
@login_required(login_url='Connexion')
def modifier_commune_ajax(request, id):
    c = get_object_or_404(commune, id=id)
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()

        if not nom:
            return JsonResponse({'success': False, 'message': 'Le nom est obligatoire.'})

        if commune.objects.filter(nom__iexact=nom, cabinet=request.user.cabinet).exclude(id=c.id).exists():
            return JsonResponse({'success': False, 'message': 'Le nom que vous voulez utiliser existe déjà !'})

        c.nom = nom
        c.save()

        row_html = f'''
        <tr id="commune{c.id}">
            <td>{c.id}</td>
            <td>{c.nom}</td>
            <td>{c.date_ouverture.strftime("%d/%m/%Y")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="commune{c.id}" data-msg="msgCommune"
                    data-url="{reverse('modifier_commune_ajax', args=[c.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="commune{c.id}" data-url="{reverse('supprimer_commune_ajax', args=[c.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''

        return JsonResponse({'success': True, 'row_html': row_html})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


@login_required(login_url='Connexion')
def supprimer_commune_ajax(request, id):
    c = get_object_or_404(commune, id=id)
    c.delete()
    return JsonResponse({'success': True, 'id': id})


# -------------------- SECTEUR --------------------
@login_required(login_url='Connexion')
def liste_secteurs_ajax(request):
    secteurs = SecteurFoncier.objects.filter(cabinet=request.user.cabinet)
    data = []
    for s in secteurs:
        data.append({
            'id': s.id,
            'nom': s.nom,
            'communes': [{'id': c.id, 'nom': c.nom} for c in s.communes.filter(cabinet=request.user.cabinet)]
        })
    return JsonResponse({'secteurs': data})

@login_required(login_url='Connexion')
def ajouter_secteur_ajax(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        communes_ids = request.POST.getlist('communes[]')

        if SecteurFoncier.objects.filter(nom__iexact=nom, cabinet=request.user.cabinet).exists():
            return JsonResponse({'success': False, 'message': 'Le secteur existe déjà'})

        s = SecteurFoncier.objects.create(nom=nom, cabinet=request.user.cabinet)

        for cid in communes_ids:
            c = commune.objects.get(id=cid)
            if c.secteurs.filter(cabinet=request.user.cabinet).exists():
                s.delete()
                return JsonResponse({'success': False, 'message': f'La commune {c.nom} est déjà assignée à un secteur'})
            s.communes.add(c)

        communes_html = " ".join([f'<span class="badge bg-info">{c.nom}</span>' for c in s.communes.filter(cabinet=request.user.cabinet)])

        row_html = f'''
        <tr id="secteur{s.id}">
            <td>{s.id}</td>
            <td>{s.nom}</td>
            <td>{communes_html}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="secteur{s.id}" data-msg="msgSecteur"
                    data-url="{reverse('modifier_secteur_ajax', args=[s.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="secteur{s.id}" data-url="{reverse('supprimer_secteur_ajax', args=[s.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''

        return JsonResponse({'success': True, 'row_html': row_html})


# -------------------- MODIFIER SECTEUR --------------------
@login_required(login_url='Connexion')
def modifier_secteur_ajax(request, secteur_id):
    s = get_object_or_404(SecteurFoncier, id=secteur_id)
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        communes_ids = request.POST.getlist('communes[]')

        if SecteurFoncier.objects.filter(nom__iexact=nom,cabinet=request.user.cabinet).exclude(id=s.id).exists():
            return JsonResponse({'success': False, 'message': 'Nom de secteur déjà utilisé'})

        s.nom = nom
        s.save()
        s.communes.clear()

        for cid in communes_ids:
            c = commune.objects.get(id=cid)
            if c.secteurs.filter(cabinet=s.cabinet).exclude(id=s.id).exists():
                return JsonResponse({'success': False, 'message': f'La commune {c.nom} est déjà assignée à un secteur'})
            s.communes.add(c)

        communes_html = " ".join([f'<span class="badge bg-info">{c.nom}</span>' for c in s.communes.filter(cabinet=request.user.cabinet)])

        row_html = f'''
        <tr id="secteur{s.id}">
            <td>{s.id}</td>
            <td>{s.nom}</td>
            <td>{communes_html}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="secteur{s.id}" data-msg="msgSecteur"
                    data-url="{reverse('modifier_secteur_ajax', args=[s.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="secteur{s.id}" data-url="{reverse('supprimer_secteur_ajax', args=[s.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''

        return JsonResponse({'success': True, 'row_html': row_html})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


@login_required(login_url='Connexion')
def supprimer_secteur_ajax(request, secteur_id):
    s = get_object_or_404(SecteurFoncier, id=secteur_id)
    s.delete()
    return JsonResponse({'success': True, 'id': secteur_id})


@login_required(login_url='Connexion')
def retirer_commune_ajax(request, secteur_id, commune_id):
    s = get_object_or_404(SecteurFoncier, id=secteur_id)
    c = get_object_or_404(commune, id=commune_id)
    s.communes.remove(c)
    return JsonResponse({'success': True, 'secteur_id': s.id, 'commune_id': c.id})


# -------------------- TYPE DE DOSSIER --------------------
@login_required(login_url='Connexion')
def liste_type_dossier_ajax(request):
    types = type_dossier.objects.filter(cabinet=request.user.cabinet)
    data = [{'id': t.id, 'nom': t.nom_type, 'date': t.date_ajouter.strftime('%d/%m/%Y')} for t in types]
    return JsonResponse({'types_dossier': data})

@login_required(login_url='Connexion')
def ajouter_type_dossier_ajax(request):
    if request.method == 'POST':
        nom_type = request.POST.get('nom_type', '').strip()

        if type_dossier.objects.filter(nom_type__iexact=nom_type,cabinet=request.user.cabinet).exists():
            return JsonResponse({'success': False, 'message': 'Ce type de dossier existe déjà !'})

        t = type_dossier.objects.create(nom_type=nom_type,cabinet=request.user.cabinet)

        row_html = f'''
        <tr id="typeDossier{t.id}">
            <td>{t.id}</td>
            <td>{t.nom_type}</td>
            <td>{t.date_ajouter.strftime("%d/%m/%Y")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="typeDossier{t.id}" data-msg="msgTypeDossier"
                    data-url="{reverse('modifier_type_dossier_ajax', args=[t.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="typeDossier{t.id}" data-url="{reverse('supprimer_type_dossier_ajax', args=[t.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''

        return JsonResponse({'success': True, 'row_html': row_html})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


# -------------------- MODIFIER TYPE DOSSIER --------------------
@login_required(login_url='Connexion')
def modifier_type_dossier_ajax(request, type_id):
    t = get_object_or_404(type_dossier, id=type_id)
    if request.method == 'POST':
        nom_type = request.POST.get('nom_type', '').strip()

        # Vérifier doublon sauf pour l'objet actuel
        if type_dossier.objects.filter(nom_type__iexact=nom_type,cabinet=request.user.cabinet).exclude(id=t.id).exists():
            return JsonResponse({'success': False, 'message': 'Nom déjà utilisé'})

        t.nom_type = nom_type
        t.save()

        row_html = f'''
        <tr id="typeDossier{t.id}">
            <td>{t.id}</td>
            <td>{t.nom_type}</td>
            <td>{t.date_ajouter.strftime("%d/%m/%Y")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="typeDossier{t.id}" data-msg="msgTypeDossier"
                    data-url="{reverse('modifier_type_dossier_ajax', args=[t.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="typeDossier{t.id}" data-url="{reverse('supprimer_type_dossier_ajax', args=[t.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''

        return JsonResponse({'success': True, 'row_html': row_html})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


@login_required(login_url='Connexion')
def supprimer_type_dossier_ajax(request, type_id):
    t = get_object_or_404(type_dossier, id=type_id)
    t.delete()
    return JsonResponse({'success': True, 'id': type_id})


# -------------------- ACTIVITE --------------------
@login_required(login_url='Connexion')
def liste_activites_ajax(request):
    acts = Activite.objects.filter(cabinet=request.user.cabinet)
    data = [{'id': a.id, 'nom': a.nom_activite, 'description': a.description, 'date': a.date_activite.strftime('%d/%m/%Y %H:%M')} for a in acts]
    return JsonResponse({'activites': data})

@login_required(login_url='Connexion')
def ajouter_activite_ajax(request):
    if request.method == 'POST':
        nom = request.POST.get('nom_activite', '').strip()
        #description = request.POST.get('description', '').strip()

        # Vérifier doublon
        if Activite.objects.filter(nom_activite__iexact=nom,cabinet=request.user.cabinet).exists():
            return JsonResponse({'success': False, 'message': 'Cette activité existe déjà !'})

        a = Activite.objects.create(nom_activite=nom,cabinet=request.user.cabinet)

        row_html = f'''
        <tr id="activite{a.id}">
            <td>{a.id}</td>
            <td>{a.nom_activite}</td>
            <td>{a.date_activite.strftime("%d/%m/%Y %H:%M")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="activite{a.id}" data-msg="msgActivite"
                    data-url="{reverse('modifier_activite_ajax', args=[a.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="activite{a.id}" data-url="{reverse('supprimer_activite_ajax', args=[a.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''

        return JsonResponse({'success': True, 'row_html': row_html})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


# -------------------- MODIFIER ACTIVITE --------------------
@login_required(login_url='Connexion')
def modifier_activite_ajax(request, id):
    a = get_object_or_404(Activite, id=id)
    if request.method == 'POST':
        nom = request.POST.get('nom_activite', '').strip()
        description = request.POST.get('description', '').strip()

        # Vérifier doublon sauf pour l'objet en cours
        if Activite.objects.filter(nom_activite__iexact=nom).exclude(id=a.id).exists():
            return JsonResponse({'success': False, 'message': 'Cette activité existe déjà !'})

        a.nom_activite = nom
        a.description = description
        a.save()

        row_html = f'''
        <tr id="activite{a.id}">
            <td>{a.id}</td>
            <td>{a.nom_activite}</td>
            <td>{a.date_activite.strftime("%d/%m/%Y %H:%M")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="activite{a.id}" data-msg="msgActivite"
                    data-url="{reverse('modifier_activite_ajax', args=[a.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="activite{a.id}" data-url="{reverse('supprimer_activite_ajax', args=[a.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''
        return JsonResponse({'success': True, 'row_html': row_html})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

@login_required(login_url='Connexion')
def supprimer_activite_ajax(request, id):
    a = get_object_or_404(Activite, id=id)
    a.delete()
    return JsonResponse({'success': True, 'id': id})


# -------------------- SPECIALITE --------------------
@login_required(login_url='Connexion')
def liste_specialites_ajax(request):
    specs = Specialite.objects.filter(cabinet=request.user.cabinet)
    data = [{'id': s.id, 'nom': s.nom, 'date': s.date_ajouter.strftime('%d/%m/%Y %H:%M')} for s in specs]
    return JsonResponse({'specialites': data})


@login_required(login_url='Connexion')
def ajouter_specialite_ajax(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()

        # Vérifier doublon
        if Specialite.objects.filter(nom__iexact=nom,cabinet=request.user.cabinet).exists():
            return JsonResponse({'success': False, 'message': 'Cette spécialité existe déjà !'})

        s = Specialite.objects.create(nom=nom,cabinet=request.user.cabinet)

        # Générer HTML de la ligne à renvoyer
        row_html = f'''
        <tr id="specialite{s.id}">
            <td>{s.id}</td>
            <td>{s.nom}</td>
            <td>{s.date_ajouter.strftime("%d/%m/%Y %H:%M")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="specialite{s.id}" data-msg="msgSpecialite"
                    data-url="{reverse('modifier_specialite_ajax', args=[s.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="specialite{s.id}" data-url="{reverse('supprimer_specialite_ajax', args=[s.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''
        return JsonResponse({'success': True, 'row_html': row_html})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


# -------------------- MODIFIER SPECIALITE --------------------
@login_required(login_url='Connexion')
def modifier_specialite_ajax(request, id):
    s = get_object_or_404(Specialite, id=id)
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()

        # Vérifier doublon sauf pour l'objet en cours
        if Specialite.objects.filter(nom__iexact=nom,cabinet=request.user.cabinet).exclude(id=s.id).exists():
            return JsonResponse({'success': False, 'message': 'Cette spécialité existe déjà !'})

        s.nom = nom
        s.save()

        # Générer HTML de la ligne modifiée
        row_html = f'''
        <tr id="specialite{s.id}">
            <td>{s.id}</td>
            <td>{s.nom}</td>
            <td>{s.date_ajouter.strftime("%d/%m/%Y %H:%M")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="specialite{s.id}" data-msg="msgSpecialite"
                    data-url="{reverse('modifier_specialite_ajax', args=[s.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="specialite{s.id}" data-url="{reverse('supprimer_specialite_ajax', args=[s.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''
        return JsonResponse({'success': True, 'row_html': row_html})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

@login_required(login_url='Connexion')
def supprimer_specialite_ajax(request, id):
    s = get_object_or_404(Specialite, id=id)
    s.delete()
    return JsonResponse({'success': True, 'id': id})



# -------------------- API POUR RÉCUPÉRER LES ACTIVITÉS --------------------

@login_required(login_url='Connexion')
def get_activites_disponibles(request):
    """Récupère toutes les activités disponibles pour le cabinet"""
    try:
        cabinet_user = getattr(request.user, 'cabinet', None)
        if not cabinet_user:
            return JsonResponse({"success": False, "message": "Aucun cabinet associé."})
        
        activites = Activite.objects.filter(cabinet=cabinet_user).values('id', 'nom_activite')
        activites_list = list(activites)
        
        return JsonResponse({"success": True, "activites": activites_list})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


# -------------------- --------------------------TARIFICATION ------------------------------------------------
from decimal import Decimal, InvalidOperation

@login_required(login_url='Connexion')
def liste_tarifs_ajax(request):
    """
    Liste tous les tarifs du cabinet connecté
    """
    cabinet_user = getattr(request.user, 'cabinet', None)
    tarifs = TarifHoraire.objects.filter(cabinet=cabinet_user).select_related('type_dossier', 'activite')

    data = []
    for t in tarifs:
        data.append({
            'id': t.id,
            'type_dossier': t.type_dossier.nom_type if t.type_dossier else '',
            'activite': t.activite.nom_activite if t.activite else '',
            'prix': t.prix,
            'date': t.date_ajouter.strftime('%d/%m/%Y %H:%M')
        })
    return JsonResponse({'tarifs': data})



@login_required(login_url='Connexion')
def ajouter_tarif_ajax(request):
    if request.method == "POST":
        try:
            secteur_id = request.POST.get("secteur")
            type_id = request.POST.get("type_dossier")
            montant_dollars = request.POST.get("montant_dollars")
            description = request.POST.get("description", "")
            
            # Récupération des activités et leurs prix
            activites_ids = request.POST.getlist("activites_ids[]")
            activites_prix = request.POST.getlist("activites_prix[]")

            # Validation
            if not secteur_id or not type_id or not montant_dollars:
                return JsonResponse({"success": False, "message": "Tous les champs sont obligatoires."})

            cabinet_user = getattr(request.user, "cabinet", None)
            if not cabinet_user:
                return JsonResponse({"success": False, "message": "Aucun cabinet associé à cet utilisateur."})

            secteur_obj = get_object_or_404(SecteurFoncier, id=secteur_id)
            type_obj = get_object_or_404(type_dossier, id=type_id)

            try:
                montant_dollars = Decimal(montant_dollars)
            except InvalidOperation:
                return JsonResponse({"success": False, "message": "Montant ou taux invalide."})

            # Vérification doublon
            if TarifHoraire.objects.filter(cabinet=cabinet_user, type_dossier=type_obj, secteur=secteur_obj).exists():
                return JsonResponse({"success": False, "message": "Ce tarif existe déjà pour ce type et secteur."})
            
            # Récupérer le dernier taux pour ce cabinet
            dernier_taux = taux.objects.filter(cabinet=cabinet_user).order_by('-date_ajouter').first()
            taux_jour_utilise = dernier_taux.cout if dernier_taux else Decimal(0)

            # Création du tarif
            tarif = TarifHoraire.objects.create(
                cabinet=cabinet_user,
                type_dossier=type_obj,
                secteur=secteur_obj,
                montant_dollars=montant_dollars,
                taux_jour=taux_jour_utilise,
                description=description
            )
            
            # Création des activités liées au tarif
            for i, activite_id in enumerate(activites_ids):
                if activite_id and i < len(activites_prix):
                    try:
                        activite_obj = get_object_or_404(Activite, id=activite_id)
                        prix_activite = Decimal(activites_prix[i])
                        
                        TarifActivite.objects.create(
                            tarif=tarif,
                            activite=activite_obj,
                            prix_dollars=prix_activite,
                            cabinet=cabinet_user
                        )
                    except (InvalidOperation, ValueError):
                        continue

            # Construction des données des activités pour l'affichage
            activites_data = []
            for ta in tarif.activites_tarif.all():
                activites_data.append({
                    'id': ta.activite.id,
                    'nom': ta.activite.nom_activite,
                    'prix': str(ta.prix_dollars)
                })

            # Construction de la ligne HTML à renvoyer
            row_html = f"""
            <tr id='tarif{tarif.id}' data-description='{tarif.description}' data-activites='{activites_data}'>
                <td>{tarif.id}</td>
                <td>{tarif.secteur.nom}</td>
                <td>{tarif.type_dossier.nom_type}</td>
                <td>{tarif.montant_dollars}</td>
                <td>{tarif.taux_jour}</td>
                <td>{tarif.montant_fc}</td>
                <td class="text-center">
                    <button class="btn btn-sm btn-warning btn-edit-ajax"
                        data-row="tarif{tarif.id}" data-msg="msgTarif"
                        data-url="{reverse('modifier_tarif_ajax', args=[tarif.id])}">
                        <i class="mdi mdi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-danger btn-delete-ajax"
                        data-row="tarif{tarif.id}"
                        data-url="{reverse('supprimer_tarif_ajax', args=[tarif.id])}">
                        <i class="mdi mdi-delete"></i>
                    </button>
                </td>
            </tr>
            """

            return JsonResponse({"success": True, "message": "Tarif ajouté avec succès.", "row_html": row_html})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erreur : {str(e)}"})

    return JsonResponse({"success": False, "message": "Méthode non autorisée."})

# -------------------- MODIFIER TARIF --------------------

@login_required(login_url='Connexion')
def get_activites_tarif(request, tarif_id):#il recupere les activite lier a un tarif
    """Renvoie la liste des activités liées à un tarif donné en JSON"""
    try:
        tarif = get_object_or_404(TarifHoraire, id=tarif_id)
        activites = [
            {
                "id": ta.activite.id,
                "nom": ta.activite.nom_activite,
                "prix": str(ta.prix_dollars)
            }
            for ta in tarif.activites_tarif.all()
        ]
        return JsonResponse({"success": True, "activites": activites})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})

@login_required(login_url='Connexion')
def modifier_tarif_ajax(request, tarif_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Méthode non autorisée."})

    try:
        tarif = get_object_or_404(TarifHoraire, id=tarif_id)
        secteur = get_object_or_404(SecteurFoncier, id=request.POST.get("secteur"))
        type_obj = get_object_or_404(type_dossier, id=request.POST.get("type_dossier"))

        montant_dollars = Decimal(request.POST.get("montant_dollars"))
        taux_jour = Decimal(request.POST.get("taux_jour"))
        description = request.POST.get("description", "")
        activites_ids = request.POST.getlist("activites[]")
        prix_activites = request.POST.getlist("prix_activite[]")

        # Mise à jour du tarif
        tarif.secteur = secteur
        tarif.type_dossier = type_obj
        tarif.montant_dollars = montant_dollars
        tarif.taux_jour = taux_jour
        tarif.description = description
        tarif.montant_fc = montant_dollars * taux_jour
        tarif.save()

        # Mise à jour des activités
        TarifActivite.objects.filter(tarif=tarif).delete()
        for act_id, prix in zip(activites_ids, prix_activites):
            if act_id and prix:
                try:
                    act_obj = get_object_or_404(Activite, id=act_id)
                    TarifActivite.objects.create(
                        tarif=tarif,
                        activite=act_obj,
                        prix_dollars=Decimal(prix)
                    )
                except InvalidOperation:
                    continue

        # Construction de la ligne HTML mise à jour
        activites_data = ",".join([
                 '{"id":"%s","nom":"%s","prix":"%s"}' % (ta.activite.id, ta.activite.nom_activite, ta.prix_dollars)
                  for ta in tarif.activites_tarif.all()
                      ])


        row_html = f"""
        <tr id='tarif{tarif.id}' data-description='{tarif.description}' data-activites='[{activites_data}]'>
            <td>{tarif.id}</td>
            <td>{tarif.secteur.nom}</td>
            <td>{tarif.type_dossier.nom_type}</td>
            <td>{tarif.montant_dollars}</td>
            <td>{int(tarif.taux_jour)}</td>
            <td>{tarif.montant_fc}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="tarif{tarif.id}" data-msg="msgTarif"
                    data-url="{reverse('modifier_tarif_ajax', args=[tarif.id])}">
                    <i class="mdi mdi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="tarif{tarif.id}"
                    data-url="{reverse('supprimer_tarif_ajax', args=[tarif.id])}">
                    <i class="mdi mdi-delete"></i>
                </button>
            </td>
        </tr>
        """

        return JsonResponse({"success": True, "message": "Tarif modifié avec succès.", "row_html": row_html})

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Erreur inattendue : {str(e)}"})
    


@login_required(login_url='Connexion')
def supprimer_tarif_ajax(request, tarif_id):
    """
    Supprime un tarif
    """
    t = get_object_or_404(TarifHoraire, id=tarif_id)
    t.delete()
    return JsonResponse({'success': True, 'id': tarif_id})




# ================= POSTE AVOCAT ====================

@login_required
def ajouter_poste_avocat_ajax(request):
    if request.method == "POST":
        nom_poste = request.POST.get("nom_poste")
        #description = request.POST.get("description", "")
        cabinet = request.user.cabinet

        # Vérifier doublon pour le cabinet
        if PosteAvocat.objects.filter(nom_poste__iexact=nom_poste, cabinet=cabinet).exists():
            return JsonResponse({'success': False, 'message': "Ce poste existe déjà pour votre cabinet."})

        poste = PosteAvocat.objects.create(
            nom_poste=nom_poste,
           # description=description,
            cabinet=cabinet
        )
        return JsonResponse({
            'success': True,
            'message': "Poste ajouté avec succès.",
            'row': f"""
                <tr id='poste{poste.id}'>
                    <td>-</td>
                    <td>{poste.nom_poste}</td>
                    <td>{poste.date_ajouter or ''}</td>
                    <td class='text-center'>
                        <button class='btn btn-sm btn-warning btn-edit-ajax' data-row='poste{poste.id}' data-msg='msgPosteAvocat' data-url='/poste/{poste.id}/modifier/'>
                            <i class='mdi mdi-pencil'></i>
                        </button>
                        <button class='btn btn-sm btn-danger btn-delete-ajax' data-row='poste{poste.id}' data-url='/poste/{poste.id}/supprimer/'>
                            <i class='mdi mdi-delete'></i>
                        </button>
                    </td>
                </tr>
            """
        })
    return JsonResponse({'success': False, 'message': "Requête invalide."})


@login_required
def modifier_poste_avocat_ajax(request, id):
    poste = get_object_or_404(PosteAvocat, id=id, cabinet=request.user.cabinet)
    if request.method == "POST":
        nom_poste = request.POST.get("nom_poste")
        poste.nom_poste = nom_poste
        poste.save()
        return JsonResponse({
            'success': True,
            'message': "Poste modifié avec succès.",
            'row_html': f"""
                <tr id='poste{poste.id}'>
                    <td>-</td>
                    <td>{poste.nom_poste}</td>
                    <td>{poste.date_ajouter.strftime("%d/%m/%Y %H:%M")}</td>                   
                    <td class='text-center'>
                        <button class='btn btn-sm btn-warning btn-edit-ajax' data-row='poste{poste.id}' data-msg='msgPosteAvocat' data-url='/poste/{poste.id}/modifier/'>
                            <i class='mdi mdi-pencil'></i>
                        </button>
                        <button class='btn btn-sm btn-danger btn-delete-ajax' data-row='poste{poste.id}' data-url='/poste/{poste.id}/supprimer/'>
                            <i class='mdi mdi-delete'></i>
                        </button>
                    </td>
                </tr>
            """
        })
    return JsonResponse({'success': False, 'message': "Méthode non autorisée."})


@login_required
def supprimer_poste_avocat_ajax(request, id):
    poste = get_object_or_404(PosteAvocat, id=id, cabinet=request.user.cabinet)
    poste.delete()
    return JsonResponse({'success': True, 'message': "Poste supprimé avec succès."})


# ================= Service cabinet ====================

@login_required
def ajouter_service_cabinet_ajax(request):
    if request.method == "POST":
        nom_service = request.POST.get("nom_service")
        #description = request.POST.get("description", "")
        cabinet = request.user.cabinet

        # Vérifier doublon pour le cabinet
        if ServiceCabinet.objects.filter(nom_service__iexact=nom_service, cabinet=cabinet).exists():
            return JsonResponse({'success': False, 'message': "Ce service existe déjà pour votre cabinet."})

        service = ServiceCabinet.objects.create(
            nom_service=nom_service,
           # description=description,
            cabinet=cabinet
        )
        return JsonResponse({
            'success': True,
            'message': "Service ajouté avec succès.",
            'row_html': f"""
                <tr id='service{service.id}'>
                    <td>-</td>
                    <td>{service.nom_service}</td>
                    <td>{service.date_ajouter or ''}</td>
                    <td class='text-center'>
                        <button class='btn btn-sm btn-warning btn-edit-ajax' data-row='service{service.id}' data-msg='msgServiceCabinet' data-url='/service/{service.id}/modifier/'>
                            <i class='mdi mdi-pencil'></i>
                        </button>
                        <button class='btn btn-sm btn-danger btn-delete-ajax' data-row='service{service.id}' data-url='/service/{service.id}/supprimer/'>
                            <i class='mdi mdi-delete'></i>
                        </button>
                    </td>
                </tr>
            """
        })
    return JsonResponse({'success': False, 'message': "Requête invalide."})


@login_required
def modifier_service_cabinet_ajax(request, id):
    service = get_object_or_404(ServiceCabinet, id=id, cabinet=request.user.cabinet)
    if request.method == "POST":
        nom_service = request.POST.get("nom_service")
        service.nom_service= nom_service
        service.save()
        return JsonResponse({
            'success': True,
            'message': "Service modifié avec succès.",
            'row_html': f"""
                <tr id='poste{service.id}'>
                    <td>-</td>
                    <td>{service.nom_service}</td>
                    <td>{service.date_ajouter.strftime("%d/%m/%Y %H:%M")}</td>                   
                    <td class='text-center'>
                        <button class='btn btn-sm btn-warning btn-edit-ajax' data-row='service{service.id}' data-msg='msgServiceCabinet' data-url='/service/{service.id}/modifier/'>
                            <i class='mdi mdi-pencil'></i>
                        </button>
                        <button class='btn btn-sm btn-danger btn-delete-ajax' data-row='poste{service.id}' data-url='/service/{service.id}/supprimer/'>
                            <i class='mdi mdi-delete'></i>
                        </button>
                    </td>
                </tr>
            """
        })
    return JsonResponse({'success': False, 'message': "Méthode non autorisée."})


@login_required
def supprimer_service_cabinet_ajax(request, id):
    service = get_object_or_404(ServiceCabinet, id=id, cabinet=request.user.cabinet)
    service.delete()
    return JsonResponse({'success': True, 'message': "Service supprimé avec succès."})


# ===================== VILLES ======================

@login_required
def ajouter_ville_ajax(request):
    if request.method == "POST":
        nom_ville = request.POST.get("nom_ville")
        province = request.POST.get("province")
        cabinet = request.user.cabinet

        if Ville.objects.filter(nom_ville__iexact=nom_ville, province__iexact=province, cabinet=cabinet).exists():
            return JsonResponse({'success': False, 'message': "Cette ville existe déjà pour votre cabinet."})

        ville = Ville.objects.create(
            nom_ville=nom_ville,
            province=province,
            cabinet=cabinet
        )
        return JsonResponse({
            'success': True,
            'message': "Ville ajoutée avec succès.",
            'row': f"""
                <tr id='ville{ville.id}'>
                    <td>-</td>
                    <td>{ville.nom_ville}</td>
                    <td>{ville.province}</td>
                    <td class='text-center'>
                        <button class='btn btn-sm btn-warning btn-edit-ajax' data-row='ville{ville.id}' data-msg='msgVille' data-url='/ville/{ville.id}/modifier/'>
                            <i class='mdi mdi-pencil'></i>
                        </button>
                        <button class='btn btn-sm btn-danger btn-delete-ajax' data-row='ville{ville.id}' data-url='/ville/{ville.id}/supprimer/'>
                            <i class='mdi mdi-delete'></i>
                        </button>
                    </td>
                </tr>
            """
        })
    return JsonResponse({'success': False, 'message': "Requête invalide."})


@login_required
def modifier_ville_ajax(request, id):
    ville = get_object_or_404(Ville, id=id, cabinet=request.user.cabinet)
    if request.method == "POST":
        ville.nom_ville = request.POST.get("nom_ville")
        ville.province = request.POST.get("province")
        ville.save()
        return JsonResponse({
    'success': True,
    'message': "Ville modifiée avec succès.",
    'row_html': f"""
        <tr id='ville{ville.id}'>
            <td>-</td>
            <td>{ville.nom_ville}</td>
            <td>{ville.province}</td>
            <td class='text-center'>
                <button class='btn btn-sm btn-warning btn-edit-ajax' data-row='ville{ville.id}' data-msg='msgVille' data-url='/ville/{ville.id}/modifier/'>
                    <i class='mdi mdi-pencil'></i>
                </button>
                <button class='btn btn-sm btn-danger btn-delete-ajax' data-row='ville{ville.id}' data-url='/ville/{ville.id}/supprimer/'>
                    <i class='mdi mdi-delete'></i>
                </button>
            </td>
        </tr>
    """
})

    return JsonResponse({'success': False, 'message': "Méthode non autorisée."})


@login_required
def supprimer_ville_ajax(request, id):
    ville = get_object_or_404(Ville, id=id, cabinet=request.user.cabinet)
    ville.delete()
    return JsonResponse({'success': True, 'message': "Ville supprimée avec succès."})



# -------------------- JURIDICTION --------------------

@login_required(login_url='Connexion')
def ajouter_juridiction_ajax(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        lieu_id = request.POST.get('lieu_id')

        if not nom or not lieu_id:
            return JsonResponse({'success': False, 'message': 'Le nom et le lieu sont obligatoires.'})

        # Vérification d'unicité (nom pour le même cabinet)
        if Juridiction.objects.filter(nom__iexact=nom, cabinet=request.user.cabinet).exists():
            return JsonResponse({'success': False, 'message': 'Cette juridiction existe déjà !'})
        
        # Récupération de l'objet adresse
        try:
            lieu_obj = commune.objects.get(id=lieu_id)
        except commune.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Adresse (Lieu) invalide.'})

        # Création
        j = Juridiction.objects.create(nom=nom, lieu=lieu_obj, cabinet=request.user.cabinet)
        
        # Construction de la nouvelle ligne HTML pour la table
        row_html = f'''
        <tr id="juridiction{j.id}">
            <td>{j.id}</td>
            <td>{j.nom}</td>
            <td data-lieu-id="{j.lieu.id}"> {j.lieu.nom}</td>
            <td>{j.date_creation.strftime("%d/%m/%Y")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="juridiction{j.id}" data-msg="msgJuridiction"
                    data-url="{reverse('modifier_juridiction_ajax', args=[j.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="juridiction{j.id}" data-url="{reverse('supprimer_juridiction_ajax', args=[j.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''
        return JsonResponse({'success': True, 'row_html': row_html})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


@login_required(login_url='Connexion')
def modifier_juridiction_ajax(request, id):
    j = get_object_or_404(Juridiction, id=id, cabinet=request.user.cabinet)
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        lieu_id = request.POST.get('lieu_id')

        if not nom or not lieu_id:
            return JsonResponse({'success': False, 'message': 'Le nom et le lieu sont obligatoires.'})

        # Vérification d'unicité (nom pour le même cabinet, excluant l'objet courant)
        if Juridiction.objects.filter(nom__iexact=nom, cabinet=request.user.cabinet).exclude(id=j.id).exists():
            return JsonResponse({'success': False, 'message': 'Ce nom de juridiction existe déjà !'})
        
        # Récupération de l'objet adresse
        try:
            lieu_obj = commune.objects.get(id=lieu_id)
        except commune.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Adresse (Lieu) invalide.'})

        # Mise à jour
        j.nom = nom
        j.lieu = lieu_obj
        j.save()

        # Construction de la ligne HTML mise à jour
        row_html = f'''
        <tr id="juridiction{j.id}">
            <td>{j.id}</td>
            <td>{j.nom}</td>
            <td data-lieu-id="{j.lieu.id}"> {j.lieu.nom}</td>
            <td>{j.date_creation.strftime("%d/%m/%Y")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="juridiction{j.id}" data-msg="msgJuridiction"
                    data-url="{reverse('modifier_juridiction_ajax', args=[j.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="juridiction{j.id}" data-url="{reverse('supprimer_juridiction_ajax', args=[j.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''
        return JsonResponse({'success': True, 'row_html': row_html})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


@login_required(login_url='Connexion')
def supprimer_juridiction_ajax(request, id):
    j = get_object_or_404(Juridiction, id=id, cabinet=request.user.cabinet)
    j.delete()
    return JsonResponse({'success': True, 'id': id})


# -------------------- TYPE DE PIECE (TypePiece) --------------------

@login_required(login_url='Connexion')
def ajouter_type_piece_ajax(request):
    if request.method == 'POST':
        nom_type = request.POST.get('nom_type', '').strip()

        if not nom_type:
            return JsonResponse({'success': False, 'message': 'Le nom du type de pièce est obligatoire.'})

        if TypePiece.objects.filter(nom_type__iexact=nom_type, cabinet=request.user.cabinet).exists():
            return JsonResponse({'success': False, 'message': 'Ce type de pièce existe déjà !'})

        tp = TypePiece.objects.create(nom_type=nom_type, cabinet=request.user.cabinet)

        row_html = f'''
        <tr id="typePiece{tp.id}">
            <td>{tp.id}</td>
            <td>{tp.nom_type}</td>
            <td>{tp.date_ajout.strftime("%d/%m/%Y")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="typePiece{tp.id}" data-msg="msgTypePiece"
                    data-url="{reverse('modifier_type_piece_ajax', args=[tp.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="typePiece{tp.id}" data-url="{reverse('supprimer_type_piece_ajax', args=[tp.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''
        return JsonResponse({'success': True, 'row_html': row_html})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


@login_required(login_url='Connexion')
def modifier_type_piece_ajax(request, id):
    tp = get_object_or_404(TypePiece, id=id, cabinet=request.user.cabinet)
    if request.method == 'POST':
        nom_type = request.POST.get('nom_type', '').strip()

        if not nom_type:
            return JsonResponse({'success': False, 'message': 'Le nom du type de pièce est obligatoire.'})

        if TypePiece.objects.filter(nom_type__iexact=nom_type, cabinet=request.user.cabinet).exclude(id=tp.id).exists():
            return JsonResponse({'success': False, 'message': 'Ce nom de type de pièce existe déjà !'})

        tp.nom_type = nom_type
        tp.save()

        row_html = f'''
        <tr id="typePiece{tp.id}">
            <td>{tp.id}</td>
            <td>{tp.nom_type}</td>
            <td>{tp.date_ajout.strftime("%d/%m/%Y")}</td>
            <td class="text-center">
                <button class="btn btn-sm btn-warning btn-edit-ajax"
                    data-row="typePiece{tp.id}" data-msg="msgTypePiece"
                    data-url="{reverse('modifier_type_piece_ajax', args=[tp.id])}"><i class="mdi mdi-pencil"></i></button>
                <button class="btn btn-sm btn-danger btn-delete-ajax"
                    data-row="typePiece{tp.id}" data-url="{reverse('supprimer_type_piece_ajax', args=[tp.id])}"><i class="mdi mdi-delete"></i></button>
            </td>
        </tr>
        '''
        return JsonResponse({'success': True, 'row_html': row_html})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


@login_required(login_url='Connexion')
def supprimer_type_piece_ajax(request, id):
    tp = get_object_or_404(TypePiece, id=id, cabinet=request.user.cabinet)
    tp.delete()
    return JsonResponse({'success': True, 'id': id})


#----------------------------taux-----------------------------
from django.db.models import F, DecimalField, ExpressionWrapper
@login_required(login_url='Connexion')
def ajouter_taux_ajax(request):
    if request.method == "POST":
        cout = request.POST.get("cout")
        

        try:
            cout_decimal = Decimal(cout)
        except:
            return JsonResponse({"success": False, "message": "Valeur du taux invalide."})

        # Enregistrement du taux
        new_taux = taux.objects.create(
            cout=cout_decimal,
            cabinet=request.user.cabinet
        )
        
        # Mise à jour automatique des tarifs existants
        TarifHoraire.objects.filter(cabinet=request.user.cabinet).update(
                 taux_jour=cout_decimal,
                 montant_fc=ExpressionWrapper( F('montant_dollars') * cout_decimal,output_field=DecimalField() )
         )
        # Construction de la ligne HTML
        row_html = f"""
        <tr id='taux{new_taux.id}' style="background-color:green;">
            <td>{new_taux.id}</td>
            <td>{new_taux.cout}</td>
            <td>{new_taux.date_ajouter.strftime('%d/%m/%Y')}</td>
        </tr>
        """

        return JsonResponse({"success": True, "message": "Taux ajouté avec succès.", "row_html": row_html})

    return JsonResponse({"success": False, "message": "Méthode non autorisée."})



def supprimer_taux_ajax(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=400)

    taux_obj = get_object_or_404(taux, id=id,cabinet=request.user.cabinet)

    # Tu peux ajouter une condition ici pour empêcher de supprimer le dernier taux utilisé
    # Par exemple :
    # if taux.objects.count() <= 1:
    #     return JsonResponse({"error": "Impossible de supprimer tous les taux."}, status=400)

    taux_obj.delete()

    return JsonResponse({'success': True, 'id': id})



def ajouter_banque_ajax(request):
    if request.method == "POST":
        nom = request.POST.get("nom_banque")
        numero = request.POST.get("numero_compte")

        if Banque.objects.filter(nom_banque__iexact=nom, cabinet=request.user.cabinet).exists():
            return JsonResponse({"status": "error", "message": "Cette banque existe déjà."})

        b = Banque.objects.create(
            nom_banque=nom,
            numero_compte=numero
        )

        return JsonResponse({
            "success": True,
            "row_html": f"""
                <tr id='banque{b.id}'  style="background-color:green;">
                    <td>NEW</td>
                    <td>{b.nom_banque}</td>
                    <td>{b.numero_compte}</td>
                    <td class="text-center">
                        <button class="btn btn-sm btn-danger btn-delete-ajax"
                                data-row="banque{b.id}"
                                data-url="/banque/supprimer/{b.id}/">
                            <i class="mdi mdi-delete"></i>
                        </button>
                    </td>
                </tr>
            """,
             "message": "Taux ajouté avec succès."
        })
   


def supprimer_banque_ajax(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=400)

    banque = get_object_or_404(Banque, id=id)
    banque.delete()

    return JsonResponse({'success': True, 'id': id})

