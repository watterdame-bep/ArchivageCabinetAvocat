from django import forms
from .models import CompteUtilisateur
from Agent.models import agent

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
