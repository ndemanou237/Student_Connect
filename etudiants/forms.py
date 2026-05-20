from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Etudiant

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"    
        self.fields['username'].help_text = "Nom d'utilisateur" 
        self.fields['email'].label= "Adresse email" 
        self.fields['password1'].label = "Mot de passe" 
        self.fields['password1'].help_text = "Au moins 8 caractères" 
        self.fields['password2'].label = "Confirmer le mot de passe" 
        self.fields['password2'].help_text = "" 


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom','prenom', 'telephone', 'filiere', 'portfolio_fichier', 'portfolio_lien']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre nom',
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre prénom',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+237 6XX XXX XXX',
            }),
            'filiere': forms.Select(attrs={
                'class': 'form-control',
            }),
            'porfolio_fichier': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
            }),
            'porfolio_lien': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/tonprofil',
            }),
        }
    
    #validation personnalisé
    def clean(self):
        cleaned_data = super().clean()
        fichier = cleaned_data.get('porfolio_fichier')
        lien = cleaned_data.get('porfolio_lien')
        #verification que au moins un des champs est rempli
        if not fichier and not lien:
            raise forms.ValidationError(
                "vous devez fournir soit un fichier, soit un lien de porfolio."
            )
        return cleaned_data

class ConnexionForm(forms.Form):
    username = forms.CharField(
        label = "Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur",
        })
    ) 
    password = forms.CharField(
        label="Mot de passe",
        #masquage du mot de passe
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
        })
    )   
    