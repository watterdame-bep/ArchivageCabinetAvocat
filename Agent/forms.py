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
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'sexe': forms.Select(choices=[('Homme', 'Homme'), ('Femme', 'Femme')]),
            'specialite': forms.Select(),  # Django va automatiquement remplir avec les Specialite existantes

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
