from django.shortcuts import render, redirect,get_object_or_404
from django.db import transaction
from django.contrib import messages
from .forms import ClientForm 
from .models import client, adresse,PieceDossier, dossier, AvocatDossier,DeclarationDossier
from Agent.models import PieceJustificative
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import dossier, Cabinet, SecteurFoncier,type_dossier,TarifHoraire,TypePiece,ReductionTarifForfaitaire,TarifActivite
from .forms import DossierForm, ModeHonoraireForm
import datetime
from django.http import JsonResponse
from Agent.models import agent
from Adresse.models import commune, Ville   
from Structure.models import Cabinet, Juridiction
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.db.models import Prefetch
from paiement.models import Paiement
from django.db.models import Sum
from django.urls import reverse


@login_required(login_url='Connexion')# Il est bon de s'assurer que l'utilisateur est connecté
def enregistrer_nouveau_client(request):
    client_form = ClientForm()
    is_modal_active = False
    pieces_post = []

    types_pieces = TypePiece.objects.all()

    if request.method == 'POST':
        client_form = ClientForm(request.POST, request.FILES)

        numeros = request.POST.getlist('numero_piece[]')
        type_ids = request.POST.getlist('type_piece[]')
        fichiers = request.FILES.getlist('fichier_piece[]')

        # Préparer pieces_post avec les instances TypePiece
        for n, tid in zip(numeros, type_ids):
            type_instance = TypePiece.objects.filter(id=tid).first()
            pieces_post.append({
                'numero': n,
                'type_piece': type_instance
            })

        if client_form.is_valid():
            try:
                with transaction.atomic():
                    nouvelle_adresse = adresse.objects.create(
                        numero=request.POST.get('numero', ''),
                        avenue=request.POST.get('avenue', ''),
                        quartier=request.POST.get('quartier', ''),
                        commune=request.POST.get('commune', ''),
                        ville=request.POST.get('ville', '')
                    )

                    client_instance = client_form.save(commit=False)
                    client_instance.adresse = nouvelle_adresse
                    if 'photo' in request.FILES:
                        client_instance.photo = request.FILES['photo']
                    client_instance.cabinet = getattr(request.user, 'cabinet', Cabinet.objects.first()) 
                    client_instance.save()

                    for n, tid, f in zip(numeros, type_ids, fichiers):
                        if tid and f:
                            type_piece_instance = TypePiece.objects.get(id=tid) 
                            PieceJustificative.objects.create(
                                client=client_instance,
                                type_piece=type_piece_instance,
                                numero_piece=n,
                                fichier=f
                            )

                    messages.success(
                        request,
                        f"Le client {client_instance.prenom} {client_instance.nom} a été enregistré avec succès ✅"
                    )
                    return redirect('client_details', client_id=client_instance.id)

            except Exception as e:
                messages.error(request, f"Erreur critique lors de la transaction : {e} ❌")
                is_modal_active = True
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire ⚠️")
            is_modal_active = True

    clients = client.objects.filter(cabinet=getattr(request.user, 'cabinet', None)) if request.user.is_authenticated else client.objects.none()
    
    context = {
        'clients': clients,
        'client_form': client_form,
        'is_modal_active': is_modal_active,
        'pieces_post': pieces_post,
        'types_pieces': types_pieces
    }

    return render(request, 'admin_template/cases.html', context)


@login_required(login_url='Connexion')
def details_client(request, client_id): 
    client_instance = get_object_or_404(
        client, 
        pk=client_id, 
        cabinet=request.user.cabinet 
    )    
    # Vous pouvez aussi récupérer ici les affaires, les documents, etc., liés à cet agent.   
    context = {
        'client': client_instance,
        # Ajoutez d'autres données nécessaires, ex: 'affaires_traitees': agent_instance.affaires.all()
    }
    
    return render(request, "admin_template/case_details - 1.html", context)


#Vue pour mettre à jour les information du client
@login_required(login_url='Connexion')
def profil_client(request, client_id):
    client_instance = get_object_or_404(client, id=client_id)

    # Récupération des communes et villes du cabinet de l'utilisateur
    user_cabinet = request.user.cabinet
    communes = commune.objects.filter(cabinet=user_cabinet)
    villes = Ville.objects.filter(cabinet=user_cabinet)

    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES, instance=client_instance)
        if form.is_valid():
            try:
                with transaction.atomic():
                    client_obj = form.save(commit=False)

                    # Adresse
                    addr = client_obj.adresse
                    addr.numero = request.POST.get("numero", addr.numero)
                    addr.avenue = request.POST.get("avenue", addr.avenue)
                    addr.quartier = request.POST.get("quartier", addr.quartier)
                    addr.commune = request.POST.get("commune", addr.commune)
                    addr.ville = request.POST.get("ville", addr.ville)
                    addr.save()

                    

                    client_obj.save()
                    messages.success(request, "Profil mis à jour avec succès ✅")
                    return redirect("client_details", client_id=client_instance.id)
            except Exception as e:
                messages.error(request, f"Erreur lors de la mise à jour : {e} ❌")
        else:
            messages.error(request, "Formulaire invalide, veuillez vérifier les informations ⚠️")
    else:
        form = ClientForm(instance=client_instance)

    context = {
        "client": client_instance,
        "form": form,
        "communes": communes,
        "villes": villes,
    }
    return render(request, "admin_template/case_details - 1.html", context)


@login_required(login_url='Connexion')
def update_client_photo(request, client_id):
    """
    Vue dédiée à la mise à jour de la photo de profil d’un client.
    """
    client_instance = get_object_or_404(client, id=client_id)

    if request.method == "POST" and 'photo' in request.FILES:
        try:
            with transaction.atomic():
                # Supprime l'ancienne photo si elle existe (facultatif)
                if client_instance.photo:
                    client_instance.photo.delete(save=False)
                
                client_instance.photo = request.FILES['photo']
                client_instance.save()
                messages.success(request, "Photo de profil mise à jour avec succès ✅")
        except Exception as e:
            messages.error(request, f"Erreur lors de la mise à jour de la photo : {e} ❌")
    else:
        messages.warning(request, "Aucune photo sélectionnée ⚠️")

    # Redirige vers la page de profil après la mise à jour
    return redirect("client_details", client_id=client_instance.id)


@login_required(login_url='Connexion')
def affaires_interface(request):
    user_cabinet = request.user.cabinet
    dossiers = dossier.objects.filter(cabinet=user_cabinet).select_related('client', 'type_affaire')
    form = DossierForm()

    # Numéro temporaire
    numero_temp = dossier.generer_numero_dossier(
        cabinet=user_cabinet,
        client_id=0  # Client non encore choisi
    )

    if request.method == "POST":
        form = DossierForm(request.POST)
        if form.is_valid():
            dossier_instance = form.save(commit=False)
            dossier_instance.cabinet = user_cabinet

            # Générer numéro final
            dossier_instance.numero_reference_dossier = dossier.generer_numero_dossier(
                cabinet=user_cabinet,
                client_id=form.cleaned_data['client'].id
            )

            # Récupérer le tarif
            try:
                tarif = TarifHoraire.objects.get(
                    cabinet=user_cabinet,
                    type_dossier=form.cleaned_data['type_affaire'],
                    secteur=form.cleaned_data['secteur_foncier']
                )

                # Sauvegarde des valeurs du tarif au moment de l'enregistrement
                dossier_instance.tarif_reference = tarif
                dossier_instance.montant_dollars_enreg = tarif.montant_dollars
                dossier_instance.montant_fc_enreg = tarif.montant_fc
                dossier_instance.taux_enreg = tarif.taux_jour

            except TarifHoraire.DoesNotExist:
                # Aucun tarif trouvé pour cette combinaison
                dossier_instance.tarif_reference = None

            dossier_instance.save()
            form.save_m2m()

            return redirect('Dossier_interfaces')
        else:
            print(form.errors)

    context = {
        'form': form,
        'dossiers': dossiers,
        'clients': client.objects.filter(cabinet=user_cabinet),
        'types_affaire': type_dossier.objects.all(),
        'secteurs': SecteurFoncier.objects.all(),
        'numero_temp': numero_temp,
    }
    return render(request, 'admin_template/dossiers.html', context)



@login_required(login_url='Connexion')
def details_affaire(request, dossier_id):
    
    # 1. Requête principale OPTIMISÉE pour récupérer le dossier et toutes ses relations
    # Ceci remplace la requête simple `dossier.objects.get(...)`
    # On précharge: client, type_affaire, secteur_foncier, tarif_reference, pieces_dossier, avocatdossier_set
    dossier_instance = get_object_or_404(
        dossier.objects
            .select_related('client', 'type_affaire', 'secteur_foncier', 'tarif_reference')
            .prefetch_related(
                'pieces_dossier',
                'avocatdossier_set__avocat' 
            ),
        pk=dossier_id, 
        cabinet=request.user.cabinet 
    ) 
    doss = get_object_or_404(dossier, id=dossier_id)

    paiements = doss.paiements.all().order_by('-date_paiement')
    # Autres données pour la page principale (non modale)
    # Précharger les spécialités dans les agents disponibles
    agents_disponibles = agent.objects.filter(poste__icontains='avocat').select_related('specialite')
    form_mode = ModeHonoraireForm(
        instance=dossier_instance, 
        dossier_instance=dossier_instance 
    ) 
    paiements_dossier = Paiement.objects.filter(dossier=dossier_id)
    # -------------------------------------------------------------------------
    # 2. LOGIQUE COMPLÈTE DU FORFAIT ET DES ACTIVITÉS (Optimisée)
    # -------------------------------------------------------------------------
    
    # Préparez la précharge pour les réductions (Requête N+1 éliminée)
    # Cela charge TOUTES les réductions liées à ce dossier en 1 seule requête.
    reductions_pour_dossier = ReductionTarifForfaitaire.objects.filter(
        dossier=dossier_instance
    ).select_related('activite')

    # Crée un dictionnaire pour un accès rapide O(1) par ID d'activité (TarifActivite)
    reductions_dict = {
        reduction.activite_id: reduction 
        for reduction in reductions_pour_dossier
    }
    
    # a. Récupération des activités - OPTIMISÉE pour charger la table 'activite'
    if dossier_instance.tarif_reference:
        activites = TarifActivite.objects.filter(tarif=dossier_instance.tarif_reference).select_related('activite')
    else:
        activites = TarifActivite.objects.none()
    
    # b. Récupération du taux (TAUX_FC)
    tarif_horaire = TarifHoraire.objects.filter(
        type_dossier=dossier_instance.type_affaire,
        secteur=dossier_instance.secteur_foncier
    ).first()
    
    taux_fc_value = dossier_instance.taux_enreg if tarif_horaire and dossier_instance.taux_enreg is not None else Decimal('00.00')
    try:
        taux_fc = Decimal(str(taux_fc_value))
    except:
        taux_fc = Decimal('2800.00') # Fallback sûr
    
    # c. Conditions d'affichage et d'édition
    editable = dossier_instance.mode_honoraire == "Forfait" and not dossier_instance.forfait_defini
    forfait_defini = dossier_instance.mode_honoraire == "Forfait" and dossier_instance.forfait_defini

    # d. Calculs et Application des réductions
    total_dollars = Decimal('0.00')
    total_fc = Decimal('0.00')
    
    for act in activites:
        prix_dollars_base = act.prix_dollars if act.prix_dollars is not None else Decimal('0.00')
        act.prix_fc_calcule = prix_dollars_base * taux_fc

        # Initialisation avec les prix de base
        act.prix_affiche_dollars = prix_dollars_base
        act.prix_affiche_fc = act.prix_fc_calcule
        act.prix_fc_defaut = prix_dollars_base * taux_fc

        # Logique de prix réduit si le forfait est déjà défini (Accès O(1) au dictionnaire)
        if forfait_defini:
            # act.id est l'ID de l'instance TarifActivite (qui est la clé dans le dictionnaire)
            reduction = reductions_dict.get(act.id)
            
            if reduction:
                # Applique la réduction si elle existe
                act.prix_affiche_dollars = reduction.prix_reduit_dollars if reduction.prix_reduit_dollars is not None else prix_dollars_base
                act.prix_affiche_fc = reduction.prix_reduit_fc if reduction.prix_reduit_fc is not None else act.prix_fc_calcule
        
        # Calcul des totaux (utilise toujours les prix affichés)
        total_dollars += act.prix_affiche_dollars
        total_fc += act.prix_affiche_fc
       
    
    # -------------------------------------------------------------------------
    # 3. Contexte Final
    # -------------------------------------------------------------------------
    montant_deja_paye = paiements_dossier.filter(devise="USD").aggregate(Sum("montant"))["montant__sum"] or 0
    montant_deja_paye_fc = paiements_dossier.filter(devise="FC").aggregate(Sum("montant"))["montant__sum"] or 0
    reste_a_payer = total_dollars - montant_deja_paye
    reste_a_payer_fc = total_fc- montant_deja_paye_fc
    taux_du_jour=tarif_horaire.taux_jour
    
    context = {
        # Contexte page principale
        'dossier': dossier_instance,
        'agents': agents_disponibles,
        'form_mode': form_mode, 
        
        # Contexte MODALE (Toutes les variables requises)
        'activites': activites,
        'total_dollars': total_dollars,
        'total_fc': total_fc,
        'editable': editable, 
        'forfait_defini': forfait_defini, 
        'taux_fc': taux_fc,
        'paiements': paiements,
        'montant_deja_paye':montant_deja_paye,
        'montant_deja_paye_fc':montant_deja_paye_fc,
        'reste_a_payer':reste_a_payer,
        'reste_a_payer_fc':reste_a_payer_fc,
        'taux_du_jour':taux_du_jour,
        
    }
        # Mode impression
    if request.GET.get("print") == "facture":
        return render(request, "facture_template/factures_historique.html", context)

    return render(request, "admin_template/dossier_details.html", context)



@login_required
def ajouter_declaration(request, dossier_id):
    dossier_instance = get_object_or_404(dossier, pk=dossier_id, cabinet=request.user.cabinet)

    if request.method == "POST":
        contenu = request.POST.get("contenu")

        if contenu and contenu.strip() != "":
            DeclarationDossier.objects.create(
                dossier=dossier_instance,
                contenu=contenu,
                auteur=request.user.agent
            )

        return redirect("dossier_details", dossier_id=dossier_id)


@login_required
def modifier_declaration(request, decl_id):
    declaration = get_object_or_404(DeclarationDossier, pk=decl_id, dossier__cabinet=request.user.cabinet)

    if request.method == "POST":
        contenu = request.POST.get("contenu")
        if contenu:
            declaration.contenu = contenu
            declaration.save()
        return redirect("dossier_details", dossier_id=declaration.dossier.id)

@login_required
def supprimer_declaration(request, decl_id):
    declaration = get_object_or_404(DeclarationDossier, pk=decl_id, dossier__cabinet=request.user.cabinet)
    dossier_id = declaration.dossier.id
    declaration.delete()
    return redirect("dossier_details", dossier_id=dossier_id)


#Pour enregistrer les document lié à un dossier

@login_required(login_url='Connexion')
def ajouter_pieces(request, dossier_id):
    # Récupération du dossier lié au cabinet de l'utilisateur
    dossier_instance = get_object_or_404(dossier, pk=dossier_id, cabinet=request.user.cabinet)

    if request.method == 'POST':
        titres = request.POST.getlist('titre_piece[]')
        fichiers = request.FILES.getlist('fichier_piece[]')
        formats = request.POST.getlist('format_piece[]')

        # Vérification que tout est renseigné
        if not titres or not fichiers or not formats or len(titres) != len(fichiers) or len(titres) != len(formats):
           # Ligne 1 : On affiche l'erreur dans la console (pour vous, le développeur)
            print(f"DEBUG ERROR: Titres: {len(titres)}, Fichiers: {len(fichiers)}, Formats: {len(formats)}")
            
            # Ligne 2 : On envoie le message à l'utilisateur
            messages.error(request, "Erreur : assurez-vous d'avoir rempli tous les titres, formats et fichiers correctement.")
            return redirect('dossier_details', dossier_id=dossier_id)

        for titre, fichier, format_piece in zip(titres, fichiers, formats):
            # Optionnel : vérifier la taille côté serveur
            if fichier.size > 200 * 1024 * 1024:
                messages.error(request, f"Le fichier {titre} dépasse la limite de 200 Mo.")
                continue

            PieceDossier.objects.create(
                dossier=dossier_instance,
                titre=titre,
                fichier=fichier,
                format_fichier=format_piece,
                ajoute_par=request.user.agent if hasattr(request.user, 'agent') else 'Administrateur'
            )

        messages.success(request, "Les documents ont été ajoutés avec succès !")
        return redirect('dossier_details', dossier_id=dossier_id)

    # Si GET
    messages.warning(request, "Accès direct à la page non autorisé.")
    return redirect('dossier_details', dossier_id=dossier_id)


@login_required(login_url='Connexion')
def supprimer_piece(request, piece_id):
    piece = get_object_or_404(PieceDossier, pk=piece_id)
    dossier_id = piece.dossier.id

    # Vérifie que l'utilisateur a le droit de supprimer
    if request.user.is_authenticated and hasattr(request.user, 'agent'):
        if request.method == 'POST':
            piece.fichier.delete(save=False)  # supprime le fichier du storage
            piece.delete()
            messages.success(request, "Document supprimé avec succès !")
            return redirect('dossier_details', dossier_id=dossier_id)

    messages.error(request, "Vous n'avez pas le droit de supprimer ce document.")
    return redirect('dossier_details', dossier_id=dossier_id)



@login_required(login_url='Connexion')
def assigner_avocats_dossier(request, dossier_id):
    dossier_instance = get_object_or_404(dossier, id=dossier_id)
    
    # ⚡ On ne prend que les agents dont le poste est "Avocat"
    agents_disponibles = agent.objects.filter(poste='Avocat',company=request.user.cabinet).select_related('specialite')

    if request.method == "POST":
        avocats_ids = request.POST.getlist('avocats_ids[]')
        roles = request.POST.getlist('roles[]')

        if not avocats_ids:
            messages.warning(request, "Veuillez sélectionner au moins un avocat.")
            return redirect('dossier_details', dossier_id=dossier_id)

        for avocat_id, role in zip(avocats_ids, roles):
            avocat_instance = agent.objects.filter(id=avocat_id).first()
            if avocat_instance:
                AvocatDossier.objects.update_or_create(
                    dossier=dossier_instance,
                    avocat=avocat_instance,
                    defaults={'role': role}
                )

        messages.success(request, "Les avocats ont été assignés avec succès.")
        return redirect('dossier_details', dossier_id=dossier_id)

    context = {
        'dossier': dossier_instance,
        'agents': agents_disponibles,
    }
    return render(request, 'admin_template/dossier_details.html', context)



@login_required(login_url='Connexion')
def supprimer_avocat_dossier(request, avocat_dossier_id):
    try:
        avocat_dossier = get_object_or_404(AvocatDossier, id=avocat_dossier_id)
        avocat_dossier.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        print("Erreur suppression avocat:", e)
        return JsonResponse({"success": False, "error": str(e)})


@login_required(login_url='Connexion')
def definir_mode_honoraire(request, dossier_id):
    dossier_instance = get_object_or_404(dossier, id=dossier_id)

    if request.method == 'POST':
        form = ModeHonoraireForm(request.POST, dossier_instance=dossier_instance)
        if form.is_valid():
            mode = form.cleaned_data['mode_honoraire']
            dossier_instance.mode_honoraire = mode

            # Si mode = Forfait → les prix doivent être définis
            dossier_instance.forfait_defini = False if mode == "Forfait"  else True
            dossier_instance.mode_defini =True

            dossier_instance.save()
            messages.success(request, "Le mode d'honoraire a été mis à jour avec succès.")

            # Redirection vers détails pour recharger l'état
             # Redirection vers la page détails + paramètre pour ouvrir le modal
            url = reverse('dossier_details', args=[dossier_instance.id])
            return redirect(f"{url}?open_modal=activites")

    else:
        form = ModeHonoraireForm(instance=dossier_instance, dossier_instance=dossier_instance)
    
    return render(request, 'admin_template/dossier_details.html', {
        'form_mode': form,
        'dossier': dossier_instance
    })



@login_required(login_url='Connexion')
def enregistrer_prix_forfaitaire(request, dossier_id):
    dossier_instance = get_object_or_404(dossier, id=dossier_id)

    if request.method != "POST":
        return redirect("dossier_details", dossier_id=dossier_id)

    # Récupération du taux basé sur le type + secteur
    tarif = TarifHoraire.objects.filter(
        type_dossier=dossier_instance.type_affaire,
        secteur=dossier_instance.secteur_foncier
    ).first()

    taux_fc = dossier_instance.taux_enreg if tarif else 0  

    # Toutes les activités du dossier
    activites = TarifActivite.objects.filter(tarif=dossier_instance.tarif_reference)

    for act in activites:
        key = f"prix_dollars_{act.id}"
        if key in request.POST:
            try:
                prix_dollar = float(request.POST[key])
            except ValueError:
                prix_dollar = 0

            prix_fc = prix_dollar * float(taux_fc)

            # Enregistrement dans ReductionTarifForfaitaire
            reduction, created = ReductionTarifForfaitaire.objects.get_or_create(
                dossier=dossier_instance,
                activite=act,
                defaults={'prix_reduit_dollars': prix_dollar, 'prix_reduit_fc': prix_fc}
            )

            if not created:
                reduction.prix_reduit_dollars = prix_dollar
                reduction.prix_reduit_fc = prix_fc
                reduction.save()

    # Marquer que tous les prix ont été définis
    dossier_instance.forfait_defini = True
    
    dossier_instance.save()

    messages.success(request, "Les prix forfaitaires ont été enregistrés avec succès.")
    return redirect("dossier_details", dossier_id=dossier_id)





