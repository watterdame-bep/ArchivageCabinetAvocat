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
    agent_qs = agent.objects.filter(pk=agent_id)
    agent_instance = get_object_or_404(
        agent,
        pk=agent_id,
        company=request.user.cabinet  # Important si tu veux limiter par cabinet
    )

    print("Agent existe ?", agent_qs.exists())


    context = {
        # IMPORTANT : On passe un seul objet nommé 'agent', pas une liste 'agents'
        'agent': agent_instance,
        # Ajoutez d'autres données nécessaires, ex: 'affaires_traitees': agent_instance.affaires.all()
    }

    return render(request, "admin_template/attorney_details.html", context)


