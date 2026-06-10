from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from gestion_comptes.models import Profile
from backend.offres_demandes.models import Proposal
from .models import Matching
from datetime import datetime

User = get_user_model()


def _split(value):
    if not value:
        return set()
    if ',' in value:
        return set([v.strip() for v in value.split(',') if v.strip()])
    return set([v.strip() for v in value.split() if v.strip()])


def _parse_dispos(value):
    """Parse disponibility : retourne (ranges_datetime, textes_set)."""
    if not value:
        return [], set()
    items = [v.strip() for v in value.replace(';', ',').split(',') if v.strip()]
    date_ranges = []
    text_items = set()
    for item in items:
        if 'T' in item and ' - ' in item:
            parts = item.split(' - ')
            if len(parts) == 2:
                try:
                    start = datetime.fromisoformat(parts[0].strip())
                    end = datetime.fromisoformat(parts[1].strip())
                    date_ranges.append((start, end))
                    continue
                except ValueError:
                    pass
        text_items.add(item)
    return date_ranges, text_items


def _dispos_overlap(dispos_a, dispos_b):
    """Retourne (nb_chevauchements, nb_total_possible)."""
    items_a = [v.strip() for v in dispos_a.replace(';', ',').split(',') if v.strip()] if dispos_a else []
    items_b = [v.strip() for v in dispos_b.replace(';', ',').split(',') if v.strip()] if dispos_b else []
    if not items_a or not items_b:
        return (0, 0)
    ranges_a, texts_a = _parse_dispos(dispos_a)
    ranges_b, texts_b = _parse_dispos(dispos_b)
    overlap = len(texts_a & texts_b)
    for r1 in ranges_a:
        for r2 in ranges_b:
            if r1[0] < r2[1] and r2[0] < r1[1]:
                overlap += 1
    return (overlap, max(len(items_a), len(items_b)))


NIVEAUX_ORDER = {'L1': 1, 'L2': 2, 'L3': 3, 'M1': 4, 'M2': 5}


def _calculer_score_dir(user_a, user_b, proposals_a=None):
    """Calcule le score dans un sens (non symétrique)."""
    score_brut = 0
    score_maximum = 0

    try:
        profile_a = user_a.profile
        profile_b = user_b.profile
    except Profile.DoesNotExist:
        return 0

    competences_a = _split(profile_a.competences)
    lacunes_b = _split(profile_b.lacunes)

    matieres_communes = competences_a & lacunes_b
    points_matieres = len(matieres_communes) * 35
    score_brut += points_matieres
    score_maximum += len(lacunes_b) * 35

    overlap, max_dispo = _dispos_overlap(profile_a.disponibilites, profile_b.disponibilites)
    if max_dispo > 0:
        score_brut += round((overlap / max_dispo) * 40)
    score_maximum += 40

    if profile_a.filiere and profile_b.filiere:
        if profile_a.filiere.strip() == profile_b.filiere.strip():
            score_brut += 10
    score_maximum += 10

    if profile_a.niveau and profile_b.niveau:
        na = NIVEAUX_ORDER.get(profile_a.niveau.strip(), 0)
        nb = NIVEAUX_ORDER.get(profile_b.niveau.strip(), 0)
        if na != nb:
            score_brut += 15
        else:
            score_brut += 5
    score_maximum += 15

    if proposals_a:
        for proposal in proposals_a:
            if proposal.type == 'OFFRE':
                if proposal.matiere.strip() in lacunes_b:
                    score_brut += 35
                score_maximum += 35
            elif proposal.type == 'DEMANDE':
                competences_b = _split(profile_b.competences)
                if proposal.matiere.strip() in competences_b:
                    score_brut += 35
                score_maximum += 35

    if score_maximum == 0:
        return 0

    score_normalise = round((score_brut / score_maximum) * 100)
    return min(score_normalise, 100)


def calculer_score(user_a, user_b, proposals_a=None):
    """Score symétrique : moyenne des deux sens."""
    score_ab = _calculer_score_dir(user_a, user_b, proposals_a)
    score_ba = _calculer_score_dir(user_b, user_a, None)
    return (score_ab + score_ba) // 2


def trouver_matiere(user_a, user_b):
    """Retourne la première matière commune compétence↔lacune dans les deux sens."""
    try:
        pa = user_a.profile
        pb = user_b.profile
    except Profile.DoesNotExist:
        return ''
    commun = (_split(pa.competences) & _split(pb.lacunes)) | (_split(pb.competences) & _split(pa.lacunes))
    return list(commun)[0] if commun else ''


def recherche_matchs(request):
    if not request.user.is_authenticated:
        return render(request, 'resultats_matching.html', {'matchs': []})

    user_actuel = request.user

    proposals_user = Proposal.objects.filter(auteur_id=user_actuel.id)

    tous_les_users = User.objects.exclude(id=user_actuel.id)

    filiere_filtre = request.GET.get('filiere', '')
    niveau_filtre = request.GET.get('niveau', '')
    sexe_filtre = request.GET.get('sexe', '')

    if filiere_filtre:
        tous_les_users = tous_les_users.filter(
            profile__filiere__iexact=filiere_filtre
        )
    if niveau_filtre:
        tous_les_users = tous_les_users.filter(
            profile__niveau__iexact=niveau_filtre
        )
    if sexe_filtre:
        tous_les_users = tous_les_users.filter(
            profile__sexe__iexact=sexe_filtre
        )

    resultats = []
    for user in tous_les_users:
        score = calculer_score(
            user_actuel,
            user,
            proposals_a=proposals_user
        )
        if score > 0:
            resultats.append({
                'user': user,
                'score': score,
                'matiere': trouver_matiere(user_actuel, user),
            })

    resultats = sorted(resultats, key=lambda x: x['score'], reverse=True)

    a_offre = proposals_user.filter(type='OFFRE').exists()
    a_demande = proposals_user.filter(type='DEMANDE').exists()
    if a_offre and not a_demande:
        titre = 'Veuillez choisir un mentoré'
    elif a_demande and not a_offre:
        titre = 'Veuillez choisir un mentor'
    else:
        titre = 'Matchs proposés'

    return render(request, 'resultats_matching.html', {
        'matchs': resultats,
        'filiere_filtre': filiere_filtre,
        'niveau_filtre': niveau_filtre,
        'sexe_filtre': sexe_filtre,
        'titre': titre,
    })


@login_required
@require_POST
def accepter_match(request):
    import json
    data = json.loads(request.body)
    cible_id = data.get('user_id')
    score = data.get('score', 0)
    matiere = data.get('matiere', '')
    try:
        cible = User.objects.get(id=cible_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'erreur', 'message': 'Utilisateur introuvable'}, status=404)

    existants = Matching.objects.filter(
        user1=request.user, user2=cible, statut__in=['EN_ATTENTE', 'VALIDE']
    ) | Matching.objects.filter(
        user1=cible, user2=request.user, statut__in=['EN_ATTENTE', 'VALIDE']
    )
    if existants.exists():
        return JsonResponse({'status': 'deja_existant'})
    Matching.objects.filter(
        user1=request.user, user2=cible
    ).delete()
    Matching.objects.filter(
        user1=cible, user2=request.user
    ).delete()

    Matching.objects.create(user1=request.user, user2=cible, score=score, statut='EN_ATTENTE', matiere=matiere)
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def repondre_match(request):
    import json
    data = json.loads(request.body)
    match_id = data.get('match_id')
    action = data.get('action')
    try:
        match = Matching.objects.get(id=match_id)
    except Matching.DoesNotExist:
        return JsonResponse({'status': 'erreur', 'message': 'Match introuvable'}, status=404)

    if request.user not in (match.user1, match.user2):
        return JsonResponse({'status': 'erreur', 'message': 'Pas votre match'}, status=403)

    if action == 'valider':
        match.statut = 'VALIDE'
    elif action == 'rejeter':
        match.statut = 'REJETE'
    elif action == 'terminer':
        match.statut = 'TERMINE'
    elif action == 'annuler':
        match.statut = 'REJETE'
    else:
        return JsonResponse({'status': 'erreur', 'message': 'Action inconnue'}, status=400)
    match.save()
    return JsonResponse({'status': 'ok'})
