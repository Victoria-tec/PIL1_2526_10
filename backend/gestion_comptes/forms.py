from django import forms
from django.contrib.auth import get_user_model
from gestion_comptes.models import Profile

User = get_user_model()


class InscriptionForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        label="Mot de passe"
    )
    confirmation_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmer le mot de passe"
    )

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'telephone']
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
        }

    def clean(self):
        cleaned_data = super().clean()
        mdp = cleaned_data.get('mot_de_passe')
        confirm = cleaned_data.get('confirmation_mot_de_passe')
        if mdp and confirm and mdp != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data


class ConnexionForm(forms.Form):
    identifiant = forms.CharField(label="Email ou téléphone")
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe"
    )


class EmailReinitialisationForm(forms.Form):
    email = forms.EmailField(label="Votre adresse email")


class ReinitialisationMotDePasseForm(forms.Form):
    code = forms.IntegerField(label="Code reçu dans votre messagerie")
    nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        label="Nouveau mot de passe"
    )
    confirmation_nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmer le nouveau mot de passe"
    )

    def clean(self):
        cleaned_data = super().clean()
        mdp = cleaned_data.get('nouveau_mot_de_passe')
        confirm = cleaned_data.get('confirmation_nouveau_mot_de_passe')
        if mdp and confirm and mdp != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
