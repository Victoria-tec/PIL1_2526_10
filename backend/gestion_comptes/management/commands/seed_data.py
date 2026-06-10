from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from gestion_comptes.models import Profile
from backend.offres_demandes.models import Proposal
from backend.matching.models import Matching
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée des données de test pour le matching'

    def handle(self, *args, **options):
        now = timezone.now()

        users_data = [
            {
                'email': 'ama.coulibaly@etud.ifri.uac.bj',
                'first_name': 'Ama',
                'last_name': 'Coulibaly',
                'telephone': '+229 01 00 00 01',
                'filiere': 'GL',
                'niveau': 'M1',
                'competences': 'Python, Algorithmique, Git, Développement web, Bases de données',
                'lacunes': 'Machine Learning, Réseaux',
                'disponibilites': 'Lundi matin, Mercredi après-midi, Vendredi matin',
                'sexe': 'F',
            },
            {
                'email': 'jean.traore@etud.ifri.uac.bj',
                'first_name': 'Jean',
                'last_name': 'Traoré',
                'telephone': '+229 01 00 00 02',
                'filiere': 'IA',
                'niveau': 'M2',
                'competences': 'Machine Learning, Python, Algorithmique, Mathématiques',
                'lacunes': 'Développement web, Réseaux, Bases de données',
                'disponibilites': 'Lundi matin, Mardi soir, Jeudi après-midi',
                'sexe': 'M',
            },
            {
                'email': 'fatou.sylla@etud.ifri.uac.bj',
                'first_name': 'Fatou',
                'last_name': 'Sylla',
                'telephone': '+229 01 00 00 03',
                'filiere': 'IA',
                'niveau': 'L3',
                'competences': 'JavaScript, Algorithmique, Développement web, Git',
                'lacunes': 'Machine Learning, Python, Mathématiques',
                'disponibilites': 'Mardi soir, Mercredi après-midi, Samedi matin',
                'sexe': 'F',
            },
            {
                'email': 'pierre.adjovi@etud.ifri.uac.bj',
                'first_name': 'Pierre',
                'last_name': 'Adjovi',
                'telephone': '+229 01 00 00 04',
                'filiere': 'GL',
                'niveau': 'L2',
                'competences': 'C/C++, Algorithmique, Linux, Git',
                'lacunes': 'Python, Développement web, Bases de données',
                'disponibilites': 'Lundi matin, Jeudi après-midi, Vendredi matin',
                'sexe': 'M',
            },
            {
                'email': 'grace.hounkpe@etud.ifri.uac.bj',
                'first_name': 'Grâce',
                'last_name': 'Hounkpè',
                'telephone': '+229 01 00 00 05',
                'filiere': 'SI',
                'niveau': 'M1',
                'competences': 'Bases de données, Réseaux, Linux, Algorithmique',
                'lacunes': 'Python, JavaScript, Développement web',
                'disponibilites': 'Lundi après-midi, Mardi soir, Mercredi matin',
                'sexe': 'F',
            },
            {
                'email': 'olivier.koffi@etud.ifri.uac.bj',
                'first_name': 'Olivier',
                'last_name': 'Koffi',
                'telephone': '+229 01 00 00 06',
                'filiere': 'SE_IoT',
                'niveau': 'L3',
                'competences': 'C/C++, Python, Réseaux, Linux',
                'lacunes': 'Algorithmique, Bases de données, JavaScript',
                'disponibilites': 'Mercredi après-midi, Jeudi soir, Samedi matin',
                'sexe': 'M',
            },
            {
                'email': 'marie.adanle@etud.ifri.uac.bj',
                'first_name': 'Marie',
                'last_name': 'Adanlè',
                'telephone': '+229 01 00 00 07',
                'filiere': 'IM',
                'niveau': 'M2',
                'competences': 'Mathématiques, Algorithmique, Python, Machine Learning',
                'lacunes': 'Développement web, Réseaux, Git',
                'disponibilites': 'Lundi matin, Mardi matin, Jeudi après-midi',
                'sexe': 'F',
            },
            {
                'email': 'sami.diallo@etud.ifri.uac.bj',
                'first_name': 'Sami',
                'last_name': 'Diallo',
                'telephone': '+229 01 00 00 08',
                'filiere': 'GL',
                'niveau': 'L1',
                'competences': '',
                'lacunes': 'Algorithmique, Python, C/C++, Git, Développement web, Bases de données',
                'disponibilites': 'Lundi toute la journée, Mercredi toute la journée, Vendredi matin',
                'sexe': 'M',
            },
            {
                'email': 'victoria.tovihouande@etud.ifri.uac.bj',
                'first_name': 'Victoria',
                'last_name': 'TOVIHOUANDE',
                'telephone': '+229 01 00 00 09',
                'filiere': 'IA',
                'niveau': 'L1',
                'competences': 'Bases de données',
                'lacunes': 'Python',
                'disponibilites': 'Lundi matin, Mercredi après-midi, Vendredi matin',
                'sexe': 'F',
            },
        ]

        proposals_data = [
            {'email': 'ama.coulibaly@etud.ifri.uac.bj', 'type': 'OFFRE', 'matiere': 'Développement web',
             'description': 'Je propose du soutien en développement web (HTML/CSS/JS).', 'debut': 1, 'fin': 90},
            {'email': 'ama.coulibaly@etud.ifri.uac.bj', 'type': 'OFFRE', 'matiere': 'Algorithmique',
             'description': 'Aide en algorithmique et structures de données.', 'debut': 2, 'fin': 60},
            {'email': 'jean.traore@etud.ifri.uac.bj', 'type': 'OFFRE', 'matiere': 'Machine Learning',
             'description': 'Je peux aider avec les fondamentaux du Machine Learning.', 'debut': 1, 'fin': 120},
            {'email': 'fatou.sylla@etud.ifri.uac.bj', 'type': 'DEMANDE', 'matiere': 'Python',
             'description': 'Débutante en Python, besoin d\'un mentor pour m\'accompagner.', 'debut': 3, 'fin': 60},
            {'email': 'fatou.sylla@etud.ifri.uac.bj', 'type': 'DEMANDE', 'matiere': 'Machine Learning',
             'description': 'Je veux apprendre le Machine Learning.', 'debut': 5, 'fin': 90},
            {'email': 'pierre.adjovi@etud.ifri.uac.bj', 'type': 'DEMANDE', 'matiere': 'Python',
             'description': 'Besoin d\'aide pour monter en compétence en Python.', 'debut': 1, 'fin': 45},
            {'email': 'pierre.adjovi@etud.ifri.uac.bj', 'type': 'DEMANDE', 'matiere': 'Développement web',
             'description': 'Je cherche un mentor en développement web.', 'debut': 2, 'fin': 60},
            {'email': 'grace.hounkpe@etud.ifri.uac.bj', 'type': 'OFFRE', 'matiere': 'Bases de données',
             'description': 'Soutien en bases de données (SQL, conception).', 'debut': 1, 'fin': 90},
            {'email': 'olivier.koffi@etud.ifri.uac.bj', 'type': 'OFFRE', 'matiere': 'C/C++',
             'description': 'Je propose du mentorat en programmation C et C++.', 'debut': 2, 'fin': 60},
            {'email': 'marie.adanle@etud.ifri.uac.bj', 'type': 'OFFRE', 'matiere': 'Mathématiques',
             'description': 'Aide en mathématiques pour informatique.', 'debut': 1, 'fin': 90},
            {'email': 'sami.diallo@etud.ifri.uac.bj', 'type': 'DEMANDE', 'matiere': 'Algorithmique',
             'description': 'Je débute, besoin d\'un mentor en algorithmique.', 'debut': 1, 'fin': 120},
            {'email': 'sami.diallo@etud.ifri.uac.bj', 'type': 'DEMANDE', 'matiere': 'Python',
             'description': 'Je veux apprendre Python depuis zéro.', 'debut': 1, 'fin': 90},
        ]

        for data in users_data:
            email = data.pop('email')
            filiere = data.pop('filiere')
            niveau = data.pop('niveau')
            competences = data.pop('competences')
            lacunes = data.pop('lacunes')
            disponibilites = data.pop('disponibilites')
            sexe = data.pop('sexe')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'telephone': data['telephone'],
                }
            )
            if created:
                user.set_password('test1234')
                user.save()
                self.stdout.write(f"  Créé utilisateur : {user.email}")

            profile, p_created = Profile.objects.get_or_create(user=user)
            profile.filiere = filiere
            profile.niveau = niveau
            profile.competences = competences
            profile.lacunes = lacunes
            profile.disponibilites = disponibilites
            profile.sexe = sexe
            profile.save()
            if p_created:
                self.stdout.write(f"  Créé profil pour : {user.email}")

        for data in proposals_data:
            email = data.pop('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.stdout.write(f"  Utilisateur {email} introuvable, skipping...")
                continue

            debut = data.pop('debut')
            fin = data.pop('fin')
            Proposal.objects.create(
                auteur=user,
                type=data['type'],
                matiere=data['matiere'],
                description=data['description'],
                disponibilite_debut=now + timedelta(days=debut),
                disponibilite_fin=now + timedelta(days=fin),
                modalite='LES_DEUX',
                statut='OUVERTE',
            )
            self.stdout.write(f"  Créée {data['type']} : {data['matiere']} par {email}")

        matches_data = [
            {'email1': 'ama.coulibaly@etud.ifri.uac.bj', 'email2': 'jean.traore@etud.ifri.uac.bj', 'score': 85, 'statut': 'VALIDE', 'matiere': 'Développement web'},
            {'email1': 'jean.traore@etud.ifri.uac.bj', 'email2': 'fatou.sylla@etud.ifri.uac.bj', 'score': 92, 'statut': 'EN_ATTENTE', 'matiere': 'Machine Learning'},
            {'email1': 'pierre.adjovi@etud.ifri.uac.bj', 'email2': 'ama.coulibaly@etud.ifri.uac.bj', 'score': 70, 'statut': 'EN_ATTENTE', 'matiere': 'Python'},
            {'email1': 'sami.diallo@etud.ifri.uac.bj', 'email2': 'ama.coulibaly@etud.ifri.uac.bj', 'score': 85, 'statut': 'EN_ATTENTE', 'matiere': 'Algorithmique'},
        ]
        for m in matches_data:
            try:
                u1 = User.objects.get(email=m['email1'])
                u2 = User.objects.get(email=m['email2'])
            except User.DoesNotExist:
                continue
            Matching.objects.get_or_create(
                user1=u1, user2=u2,
                defaults={'score': m['score'], 'statut': m['statut'], 'matiere': m['matiere']}
            )
            self.stdout.write(f"  Match {m['statut']} : {m['email1']} <-> {m['email2']} sur {m['matiere']} ({m['score']}%)")

        self.stdout.write(self.style.SUCCESS(f'\nSeed terminé ! {len(users_data)} utilisateurs, {len(proposals_data)} propositions, {len(matches_data)} matchs créés.'))
        self.stdout.write(self.style.SUCCESS('Mot de passe pour tous : test1234'))
