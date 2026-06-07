from django import forms
from .models import User, Profile

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
        fields = ['nom', 'prenom', 'email', 'telephone']

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
class ReinitialisationMotDePasseForm(forms.Form):
    email = forms.EmailField(
        label="Votre adresse email"
    )
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