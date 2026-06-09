# Create your views here.
from django.shortcuts import render
from backend.gestion_comptes.models import User, Profile
from .models import Matching

def calculer_score(user_a, user_b):
    score = 0
    
    try:
        profile_a = user_a.profile
        profile_b = user_b.profile
    except Profile.DoesNotExist:
        return 0

    # Compétences de A correspondent aux lacunes de B ?
    competences_a = set(profile_a.competences.split(','))
    lacunes_b = set(profile_b.lacunes.split(','))
    matieres_communes = competences_a & lacunes_b
    score += len(matieres_communes) * 10  # 10 points par matière commune

    # Même filière ?
    if profile_a.filiere == profile_b.filiere:
        score += 20

    # Même niveau ?
    if profile_a.niveau == profile_b.niveau:
        score += 20

    # Disponibilités compatibles ?
    dispos_a = set(profile_a.disponibilites.split(','))
    dispos_b = set(profile_b.disponibilites.split(','))
    dispos_communes = dispos_a & dispos_b
    if dispos_communes:
        score += 20

    return score


def recherche_matchs(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'matching/recherche_matchs.html', {'matchs': []})
    
    user_actuel = User.objects.get(id=user_id)
    tous_les_users = User.objects.exclude(id=user_id)
    
    resultats = []
    for user in tous_les_users:
        score = calculer_score(user_actuel, user)
        if score > 0:
            resultats.append({
                'user': user,
                'score': score,
            })
    
    # Trier du score le plus élevé au plus bas
    resultats = sorted(resultats, key=lambda x: x['score'], reverse=True)
    
    return render(request, 'matching/resultats_matchs.html', {'matchs': resultats})
