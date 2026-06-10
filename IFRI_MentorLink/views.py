from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from backend.matching.models import Matching
from backend.matching.views import calculer_score

User = get_user_model()


def accueil(request):
    return render(request, 'base.html')


@login_required
def hub(request):
    tous_matchs = Matching.objects.filter(
        user1=request.user
    ) | Matching.objects.filter(
        user2=request.user
    ).select_related('user1', 'user2')

    matchs_en_cours = tous_matchs.filter(statut='VALIDE')
    matchs_attente_validation = tous_matchs.filter(statut='EN_ATTENTE', user2=request.user)
    matchs_attente_reponse = tous_matchs.filter(statut='EN_ATTENTE', user1=request.user)

    suggestions = []
    autres = User.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    actifs = tous_matchs.filter(statut__in=['EN_ATTENTE', 'VALIDE'])
    deja_matches = set()
    for m in actifs:
        deja_matches.add(m.user1_id)
        deja_matches.add(m.user2_id)
    for u in autres:
        if u.id in deja_matches:
            continue
        score = calculer_score(request.user, u)
        if score > 0:
            from backend.matching.views import trouver_matiere
            matiere = trouver_matiere(request.user, u)
            suggestions.append({'user': u, 'score': score, 'matiere': matiere})
    suggestions.sort(key=lambda x: -x['score'])
    suggestions = suggestions[:6]

    return render(request, 'hub.html', {
        'matchs_en_cours': matchs_en_cours[:10],
        'matchs_attente_validation': matchs_attente_validation[:10],
        'matchs_attente_reponse': matchs_attente_reponse[:10],
        'suggestions': suggestions,
    })


def profil_visiteur(request, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    visiteur = User.objects.get(id=user_id)
    return render(request, 'profil-visiteur.html', {'visiteur': visiteur})
