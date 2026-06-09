from django.shortcuts import render,redirect,get_object_or_404
from.models import Proposal
from .forms import ProposalForm
def liste_proposals(request):
    proposals = Proposal.objects.all()
    return render(request,'offres_demandes/liste.html',{'proposals':proposals})
def creer_proposal(request):
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.auteur = request.user
            proposal.save()
            return redirect('liste_proposals')
    else:
        form = ProposalForm()
    return render(request,'offres_demandes/creer.html',{'form': form})
def detail_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    return render(request,'offres_demandes/detail.html',{'proposal': proposal})
def supprimer_proposal(request,pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    if request.method == 'POST':
        proposal.delete()
        return redirect('liste_proposals')
    return render(request,'offres_demandes/supprimer.html',{'proposal':proposal})
def rechercher_proposals(request):
    matiere = request.GET.get('matiere', '')
    type_proposal = request.GET.get('type', '')
    proposals = Proposal.objects.all()
    if matiere:
        proposals = proposals.filter(matiere__icontains=matiere)
    if type_proposal:
        proposals = proposals.filter(type=type_proposal)
    return render(request, 'offres_demandes/liste.html', {'proposals': proposals})

def repondre_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    if request.method == 'POST':
        reponse = Proposal.objects.create(
            auteur=request.user,
            type='DEMANDE' if proposal.type == 'OFFRE' else 'OFFRE',
            matiere=proposal.matiere,
            description=request.POST.get('description', ''),
            disponibilite_debut=proposal.disponibilite_debut,
            disponibilite_fin=proposal.disponibilite_fin,
            modalite=proposal.modalite,
            statut='OUVERTE'
        )
        return redirect('liste_proposals')
    return render(request, 'offres_demandes/repondre.html', {'proposal': proposal})