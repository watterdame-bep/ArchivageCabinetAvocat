from django import forms
from .models import agent, PieceJustificative
from django.forms import modelformset_factory

class AgentForm(forms.ModelForm):
    class Meta:
        model = agent
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'numero_identification', 'date_naissance',
            'sexe', 'adresse', 'poste', 'specialite', 'annee_experience',
            'a_propos', 'photo'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de famille'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemple.com'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+243 XXX XXX XXX'}),
            'numero_identification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro d\'identification'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}, choices=[('Homme', 'Homme'), ('Femme', 'Femme')]),
            'poste': forms.Select(attrs={'class': 'form-control'}),
            'specialite': forms.Select(attrs={'class': 'form-control'}),
            'annee_experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 5'}),
            'a_propos': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Décrivez brièvement l\'agent...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class PieceJustificativeForm(forms.ModelForm):
    class Meta:
        model = PieceJustificative
        fields = ['type_piece', 'numero_piece', 'fichier']


PieceJustificativeFormSet = modelformset_factory(
    PieceJustificative,
    form=PieceJustificativeForm,
    extra=1,  # au moins un champ vide pour ajouter un document
    can_delete=True  # permet de supprimer un document existant
)
