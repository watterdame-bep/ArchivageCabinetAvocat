# Structure/forms.py
from django import forms
from .models import Cabinet
from  Authentification.models import CompteUtilisateur
from django.contrib.auth.models import Group
from Adresse.models import adresse, Ville, commune

class CabinetCreationForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    #confirm_password = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Cabinet
        fields = ['nom', 'numero_identification', 'telephone', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        """confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")"""
        return cleaned_data

    def save(self, commit=True):
        cabinet = super().save(commit=False)
        if commit:
            cabinet.save()
            # Créer le compte admin lié
            user = CompteUtilisateur.objects.create_superuser(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                cabinet=cabinet,
                
            )

            # Ajouter l'utilisateur au groupe
        try:
            groupe_admin = Group.objects.get(name="Administrateur")
            user.groups.add(groupe_admin)
        except Group.DoesNotExist:
            # Optionnel : log ou message si le groupe n'existe pas
            pass
            user.save()
        return cabinet




class AdresseForm(forms.ModelForm):
    class Meta:
        model = adresse
        fields = ["numero", "avenue", "quartier", "commune", "ville"]


class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = [
            "nom", "numero_identification", "telephone",
            "telephone_secondaire", "forme_juridique",
            "num_id_fiscal", "email", "logo"
        ]

class VilleSelectForm(forms.ModelForm):
    ville = forms.ModelChoiceField(queryset=Ville.objects.all(), required=True)

    class Meta:
        model = adresse
        fields = ["ville"]

class CommuneSelectForm(forms.ModelForm):
    commune = forms.ModelChoiceField(queryset=commune.objects.all(), required=True)

    class Meta:
        model = adresse
        fields = ["commune"]
