from django import forms
from .models import Proposal
class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['type','matiere','description','disponibilite_debut','disponibilite_fin','modalite']
        