from django.shortcuts import render
from backend.gestion_comptes.models import User, Profile
from .models import Matching

def calculer_score(user_a, user_b, offres_a=None, demandes_a=None):
    """
    Calcule le score de compatibilité entre deux utilisateurs.
    Le score est normalisé sur 100.
    Priorité haute : matières compatibles + disponibilités horaires
    Priorité basse : filière + niveau
    """
    score_brut = 0
    score_maximum = 0  # On calcule le maximum possible au fur et à mesure

    # ─────────────────────────────────────────
    # Récupération des profils des deux utilisateurs
    # Si l'un des deux n'a pas de profil → score = 0
    # ─────────────────────────────────────────
    try:
        profile_a = user_a.profile
        profile_b = user_b.profile
    except Profile.DoesNotExist:
        return 0

    # ─────────────────────────────────────────
    # PRIORITÉ HAUTE 1 — Matières compatibles
    # Compétences de A vs Lacunes de B
    # 20 points par matière commune
    # ─────────────────────────────────────────
    competences_a = set(
        [c.strip() for c in profile_a.competences.split(',') if c.strip()]
    )
    lacunes_b = set(
        [l.strip() for l in profile_b.lacunes.split(',') if l.strip()]
    )

    # Nombre de matières en commun
    matieres_communes = competences_a & lacunes_b
    points_matieres = len(matieres_communes) * 20
    score_brut += points_matieres

    # Le maximum pour les matières = nombre de lacunes de B × 20
    # (dans le meilleur des cas A couvre toutes les lacunes de B)
    score_maximum += len(lacunes_b) * 20

    # ─────────────────────────────────────────
    # PRIORITÉ HAUTE 2 — Disponibilités communes
    # 20 points si au moins une disponibilité commune
    # ─────────────────────────────────────────
    dispos_a = set(
        [d.strip() for d in profile_a.disponibilites.split(',') if d.strip()]
    )
    dispos_b = set(
        [d.strip() for d in profile_b.disponibilites.split(',') if d.strip()]
    )
    dispos_communes = dispos_a & dispos_b
    if dispos_communes:
        score_brut += 20
    score_maximum += 20  # Maximum possible pour les disponibilités = 20

    # ─────────────────────────────────────────
    # PRIORITÉ BASSE 1 — Même filière
    # 10 points
    # ─────────────────────────────────────────
    if profile_a.filiere and profile_b.filiere:
        if profile_a.filiere.strip() == profile_b.filiere.strip():
            score_brut += 10
    score_maximum += 10  # Maximum possible pour la filière = 10

    # ─────────────────────────────────────────
    # PRIORITÉ BASSE 2 — Même niveau
    # 10 points
    # ─────────────────────────────────────────
    if profile_a.niveau and profile_b.niveau:
        if profile_a.niveau.strip() == profile_b.niveau.strip():
            score_brut += 10
    score_maximum += 10  # Maximum possible pour le niveau = 10

    # ─────────────────────────────────────────
    # BONUS — Matching par formulaires
    # Si A a publié des offres ou demandes
    # On compare avec le profil de B
    # ─────────────────────────────────────────
    if offres_a:
        for offre in offres_a:
            # La compétence proposée dans l'offre
            # correspond à une lacune de B ?
            if offre.subject.strip() in lacunes_b:
                score_brut += 20
            score_maximum += 20

            # Les disponibilités du formulaire chevauchent-elles
            # les disponibilités habituelles de B ?
            if offre.disponibilite_debut and offre.disponibilite_fin:
                for dispo_b in dispos_b:
                    if dispo_b.strip():
                        score_brut += 10
                        break
                score_maximum += 10

    if demandes_a:
        for demande in demandes_a:
            # La lacune exprimée dans la demande
            # correspond à une compétence de B ?
            competences_b = set(
                [c.strip() for c in profile_b.competences.split(',') if c.strip()]
            )
            if demande.subject.strip() in competences_b:
                score_brut += 20
            score_maximum += 20

            # Les disponibilités du formulaire chevauchent-elles
            # les disponibilités habituelles de B ?
            if demande.disponibilite_debut and demande.disponibilite_fin:
                for dispo_b in dispos_b:
                    if dispo_b.strip():
                        score_brut += 10
                        break
                score_maximum += 10

    # ─────────────────────────────────────────
    # NORMALISATION — Score sur 100
    # Si score_maximum = 0 → pas de critères → score = 0
    # Sinon → score normalisé = (score_brut / score_maximum) × 100
    # ─────────────────────────────────────────
    if score_maximum == 0:
        return 0

    score_normalise = round((score_brut / score_maximum) * 100)

    # On s'assure que le score ne dépasse pas 100
    return min(score_normalise, 100)


def recherche_matchs(request):
    """
    Vue principale du matching.
    Récupère l'utilisateur connecté, compare son profil
    avec tous les autres et retourne les résultats triés.
    """
    # Vérifier si l'utilisateur est connecté
    user_id = request.session.get('user_id')
    if not user_id:
        # Si non connecté → liste vide
        return render(request, 'matching/resultats_matchs.html', {'matchs': []})

    # Récupérer l'utilisateur connecté
    user_actuel = User.objects.get(id=user_id)

    # ─────────────────────────────────────────
    # Récupérer les offres et demandes
    # de l'utilisateur connecté
    # Si le module n'est pas encore prêt → listes vides
    # ─────────────────────────────────────────
    try:
        from backend.offre_demandes.models import Offre, Demande
        offres_user = Offre.objects.filter(auteur_id=user_actuel.id)
        demandes_user = Demande.objects.filter(auteur_id=user_actuel.id)
    except:
        offres_user = []
        demandes_user = []

    # ─────────────────────────────────────────
    # Récupérer tous les autres utilisateurs
    # sauf l'utilisateur connecté
    # ─────────────────────────────────────────
    tous_les_users = User.objects.exclude(id=user_actuel.id)

    # ─────────────────────────────────────────
    # Appliquer les filtres si l'utilisateur
    # en a choisi dans le menu
    # ─────────────────────────────────────────
    filiere_filtre = request.GET.get('filiere', '')
    niveau_filtre = request.GET.get('niveau', '')
    sexe_filtre = request.GET.get('sexe', '')

    if filiere_filtre:
        # Filtrer par filière
        tous_les_users = tous_les_users.filter(
            profile__filiere=filiere_filtre
        )
    if niveau_filtre:
        # Filtrer par niveau
        tous_les_users = tous_les_users.filter(
            profile__niveau=niveau_filtre
        )
    if sexe_filtre:
        # Filtrer par sexe
        tous_les_users = tous_les_users.filter(
            profile__sexe=sexe_filtre
        )

    # ─────────────────────────────────────────
    # Calculer le score pour chaque utilisateur
    # et garder uniquement ceux avec un score > 0
    # ─────────────────────────────────────────
    resultats = []
    for user in tous_les_users:
        score = calculer_score(
            user_actuel,
            user,
            offres_a=offres_user,
            demandes_a=demandes_user
        )
        if score > 0:
            resultats.append({
                'user': user,
                'score': score,
            })

    # ─────────────────────────────────────────
    # Trier les résultats du score
    # le plus élevé au plus bas
    # ─────────────────────────────────────────
    resultats = sorted(resultats, key=lambda x: x['score'], reverse=True)

    # Envoyer les résultats à la page HTML
    return render(request, 'matching/resultats_matchs.html', {
        'matchs': resultats,
        'filiere_filtre': filiere_filtre,
        'niveau_filtre': niveau_filtre,
        'sexe_filtre': sexe_filtre,
    })