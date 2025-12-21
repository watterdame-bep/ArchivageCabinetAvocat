# views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import LoginForm,CompteForm, ChangePasswordForm
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
