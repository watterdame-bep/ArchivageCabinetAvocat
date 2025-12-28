from django.shortcuts import render, redirect
from django.contrib import messages
from .models import agent, PieceJustificative, Specialite
from Dossier.models import TypePiece
from .forms import AgentForm, PieceJustificativeFormSet 
from Adresse.models import adresse, commune,Ville
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group
from Agent.models import agent # Assurez-vous que le modèle 'agent' est correctement importé comme 'Agent'

def ajouter_agent(request): 
    specialites = Specialite.objects.all()
    communes = commune.objects.filter(cabinet=request.user.cabinet)
    villes = Ville.objects.filter(cabinet=request.user.cabinet)

    if request.method == "POST":
        try:
            # Récupération des instances à partir des IDs
            commune_id = request.POST.get('commune')
            ville_id = request.POST.get('ville')

            commune_instance = commune.objects.get(pk=commune_id) if commune_id else None
            ville_instance = Ville.objects.get(pk=ville_id) if ville_id else None

            # Création de l’adresse
            nouvelle_adresse = adresse.objects.create(
                numero=request.POST.get('numero'),
                avenue=request.POST.get('avenue'),
                quartier=request.POST.get('quartier'),
                commune=commune_instance.nom if commune_instance else '',
                ville=ville_instance.nom_ville if ville_instance else '',
            )
            adresse_id = nouvelle_adresse.pk

        except Exception as e:
            messages.error(request, f"Erreur lors de la création de l'adresse: {e}")
            agent_form = AgentForm(request.POST, request.FILES)
            return render(request, 'admin_template/attorney_list.html', {
                'agent_form': agent_form,
                'specialites': specialites,
                'communes': communes,
                'villes': villes,
            })
        
        # Suite du code inchangée…
        post_data = request.POST.copy()
        post_data['adresse'] = adresse_id 
        agent_form = AgentForm(post_data, request.FILES)
        pieces_formset = PieceJustificativeFormSet(request.POST, request.FILES)

        if agent_form.is_valid():          
            agent_instance = agent_form.save(commit=False)
            poste_choisi = post_data.get('poste')

            if poste_choisi:
                try:
                    groupe = Group.objects.get(name=poste_choisi)
                    agent_instance.groupe_attribue_id = groupe.pk
                except Group.DoesNotExist:
                    pass

            specialite_id = post_data.get('specialite')
            if specialite_id:
                try:
                    agent_instance.specialite = Specialite.objects.get(id=specialite_id)
                except Specialite.DoesNotExist:
                    agent_instance.specialite = None

            agent_instance.company = request.user.cabinet
            agent_instance.save()

            # Gestion des pièces justificatives
            all_type_pieces = post_data.getlist('type_piece')
            all_numeros = post_data.getlist('numero_piece')
            all_fichiers = request.FILES.getlist('fichier')

            for type_piece_id, numero, fichier in zip(all_type_pieces, all_numeros, all_fichiers):
              if type_piece_id and fichier:
                type_piece_instance = TypePiece.objects.get(id=type_piece_id)
                PieceJustificative.objects.create(
            agent=agent_instance,
            type_piece=type_piece_instance,
            numero_piece=numero,
            fichier=fichier
           )


            messages.success(request, f"L'agent {agent_instance.prenom} {agent_instance.nom} a été enregistré avec succès.")
            return redirect('Agent_Liste')
        else:
            messages.error(request, "Erreur de validation. Veuillez vérifier les informations de l'agent.")
            return render(request, 'admin_template/attorney_list.html', {
                'agent_form': agent_form,
                'specialites': specialites,
                'communes': communes,
                'villes': villes,
                'is_modal_active': True,
            })

    else:  # Méthode GET
        agent_form = AgentForm()
        pieces_formset = PieceJustificativeFormSet(queryset=PieceJustificative.objects.none())

    return render(request, 'admin_template/attorney_list.html', {
        'agent_form': agent_form,
        'pieces_formset': pieces_formset,
        'specialites': specialites,
        'communes': communes,
        'villes': villes,
    })





def details_agent(request, agent_id):
    """Vue détaillée d'un agent avec toutes ses informations et statistiques"""
    agent_instance = get_object_or_404(
        agent,
        pk=agent_id,
        company=request.user.cabinet  # Limiter par cabinet
    )
    
    # Importer les modèles nécessaires pour les statistiques
    from Dossier.models import dossier, AvocatDossier, DeclarationDossier, PieceDossier
    from paiement.models import Paiement
    from .models_activity import ActivityLog
    from django.db.models import Count, Sum, Q
    from datetime import datetime, timedelta
    
    # Période pour les statistiques (30 derniers jours)
    date_limite = datetime.now() - timedelta(days=30)
    
    # === STATISTIQUES DES DOSSIERS ===
    try:
        # Dossiers assignés à cet agent
        dossiers_assignes = AvocatDossier.objects.filter(avocat=agent_instance)
        total_dossiers = dossiers_assignes.count()
        
        # Dossiers par statut
        dossiers_actifs = dossiers_assignes.filter(
            dossier__statut_dossier__in=['En cours', 'Ouvert']
        ).count()
        
        dossiers_clotures = dossiers_assignes.filter(
            dossier__statut_dossier='Clôturé'
        ).count()
        
        dossiers_gagnes = dossiers_assignes.filter(
            dossier__score='gagne'
        ).count()
        
        dossiers_perdus = dossiers_assignes.filter(
            dossier__score='perdu'
        ).count()
    except Exception as e:
        print(f"Erreur dans le calcul des statistiques de dossiers: {e}")
        total_dossiers = dossiers_actifs = dossiers_clotures = dossiers_gagnes = dossiers_perdus = 0
    
    # === STATISTIQUES DES PAIEMENTS ===
    try:
        paiements_traites = Paiement.objects.filter(agent=agent_instance)
        total_paiements = paiements_traites.count()
        
        # Montants traités
        montants_totaux = paiements_traites.aggregate(
            total_usd=Sum('montant_payer_dollars'),
            total_fc=Sum('montant_payer_fc')
        )
        
        # Paiements récents (30 derniers jours)
        paiements_recents = paiements_traites.filter(
            date_paiement__gte=date_limite
        ).count()
    except Exception as e:
        print(f"Erreur dans le calcul des statistiques de paiements: {e}")
        total_paiements = paiements_recents = 0
        montants_totaux = {'total_usd': 0, 'total_fc': 0}
    
    # === STATISTIQUES DES ACTIVITÉS ===
    try:
        # Déclarations rédigées
        declarations_total = DeclarationDossier.objects.filter(ecrit_par=agent_instance).count()
        declarations_recentes = DeclarationDossier.objects.filter(
            ecrit_par=agent_instance,
            date_ajout__gte=date_limite
        ).count()
        
        # Documents ajoutés
        documents_total = PieceDossier.objects.filter(ajoute_par=agent_instance).count()
        documents_recents = PieceDossier.objects.filter(
            ajoute_par=agent_instance,
            date_ajout__gte=date_limite
        ).count()
    except Exception as e:
        print(f"Erreur dans le calcul des statistiques d'activités: {e}")
        declarations_total = declarations_recentes = documents_total = documents_recents = 0
    
    # === DOSSIERS DÉTAILLÉS ===
    try:
        # Dossiers actifs avec détails
        dossiers_actifs_detail = dossier.objects.filter(
            avocatdossier__avocat=agent_instance,
            statut_dossier__in=['En cours', 'Ouvert']
        ).select_related('client', 'type_affaire').order_by('-date_ouverture')[:5]
        
        # Dossiers récemment clôturés
        dossiers_clotures_detail = dossier.objects.filter(
            avocatdossier__avocat=agent_instance,
            statut_dossier='Clôturé'
        ).select_related('client', 'type_affaire').order_by('-date_cloture')[:5]
    except Exception as e:
        print(f"Erreur dans la récupération des dossiers détaillés: {e}")
        dossiers_actifs_detail = dossiers_clotures_detail = []
    
    # === ACTIVITÉS RÉCENTES (SYSTÈME SIMPLE) ===
    try:
        # Importer le modèle d'activité
        from .models_activity import ActivityLog
        
        # Récupérer les activités réelles depuis les logs
        activites_logs = ActivityLog.objects.all().order_by('-timestamp')[:20]
        
        activites_recentes = []
        for log in activites_logs:
            activites_recentes.append({
                'type': log.action,
                'icon': log.icon,
                'color': log.color,
                'titre': log.title,
                'description': log.description,
                'date': log.timestamp,
                'dossier_id': log.dossier_id
            })
        
        # Si pas assez d'activités dans les logs, compléter avec les anciennes données
        if len(activites_recentes) < 8:
            # Paiements récents
            paiements_recents_detail = Paiement.objects.filter(
                agent=agent_instance
            ).select_related('dossier', 'client').order_by('-date_paiement')[:3]
            
            for paiement in paiements_recents_detail:
                if len(activites_recentes) >= 15:
                    break
                activites_recentes.append({
                    'type': 'paiement',
                    'icon': 'mdi-cash',
                    'color': 'success',
                    'titre': 'Paiement enregistré',
                    'description': f'{paiement.montant_payer_dollars} USD - {paiement.dossier.numero_reference_dossier if paiement.dossier else "Caisse"}',
                    'date': paiement.date_paiement,
                    'dossier_id': paiement.dossier.id if paiement.dossier else None
                })
        
        # Trier par date
        activites_recentes.sort(key=lambda x: x['date'], reverse=True)
        activites_recentes = activites_recentes[:15]  # Garder les 15 plus récentes
        
    except Exception as e:
        print(f"Erreur dans la récupération des activités récentes: {e}")
        activites_recentes = []
    
    # === PIÈCES JUSTIFICATIVES ===
    try:
        pieces_justificatives = PieceJustificative.objects.filter(
            agent=agent_instance
        ).select_related('type_piece')
        total_pieces_justificatives = pieces_justificatives.count()
    except Exception as e:
        print(f"Erreur dans la récupération des pièces justificatives: {e}")
        pieces_justificatives = []
        total_pieces_justificatives = 0
    
    # Debug: Afficher les statistiques calculées
    print(f"Statistiques pour l'agent {agent_instance.nom}:")
    print(f"- Total dossiers: {total_dossiers}")
    print(f"- Dossiers actifs: {dossiers_actifs}")
    print(f"- Total paiements: {total_paiements}")
    print(f"- Total pièces: {total_pieces_justificatives}")
    print(f"- Activités récentes: {len(activites_recentes)}")
    
    context = {
        'agent': agent_instance,
        'statistiques': {
            'total_dossiers': total_dossiers,
            'dossiers_actifs': dossiers_actifs,
            'dossiers_clotures': dossiers_clotures,
            'dossiers_gagnes': dossiers_gagnes,
            'dossiers_perdus': dossiers_perdus,
            'total_pieces_justificatives': total_pieces_justificatives,
            'total_paiements': total_paiements,
            'paiements_recents': paiements_recents,
            'montant_total_usd': montants_totaux['total_usd'] or 0,
            'montant_total_fc': montants_totaux['total_fc'] or 0,
            'declarations_total': declarations_total,
            'declarations_recentes': declarations_recentes,
            'documents_total': documents_total,
            'documents_recents': documents_recents,
        },
        'dossiers_actifs': dossiers_actifs_detail,
        'dossiers_clotures': dossiers_clotures_detail,
        'activites_recentes': activites_recentes,
        'pieces_justificatives': pieces_justificatives,
    }

    return render(request, "admin_template/attorney_details.html", context)


def modifier_agent(request, agent_id):
    """Vue pour modifier les informations d'un agent"""
    agent_instance = get_object_or_404(
        agent,
        pk=agent_id,
        company=request.user.cabinet  # Limiter par cabinet
    )
    
    # Importer les modèles nécessaires
    from Adresse.models import commune, Ville
    from Structure.models import Specialite
    from django.contrib.auth.models import Group
    
    # Récupérer les données pour les formulaires
    specialites = Specialite.objects.all()
    communes = commune.objects.filter(cabinet=request.user.cabinet)
    villes = Ville.objects.filter(cabinet=request.user.cabinet)
    
    if request.method == "POST":
        try:
            # Gestion de l'adresse si modifiée
            commune_id = request.POST.get('commune')
            ville_id = request.POST.get('ville')
            
            if commune_id and ville_id:
                commune_instance = commune.objects.get(pk=commune_id)
                ville_instance = Ville.objects.get(pk=ville_id)
                
                # Mettre à jour l'adresse existante ou en créer une nouvelle
                if agent_instance.adresse:
                    agent_instance.adresse.numero = request.POST.get('numero', agent_instance.adresse.numero)
                    agent_instance.adresse.avenue = request.POST.get('avenue', agent_instance.adresse.avenue)
                    agent_instance.adresse.quartier = request.POST.get('quartier', agent_instance.adresse.quartier)
                    agent_instance.adresse.commune = commune_instance.nom
                    agent_instance.adresse.ville = ville_instance.nom_ville
                    agent_instance.adresse.save()
                else:
                    # Créer une nouvelle adresse
                    from Adresse.models import adresse
                    nouvelle_adresse = adresse.objects.create(
                        numero=request.POST.get('numero'),
                        avenue=request.POST.get('avenue'),
                        quartier=request.POST.get('quartier'),
                        commune=commune_instance.nom,
                        ville=ville_instance.nom_ville,
                    )
                    agent_instance.adresse = nouvelle_adresse
            
            # Traitement du formulaire agent
            post_data = request.POST.copy()
            if agent_instance.adresse:
                post_data['adresse'] = agent_instance.adresse.pk
            
            agent_form = AgentForm(post_data, request.FILES, instance=agent_instance)
            
            if agent_form.is_valid():
                agent_instance = agent_form.save(commit=False)
                
                # Gestion du poste et du groupe
                poste_choisi = post_data.get('poste')
                if poste_choisi:
                    try:
                        groupe = Group.objects.get(name=poste_choisi)
                        agent_instance.groupe_attribue_id = groupe.pk
                    except Group.DoesNotExist:
                        pass
                
                # Gestion de la spécialité
                specialite_id = post_data.get('specialite')
                if specialite_id:
                    try:
                        agent_instance.specialite = Specialite.objects.get(id=specialite_id)
                    except Specialite.DoesNotExist:
                        agent_instance.specialite = None
                
                agent_instance.save()
                
                messages.success(request, f"Les informations de {agent_instance.prenom} {agent_instance.nom} ont été mises à jour avec succès.")
                return redirect('agent_details', agent_id=agent_instance.id)
            else:
                messages.error(request, "Erreur de validation. Veuillez vérifier les informations.")
                
        except Exception as e:
            messages.error(request, f"Erreur lors de la mise à jour: {e}")
    
    else:  # Méthode GET
        agent_form = AgentForm(instance=agent_instance)
    
    context = {
        'agent_form': agent_form,
        'agent': agent_instance,
        'specialites': specialites,
        'communes': communes,
        'villes': villes,
        'is_edit_mode': True,
    }
    
    return render(request, 'admin_template/edit_agent.html', context)


