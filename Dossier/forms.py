from django import forms
from .models import client,dossier,PieceDossier
from Structure.models import Juridiction
# type: ignore 
from django_select2.forms import ModelSelect2Widget  # type: ignore

class ClientForm(forms.ModelForm):
    class Meta:
        model = client
        # Excluez 'adresse', 'cabinet', 'photo' et 'date_enregistrement' car ils seront gérés séparément dans la vue ou par défaut.
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'date_naissance', 'sexe', 
            'nationalite', 'type_client', 
            'profession', 'representant_legal'
        ]
        
        widgets = {
             'type_client': forms.Select(attrs={'id': 'typeClientSelect'}), # Pour la liaison JS
             'representant_legal': forms.TextInput(attrs={'id': 'representantLegalInput', 'placeholder': 'Nom du représentant légal'}),
                     }


    def clean(self):
        """
        Validation conditionnelle: Les champs Representant légal et N° d'identification
        sont obligatoires si le type de client est 'Morale'.
        """
        cleaned_data = super().clean()
        
        type_client = cleaned_data.get("type_client")
        representant_legal = cleaned_data.get("representant_legal")
        numero_identification = cleaned_data.get("numero_identification")

        if type_client == 'Morale':
            if not representant_legal:
                self.add_error('representant_legal', "Ce champ est obligatoire pour un client de type Morale.")
            
            if not numero_identification:
                self.add_error('numero_identification', "Le N° d’identification (RCCM, etc.) est obligatoire pour un client de type Morale.")

        # Si 'Physique' est sélectionné, les champs sont 'blank=True' et donc facultatifs.

        return cleaned_data
    


class DossierForm(forms.ModelForm):
    class Meta:
        model = dossier
        fields = ['client','titre','type_affaire','secteur_foncier','partie_adverse_nom','juridiction','tarif_reference']

        widgets = {
           'client': ModelSelect2Widget(
                model=client,
                search_fields=['nom__icontains', 'prenom__icontains'],
                attrs={
                    'data-placeholder': 'Rechercher un client...',
                    'class': 'form-select',
                }
            ),
            'titre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nom du dossier', 'required': 'required' }),
            'type_affaire': forms.Select(attrs={'class': 'form-select select2','required': 'required' }),
            'secteur_foncier': forms.Select(attrs={ 'class': 'form-select select2','required': 'required' }),
            'partie_adverse_nom': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nom de la partie adverse','required': 'required'}),
            'juridiction': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ex : Tribunal de Grande Instance','required': 'required'}),
            #'description': forms.Textarea(attrs={'class': 'form-control','rows': 3,'placeholder': 'Description du dossier (facultatif)'}),
            
        }
        juridiction = forms.ModelChoiceField(
        queryset=Juridiction.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        label="Juridiction compétente"
    )
      

#Pour gerer les pices d'un dossier

class PieceDossierForm(forms.ModelForm):
    class Meta:
        model = PieceDossier
        fields = ['titre', 'fichier','format_fichier']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du document'}),
            #'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description (facultatif)'}),
            'fichier': forms.ClearableFileInput(attrs={'class': 'form-control'}),         
            #'format': forms.Select(attrs={'class': 'form-select select2','required': 'required' }),
        }




#pour gerer assignation d'avocat pour un dossier
from django import forms
from .models import AvocatDossier

class AssignerAvocatsForm(forms.Form):
    avocats = forms.ModelMultipleChoiceField(
        queryset=None,  # On va l'initialiser dynamiquement dans la vue
        widget=forms.MultipleHiddenInput()
    )

    def __init__(self, *args, **kwargs):
        agents_queryset = kwargs.pop('agents_queryset', None)
        super().__init__(*args, **kwargs)
        if agents_queryset is not None:
            self.fields['avocats'].queryset = agents_queryset


#Pour gerer le tarif honoraire
# forms.py
from django import forms
from .models import dossier, TarifHoraire

class ModeHonoraireForm(forms.ModelForm):
    class Meta:
        model = dossier
        fields = ['mode_honoraire', 'tarif_reference']
        widgets = {
            'mode_honoraire': forms.Select(attrs={'class': 'form-select'}),
            'tarif_reference': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        # On reçoit le dossier dans les kwargs pour filtrer les tarifs
        dossier_instance = kwargs.pop('dossier_instance', None)
        super().__init__(*args, **kwargs)

        if dossier_instance:
            self.fields['tarif_reference'].queryset = TarifHoraire.objects.filter(
                type_dossier=dossier_instance.type_affaire,
                secteur=dossier_instance.secteur_foncier
            )
        else:
            self.fields['tarif_reference'].queryset = TarifHoraire.objects.none()
