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
from parametre.models import taux
import requests
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum
import base64
import os
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone


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

            dossier_instance.save()
            now = datetime.now()
            reference = f"FACT-{dossier_instance.id}-{now.strftime('%Y%m%d%H%M%S')}"
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
                dossier_instance.reference=reference

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
    montant_deja_paye =paiements.aggregate(Sum("montant_payer_dollars"))["montant_payer_dollars__sum"] or 0

    montant_deja_paye_fc = paiements.aggregate(Sum("montant_payer_fc"))["montant_payer_fc__sum"] or 0
      
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
        auteur=request.POST.get("auteur")

        if auteur == '':
            auteur= f'{dossier_instance.client.nom} (client)'

        if contenu and contenu.strip() != "":
            declaration = DeclarationDossier.objects.create(
                dossier=dossier_instance,
                contenu=contenu,
                auteur=auteur,
                ecrit_par=request.user.agent
            )
            
            # Log de l'activité
            try:
                from Agent.models_activity import ActivityLogManager
                ActivityLogManager.log_declaration_added(request.user, declaration, request)
            except Exception as e:
                print(f"Erreur lors du logging de l'ajout de déclaration: {e}")

        return redirect("dossier_details", dossier_id=dossier_id)


@login_required
def modifier_declaration(request, decl_id):
    declaration = get_object_or_404(DeclarationDossier, pk=decl_id, dossier__cabinet=request.user.cabinet)

    if request.method == "POST":
        contenu = request.POST.get("contenu")
        if contenu:
            declaration.contenu = contenu
            declaration.save()
            
            # Log de l'activité
            try:
                from Agent.models_activity import ActivityLogManager
                ActivityLogManager.log_declaration_updated(request.user, declaration, request)
            except Exception as e:
                print(f"Erreur lors du logging de la modification de déclaration: {e}")
                
        return redirect("dossier_details", dossier_id=declaration.dossier.id)

@login_required
def supprimer_declaration(request, decl_id):
    declaration = get_object_or_404(DeclarationDossier, pk=decl_id, dossier__cabinet=request.user.cabinet)
    dossier_id = declaration.dossier.id
    
    # Log de l'activité avant suppression
    try:
        from Agent.models_activity import ActivityLog
        ActivityLog.log_activity(
            user=request.user,
            action='delete',
            entity_type='declaration',
            title='Déclaration supprimée',
            description=f'Dossier {declaration.dossier.numero_reference_dossier}',
            request=request,
            dossier_id=declaration.dossier.id
        )
    except Exception as e:
        print(f"Erreur lors du logging de la suppression de déclaration: {e}")
    
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

            document = PieceDossier.objects.create(
                dossier=dossier_instance,
                titre=titre,
                fichier=fichier,
                format_fichier=format_piece,
                ajoute_par=request.user.agent if hasattr(request.user, 'agent') else 'Administrateur'
            )
            
            # Log de l'activité
            try:
                from Agent.models_activity import ActivityLogManager
                ActivityLogManager.log_document_added(request.user, document, dossier_instance, request)
            except Exception as e:
                print(f"Erreur lors du logging de l'ajout de document: {e}")

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
            # Log de l'activité avant suppression
            try:
                from Agent.models_activity import ActivityLogManager
                ActivityLogManager.log_document_deleted(request.user, piece.titre, piece.dossier, request)
            except Exception as e:
                print(f"Erreur lors du logging de la suppression de document: {e}")
            
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

            # 👉 Si l'utilisateur choisit "Forfait", remettre les montants à 0
            if mode == "Forfait":
                dossier_instance.montant_dollars_enreg = 0.0
                dossier_instance.montant_fc_enreg = 0.0
                dossier_instance.forfait_defini = False
            else:
                dossier_instance.forfait_defini = True

            dossier_instance.mode_defini = True
            dossier_instance.save()

            messages.success(request, "Le mode d'honoraire a été mis à jour avec succès.")

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
    
    t = taux.objects.filter(cabinet=request.user.cabinet).order_by('-date_ajouter').first()
    if not t:
        messages.error(request, "Aucun taux de change n'est défini pour ce cabinet.")
        return redirect('dossier_details', dossier_id=dossier_id)

    taux_fc = float(t.cout)
    

    # Toutes les activités du dossier
    activites = TarifActivite.objects.filter(tarif=dossier_instance.tarif_reference)

    total_dollars = 0.0
    total_fc = 0.0

    for act in activites:
        key = f"prix_dollars_{act.id}"
        if key in request.POST:
            try:
                prix_dollar = float(request.POST[key])
            except ValueError:
                prix_dollar = 0

            prix_fc = prix_dollar * float(taux_fc)

            # Ajouter au total
            total_dollars += prix_dollar
            total_fc += prix_fc

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

    # Mettre à jour les montants totaux du dossier
    dossier_instance.montant_dollars_enreg = total_dollars
    dossier_instance.montant_fc_enreg = total_fc
    dossier_instance.taux_enreg = taux_fc
    dossier_instance.forfait_defini = True
    dossier_instance.save()

    messages.success(request, "Les prix forfaitaires ont été enregistrés avec succès.")
    return redirect("dossier_details", dossier_id=dossier_id)



@login_required(login_url='Connexion')
def extrait_compte_preview(request, dossier_id):
    doss = get_object_or_404(dossier, pk=dossier_id, cabinet=request.user.cabinet)

    date_debut = request.GET.get("date_debut")
    date_fin = request.GET.get("date_fin")
    devise = request.GET.get("devise", "USD")

    paiements = doss.paiements.all()

    # Filtrage correct des dates : inclure toute la journée de date_fin
    if date_debut and date_fin:
        date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d")
        date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d")

        # Ajouter 1 jour à la date de fin pour inclure TOUTE la journée
        date_fin_plus_un = date_fin_obj + timedelta(days=1)

        paiements = paiements.filter(
            date_paiement__gte=date_debut_obj,
            date_paiement__lt=date_fin_plus_un
        )

    # Calcul des totaux selon la devise
    if devise == "USD":
        total_paye = paiements.aggregate(Sum("montant_payer_dollars"))["montant_payer_dollars__sum"] or 0
        reste_a_payer = doss.montant_dollars_enreg - total_paye
    else:
        total_paye = paiements.aggregate(Sum("montant_payer_fc"))["montant_payer_fc__sum"] or 0
        reste_a_payer = doss.montant_fc_enreg - total_paye

    context = {
        "dossier": doss,
        "paiements": paiements.order_by('date_paiement'),
        "date_debut": date_debut,
        "date_fin": date_fin,
        "devise": devise,
        "total_paye": total_paye,
        "reste_a_payer": reste_a_payer,
    }

    return render(request, "admin_template/extrait_preview.html", context)


@login_required(login_url='Connexion')
def extrait_compte_date_form(request, dossier_id):
    return render(request, "admin_template/extrait_compte_date_form.html", {"dossier_id": dossier_id})



@login_required(login_url='Connexion')
def imprimer_paiements(request, dossier_id):
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Récupérer le dossier avec relations
    doss = get_object_or_404(
        dossier.objects.select_related(
            'client', 'type_affaire', 'secteur_foncier', 'tarif_reference', 'cabinet'
        ).prefetch_related('paiements', 'pieces_dossier', 'avocatdossier_set__avocat'),
        pk=dossier_id,
        cabinet=request.user.cabinet
    )

    # Paramètres GET
    date_debut = request.GET.get("date_debut")
    date_fin = request.GET.get("date_fin")
    devise = request.GET.get("devise", "USD").upper()  # Devise par défaut USD

    # Paiements filtrés
    paiements = doss.paiements.all().order_by("date_paiement")
    if date_debut and date_fin:
        date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d').date() + timedelta(days=1)
        paiements = paiements.filter(date_paiement__gte=date_debut, date_paiement__lt=date_fin_obj)

    # Logo du cabinet
    logo_url = ""
    if doss.cabinet.logo:
        with doss.cabinet.logo.open("rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_url = f"data:image/png;base64,{logo_base64}"

    # Activités et réductions
    reductions_dict = {r.activite_id: r for r in ReductionTarifForfaitaire.objects.filter(dossier=doss)}
    activites = TarifActivite.objects.filter(tarif=doss.tarif_reference).select_related('activite') if doss.tarif_reference else []
    tarif_horaire = TarifHoraire.objects.filter(type_dossier=doss.type_affaire, secteur=doss.secteur_foncier).first()
    taux_fc = float(doss.taux_enreg or 2800.0)

    total_dollars = 0.0
    total_fc = 0.0
    activites_list = []
    forfait_defini = doss.mode_honoraire == "Forfait" and doss.forfait_defini

    for act in activites:
        prix_dollars_base = float(act.prix_dollars or 0)
        prix_fc_calcule = prix_dollars_base * taux_fc

        prix_affiche_dollars = prix_dollars_base
        prix_affiche_fc = prix_fc_calcule

        if forfait_defini:
            reduction = reductions_dict.get(act.id)
            if reduction:
                prix_affiche_dollars = float(reduction.prix_reduit_dollars or prix_dollars_base)
                prix_affiche_fc = float(reduction.prix_reduit_fc or prix_fc_calcule)

        total_dollars += prix_affiche_dollars
        total_fc += prix_affiche_fc

        activites_list.append({
            "nom": act.activite.nom_activite if act.activite else "",
            "prix_affiche": prix_affiche_dollars if devise == "USD" else prix_affiche_fc
        })

    # Calcul total payé et reste
    if devise == "USD":
        total_paye = float(paiements.aggregate(Sum("montant_payer_dollars"))["montant_payer_dollars__sum"] or 0)
        dernier_paiement = paiements.last()
        reste = float(dernier_paiement.montant_reste_dollars) if dernier_paiement else 0
    else:
        total_paye = float(paiements.aggregate(Sum("montant_payer_fc"))["montant_payer_fc__sum"] or 0)
        dernier_paiement = paiements.last()
        reste = float(dernier_paiement.montant_reste_fc) if dernier_paiement else 0

    taux_du_jour = float(tarif_horaire.taux_jour) if tarif_horaire else 0.0

   

    # Préparer données pour jsreport
    dossier_data = {
        "numero_reference_dossier": doss.numero_reference_dossier,
        "type_affaire": doss.type_affaire.nom_type if doss.type_affaire else "",
        "secteur_foncier": doss.secteur_foncier.nom if doss.secteur_foncier else "",
        "juridiction": doss.juridiction.nom if doss.juridiction else "",
        "date_ouverture": doss.date_ouverture.strftime("%d/%m/%Y") if doss.date_ouverture else "",
        "total_a_payer": float(doss.montant_dollars_enreg if devise == "USD" else doss.montant_fc_enreg),
        "reste_total_a_payer": reste,
        "total_deja_paye": total_paye,
        "reference": doss.reference or "-",
        "num_facture":doss.reference,

        "client": {
            "nom": doss.client.nom,
            "prenom": doss.client.prenom,
            "telephone": doss.client.telephone,
            "email": doss.client.email,
            "adresse": f"{doss.client.adresse.numero}, {doss.client.adresse.avenue}, {doss.client.adresse.quartier}, {doss.client.adresse.ville}" if doss.client.adresse else "",
            "representant_legal": doss.client.representant_legal if doss.client.representant_legal != "Aucune" else ""
        },
        "cabinet": {
            "nom": doss.cabinet.nom,
            "logo": logo_url,
            "telephone": doss.cabinet.telephone,
            "telephone_secondaire": doss.cabinet.telephone_secondaire,
            "email": doss.cabinet.email,
            "site_web": doss.cabinet.site_web,
            "adresse": f"{doss.cabinet.adresse.numero}, {doss.cabinet.adresse.avenue}, {doss.cabinet.adresse.quartier}, {doss.cabinet.adresse.ville}" if doss.cabinet.adresse else ""
        }
    }
    

     # Préparer paiements avec montant et reste selon devise
    paiements_data = []
    for p in paiements:
        if devise == "USD":
            montant = float(p.montant_payer_dollars)
            reste_p = float(p.montant_reste_dollars)
        else:
            montant = float(p.montant_payer_fc)
            reste_p = float(p.montant_reste_fc)

        paiements_data.append({
            "date_paiement": p.date_paiement.strftime("%d/%m/%Y"),
            "type_paiement": p.type_paiement,
            "montant": montant,
            "reste": reste_p,
            "montant_total":dossier_data,
            "personne_qui_paie": p.personne_qui_paie or "Client",
           
            "notes": p.notes or "-",
        })


    context = {
        "dossier": dossier_data,
        "today": today,
        "paiements": paiements_data,
        "activites": activites_list,
        "total_dollars": total_dollars,
        "total_fc": total_fc,
        "editable": doss.mode_honoraire == "Forfait" and not doss.forfait_defini,
        "forfait_defini": forfait_defini,
        "taux_fc": taux_fc,
        "devise": devise,
    }

    # Background
    bg_path = os.path.join(settings.BASE_DIR, "static", "images", "facture_bg.png")
    with open(bg_path, "rb") as f:
        background_base64 = base64.b64encode(f.read()).decode()
    context["background_url"] = f"data:image/png;base64,{background_base64}"

    # Appel jsreport via le service centralisé
    from utils.jsreport_service import jsreport_service
    
    filename = f"extrait_compte_{doss.numero_reference_dossier}.pdf"
    return jsreport_service.generate_pdf_response(
        template_name="Extrait_de_compte_client",
        data=context,
        filename=filename
    )



@login_required(login_url='Connexion')
def cloturer_dossier(request, dossier_id):
    """
    Vue pour clôturer définitivement un dossier
    """
    dossier_instance = get_object_or_404(dossier, pk=dossier_id, cabinet=request.user.cabinet)
    
    if request.method == 'POST':
        try:
            # Marquer le dossier comme clôturé
            dossier_instance.statut_dossier = 'Clôturé'
            dossier_instance.date_cloture = timezone.now()
            dossier_instance.save()
            
            # Log de l'activité
            try:
                from Agent.models_activity import ActivityLog
                ActivityLog.log_activity(
                    user=request.user,
                    action='close',
                    entity_type='dossier',
                    title='Dossier clôturé',
                    description=f'Dossier {dossier_instance.numero_reference_dossier} clôturé définitivement',
                    request=request,
                    dossier_id=dossier_instance.id
                )
            except Exception as e:
                print(f"Erreur lors du logging de la clôture de dossier: {e}")
            
            messages.success(request, f"Le dossier {dossier_instance.numero_reference_dossier} a été clôturé avec succès.")
            return redirect('dossier_details', dossier_id=dossier_id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la clôture du dossier: {str(e)}")
            return redirect('dossier_details', dossier_id=dossier_id)
    
    # Si ce n'est pas une requête POST, rediriger vers les détails du dossier
    messages.warning(request, "Méthode non autorisée pour la clôture de dossier.")
    return redirect('dossier_details', dossier_id=dossier_id)

@login_required(login_url='Connexion')
def print_facture(request, dossier_id):
    """
    Vue pour imprimer la facture d'un dossier avec la devise spécifiée
    """
    dossier_instance = get_object_or_404(dossier, pk=dossier_id, cabinet=request.user.cabinet)
    devise = request.GET.get('devise', 'USD').upper()
    
    # Récupérer les paiements du dossier
    paiements = dossier_instance.paiements.all().order_by('-date_paiement')
    
    # Récupérer les activités et réductions
    reductions_dict = {}
    if dossier_instance.tarif_reference:
        reductions_pour_dossier = ReductionTarifForfaitaire.objects.filter(
            dossier=dossier_instance
        ).select_related('activite')
        reductions_dict = {reduction.activite_id: reduction for reduction in reductions_pour_dossier}
        
        activites = TarifActivite.objects.filter(
            tarif=dossier_instance.tarif_reference
        ).select_related('activite')
    else:
        activites = TarifActivite.objects.none()
    
    # Récupérer le taux
    tarif_horaire = TarifHoraire.objects.filter(
        type_dossier=dossier_instance.type_affaire,
        secteur=dossier_instance.secteur_foncier
    ).first()
    
    taux_fc = float(dossier_instance.taux_enreg or 2800.0)
    
    # Calculer les totaux et préparer les activités
    total_dollars = Decimal('0.00')
    total_fc = Decimal('0.00')
    activites_list = []
    forfait_defini = dossier_instance.mode_honoraire == "Forfait" and dossier_instance.forfait_defini
    
    for act in activites:
        prix_dollars_base = float(act.prix_dollars or 0)
        prix_fc_calcule = prix_dollars_base * taux_fc
        
        prix_affiche_dollars = prix_dollars_base
        prix_affiche_fc = prix_fc_calcule
        
        if forfait_defini:
            reduction = reductions_dict.get(act.id)
            if reduction:
                prix_affiche_dollars = float(reduction.prix_reduit_dollars or prix_dollars_base)
                prix_affiche_fc = float(reduction.prix_reduit_fc or prix_fc_calcule)
        
        total_dollars += Decimal(str(prix_affiche_dollars))
        total_fc += Decimal(str(prix_affiche_fc))
        
        activites_list.append({
            "nom": act.activite.nom_activite if act.activite else "",
            "prix_dollars": prix_affiche_dollars,
            "prix_fc": prix_affiche_fc
        })
    
    # Calculer les montants payés
    if devise == "USD":
        total_paye = float(paiements.aggregate(Sum("montant_payer_dollars"))["montant_payer_dollars__sum"] or 0)
        dernier_paiement = paiements.first()
        reste = float(dernier_paiement.montant_reste_dollars) if dernier_paiement else 0
        montant_total = float(total_dollars)
    else:  # CDF
        total_paye = float(paiements.aggregate(Sum("montant_payer_fc"))["montant_payer_fc__sum"] or 0)
        dernier_paiement = paiements.first()
        reste = float(dernier_paiement.montant_reste_fc) if dernier_paiement else 0
        montant_total = float(total_fc)
    
    # Préparer le logo du cabinet
    logo_url = ""
    if dossier_instance.cabinet.logo:
        try:
            with dossier_instance.cabinet.logo.open("rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode()
            logo_url = f"data:image/png;base64,{logo_base64}"
        except:
            logo_url = ""
    
    # Préparer les données pour JSReport
    dossier_data = {
        "numero_reference_dossier": dossier_instance.numero_reference_dossier,
        "type_affaire": dossier_instance.type_affaire.nom_type if dossier_instance.type_affaire else "",
        "secteur_foncier": dossier_instance.secteur_foncier.nom if dossier_instance.secteur_foncier else "",
        "juridiction": dossier_instance.juridiction.nom if dossier_instance.juridiction else "",
        "date_ouverture": dossier_instance.date_ouverture.strftime("%d/%m/%Y") if dossier_instance.date_ouverture else "",
        "total_a_payer": montant_total,
        "reste_total_a_payer": reste,
        "total_deja_paye": total_paye,
        "reference": dossier_instance.reference or "-",
        "num_facture": dossier_instance.reference,
        "client": {
            "nom": dossier_instance.client.nom,
            "prenom": dossier_instance.client.prenom,
            "telephone": dossier_instance.client.telephone,
            "email": dossier_instance.client.email,
            "adresse": f"{dossier_instance.client.adresse.numero}, {dossier_instance.client.adresse.avenue}, {dossier_instance.client.adresse.quartier}, {dossier_instance.client.adresse.ville}" if dossier_instance.client.adresse else "",
            "representant_legal": dossier_instance.client.representant_legal if dossier_instance.client.representant_legal != "Aucune" else ""
        },
        "cabinet": {
            "nom": dossier_instance.cabinet.nom,
            "logo": logo_url,
            "telephone": dossier_instance.cabinet.telephone,
            "telephone_secondaire": dossier_instance.cabinet.telephone_secondaire,
            "email": dossier_instance.cabinet.email,
            "site_web": dossier_instance.cabinet.site_web,
            "adresse": f"{dossier_instance.cabinet.adresse.numero}, {dossier_instance.cabinet.adresse.avenue}, {dossier_instance.cabinet.adresse.quartier}, {dossier_instance.cabinet.adresse.ville}" if dossier_instance.cabinet.adresse else ""
        }
    }
    
    # Préparer les paiements
    paiements_data = []
    for p in paiements:
        if devise == "USD":
            montant = float(p.montant_payer_dollars)
            reste_p = float(p.montant_reste_dollars)
        else:
            montant = float(p.montant_payer_fc)
            reste_p = float(p.montant_reste_fc)
        
        paiements_data.append({
            "date_paiement": p.date_paiement.strftime("%d/%m/%Y"),
            "type_paiement": p.type_paiement,
            "montant": montant,
            "reste": reste_p,
            "personne_qui_paie": p.personne_qui_paie or "Client",
            "notes": p.notes or "-",
        })
    
    context = {
        "dossier": dossier_data,
        "today": datetime.now().strftime("%d/%m/%Y"),
        "paiements": paiements_data,
        "activites": activites_list,
        "total_dollars": float(total_dollars),
        "total_fc": float(total_fc),
        "editable": dossier_instance.mode_honoraire == "Forfait" and not dossier_instance.forfait_defini,
        "forfait_defini": forfait_defini,
        "taux_fc": taux_fc,
        "devise": devise,
    }
    
    # Ajouter le background
    try:
        bg_path = os.path.join(settings.BASE_DIR, "static", "images", "facture_bg.png")
        with open(bg_path, "rb") as f:
            background_base64 = base64.b64encode(f.read()).decode()
        context["background_url"] = f"data:image/png;base64,{background_base64}"
    except:
        context["background_url"] = ""
    
    # Appel JSReport via le service centralisé
    from utils.jsreport_service import jsreport_service
    
    filename = f"facture_{dossier_instance.numero_reference_dossier}_{devise}.pdf"
    return jsreport_service.generate_pdf_response(
        template_name="Extrait_de_compte_client",
        data=context,
        filename=filename,
        disposition="inline"
    )