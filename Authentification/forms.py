from django import forms
from .models import CompteUtilisateur
from Agent.models import agent
from django.contrib.auth.forms import PasswordChangeForm

# forms.py
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom utilisateur',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
 widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'autocomplete': 'off'
        })
    )
    cabinet = forms.CharField(
        label="Cabinet",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    

 

class CompteForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )

    class Meta:
        model = CompteUtilisateur
        fields = ['username', 'password', 'agent']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'agent': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        cabinet = kwargs.pop('cabinet', None)
        super().__init__(*args, **kwargs)

        # Limiter les agents qui n'ont pas de compte
        qs = agent.objects.filter(Agent_Utilisateur__isnull=True)
        if cabinet:
            qs = qs.filter(company=cabinet)
        self.fields['agent'].queryset = qs


class UserProfileForm(forms.ModelForm):
    """Formulaire pour modifier le profil utilisateur"""
    
    class Meta:
        model = CompteUtilisateur
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom d'utilisateur"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de famille'
            }),
        }
        labels = {
            'username': "Nom d'utilisateur",
            'email': 'Adresse email',
            'first_name': 'Prénom',
            'last_name': 'Nom de famille',
        }

    def clean_username(self):
        """Vérifier que le nom d'utilisateur est unique (sauf pour l'utilisateur actuel)"""
        username = self.cleaned_data.get('username')
        if CompteUtilisateur.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return username

    def clean_email(self):
        """Vérifier que l'email est unique (sauf pour l'utilisateur actuel)"""
        email = self.cleaned_data.get('email')
        if email and CompteUtilisateur.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email


class ChangePasswordForm(forms.Form):
    """Formulaire pour changer le mot de passe de l'utilisateur connecté"""
    old_password = forms.CharField(
        label="Mot de passe actuel",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe actuel'
        })
    )
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        })
    )
    new_password2 = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le nouveau mot de passe'
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """Vérifier que l'ancien mot de passe est correct"""
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("L'ancien mot de passe est incorrect.")
        return old_password

    def clean_new_password2(self):
        """Vérifier que les deux nouveaux mots de passe correspondent"""
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return password2

    def clean_new_password1(self):
        """Validation du nouveau mot de passe"""
        password = self.cleaned_data.get('new_password1')
        if password:
            if len(password) < 6:
                raise forms.ValidationError("Le mot de passe doit contenir au moins 6 caractères.")
        return password

    def save(self):
        """Sauvegarder le nouveau mot de passe"""
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        self.user.save()
        return self.user
