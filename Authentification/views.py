# views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import LoginForm,CompteForm, ChangePasswordForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group 
from Authentification.models import CompteUtilisateur
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


User = get_user_model()

def login_view(request):
    form = LoginForm(request.POST or None)
    cabinet_name = ""

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Récupérer le cabinet lié
                if hasattr(user, 'cabinet') and user.cabinet:
                    cabinet_name = user.cabinet.nom

                login(request, user)

                # Durée de session selon "Se souvenir de moi"
                """if remember_me:
                    request.session.set_expiry(1209600)  # 2 semaines
                else:
                    request.session.set_expiry(0)  # se termine à la fermeture du navigateur"""
                if(user.type_compte == 'admin'):
                   return redirect('Dashboard_Administrator')
                elif(user.type_compte == 'user'): #and user.is_superuser):
                   return redirect('Dashboard_Cabinet_Administrateur')
                #else :
                #    return redirect('Dashboard_Cabinet_Agent_Avocat')

            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect ❌")
        else:
              form=LoginForm()

    context = {
        'form': form,
        'cabinet_name': cabinet_name
    }
    return render(request, 'auth_template/auth_login.html', context)


@login_required
def user_profile_view(request):
    """Vue pour afficher et modifier le profil utilisateur"""
    user = request.user
    
    # Informations de l'agent associé
    agent_info = None
    if hasattr(user, 'agent') and user.agent:
        agent_info = user.agent
    
    # Informations du cabinet
    cabinet_info = None
    if hasattr(user, 'cabinet') and user.cabinet:
        cabinet_info = user.cabinet
    
    # Statistiques d'activité de l'utilisateur
    from Dossier.models import dossier, AvocatDossier, DeclarationDossier, PieceDossier
    from paiement.models import Paiement
    from django.db.models import Count, Sum
    from datetime import datetime, timedelta
    
    # Période pour les statistiques (30 derniers jours)
    date_limite = datetime.now() - timedelta(days=30)
    
    # Statistiques des dossiers
    dossiers_assignes = 0
    dossiers_actifs = 0
    if agent_info:
        # Dossiers où l'agent est assigné comme avocat
        dossiers_assignes = AvocatDossier.objects.filter(avocat=agent_info).count()
        dossiers_actifs = AvocatDossier.objects.filter(
            avocat=agent_info, 
            dossier__statut_dossier__in=['En cours', 'Ouvert']
        ).count()
    
    # Statistiques des paiements (si l'utilisateur gère la caisse)
    paiements_traites = Paiement.objects.filter(agent=agent_info).count() if agent_info else 0
    paiements_recents = Paiement.objects.filter(
        agent=agent_info, 
        date_paiement__gte=date_limite
    ).count() if agent_info else 0
    
    # Montant total des paiements traités (30 derniers jours)
    montant_paiements_recents = Paiement.objects.filter(
        agent=agent_info,
        date_paiement__gte=date_limite
    ).aggregate(
        total_usd=Sum('montant_payer_dollars'),
        total_fc=Sum('montant_payer_fc')
    ) if agent_info else {'total_usd': 0, 'total_fc': 0}
    
    # Déclarations ajoutées
    declarations_ajoutees = DeclarationDossier.objects.filter(
        ecrit_par=agent_info
    ).count() if agent_info else 0
    
    declarations_recentes = DeclarationDossier.objects.filter(
        ecrit_par=agent_info,
        date_ajout__gte=date_limite
    ).count() if agent_info else 0
    
    # Documents ajoutés
    documents_ajoutes = PieceDossier.objects.filter(
        ajoute_par=agent_info
    ).count() if agent_info else 0
    
    documents_recents = PieceDossier.objects.filter(
        ajoute_par=agent_info,
        date_ajout__gte=date_limite
    ).count() if agent_info else 0
    
    # Activités récentes détaillées (5 dernières)
    activites_recentes = []
    
    if agent_info:
        # Paiements récents
        paiements_recents_detail = Paiement.objects.filter(
            agent=agent_info
        ).order_by('-date_paiement')[:3]
        
        for paiement in paiements_recents_detail:
            activites_recentes.append({
                'type': 'paiement',
                'icon': 'mdi-cash',
                'color': 'success',
                'titre': f'Paiement enregistré',
                'description': f'{paiement.montant_payer_dollars} USD - {paiement.dossier.numero_reference_dossier if paiement.dossier else "Caisse"}',
                'date': paiement.date_paiement,
                'url': f'/dossier/{paiement.dossier.id}/' if paiement.dossier else '/caisse/'
            })
        
        # Déclarations récentes
        declarations_recentes_detail = DeclarationDossier.objects.filter(
            ecrit_par=agent_info
        ).order_by('-date_ajout')[:2]
        
        for declaration in declarations_recentes_detail:
            activites_recentes.append({
                'type': 'declaration',
                'icon': 'mdi-file-document-edit',
                'color': 'info',
                'titre': 'Déclaration ajoutée',
                'description': f'Dossier {declaration.dossier.numero_reference_dossier}',
                'date': declaration.date_ajout,
                'url': f'/dossier/{declaration.dossier.id}/'
            })
        
        # Documents récents
        documents_recents_detail = PieceDossier.objects.filter(
            ajoute_par=agent_info
        ).order_by('-date_ajout')[:2]
        
        for document in documents_recents_detail:
            activites_recentes.append({
                'type': 'document',
                'icon': 'mdi-file-plus',
                'color': 'warning',
                'titre': 'Document ajouté',
                'description': f'{document.titre} - {document.dossier.numero_reference_dossier}',
                'date': document.date_ajout,
                'url': f'/dossier/{document.dossier.id}/'
            })
    
    # Trier les activités par date (plus récentes en premier)
    activites_recentes.sort(key=lambda x: x['date'], reverse=True)
    activites_recentes = activites_recentes[:5]  # Garder seulement les 5 plus récentes
    
    context = {
        'user': user,
        'agent_info': agent_info,
        'cabinet_info': cabinet_info,
        'statistiques': {
            'dossiers_assignes': dossiers_assignes,
            'dossiers_actifs': dossiers_actifs,
            'paiements_traites': paiements_traites,
            'paiements_recents': paiements_recents,
            'montant_paiements_usd': montant_paiements_recents['total_usd'] or 0,
            'montant_paiements_fc': montant_paiements_recents['total_fc'] or 0,
            'declarations_ajoutees': declarations_ajoutees,
            'declarations_recentes': declarations_recentes,
            'documents_ajoutes': documents_ajoutes,
            'documents_recents': documents_recents,
        },
        'activites_recentes': activites_recentes,
    }
    
    return render(request, 'auth_template/user_profile.html', context)


@login_required
def edit_profile_view(request):
    """Vue pour modifier les informations du profil"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès ✅")
            return redirect('user_profile')
        else:
            messages.error(request, "Erreur lors de la mise à jour du profil ❌")
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    
    return render(request, 'auth_template/edit_profile.html', context)

    return render(request, "auth_template/auth_login.html", {'form': form, 'cabinet_name': cabinet_name})


# 🔸 Nouvelle vue AJAX pour afficher le cabinet lié à un nom d'utilisateur
def get_cabinet_name(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
        cabinet_name = user.cabinet.nom if hasattr(user, 'cabinet') and user.cabinet else ""
        return JsonResponse({'cabinet_name': cabinet_name})
    except User.DoesNotExist:
        return JsonResponse({'cabinet_name': ''})


def creer_utilisateur_agent(request):
    cabinet_user = getattr(request.user, 'cabinet', None)

    if request.method == "POST":
        form = CompteForm(request.POST, request.FILES, cabinet=cabinet_user)
        if form.is_valid():
            compte = form.save(commit=False)
            compte.cabinet = cabinet_user

            # Copier la photo de l'agent si disponible
            agent_associe = form.cleaned_data.get('agent')
            if agent_associe and agent_associe.photo:
                compte.photo = agent_associe.photo

            compte.save()
            
             # Lier le compte au même groupe que l'agent
            if agent_associe and agent_associe.groupe_attribue:
                compte.groups.add(agent_associe.groupe_attribue)

            return redirect('creer_utilisateur_agent')  # page liste des comptes
        else:
            print("Form errors:", form.errors)
                
    else:
        form = CompteForm(cabinet=cabinet_user)
    compte = CompteUtilisateur.objects.filter(cabinet=request.user.cabinet)
    return render(request, 'admin_template/cases -2Compte.html', {'form': form,'compte':compte})




def deconnexion(request):
    """
    Déconnecte l'utilisateur et supprime toutes les données de session.
    Empêche aussi les données de rester dans le formulaire de connexion.
    """
    # Django supprime automatiquement la session avec logout()
    logout(request)
    
    # Par sécurité, on nettoie toute la session manuellement (optionnel mais recommandé)
    request.session.flush()
    
    # Redirige vers la page de connexion
    response = redirect('Connexion')

    # Empêche le navigateur de garder le cache du formulaire
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


@login_required
def change_password(request):
    """Vue pour changer le mot de passe de l'utilisateur connecté"""
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Maintenir la session après changement de mot de passe
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Votre mot de passe a été modifié avec succès ! ✅')
            
            # Rediriger selon le type d'utilisateur
            if request.user.type_compte == 'admin':
                return redirect('Dashboard_Administrator')
            elif request.user.type_compte == 'user':
                return redirect('Dashboard_Cabinet_Administrateur')
            else:
                return redirect('change_password')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous. ❌')
    else:
        form = ChangePasswordForm(user=request.user)
    
    return render(request, 'auth_template/auth_user_pass.html', {'form': form})
