# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import InscriptionForm, ConnexionForm
from .models import User, Profile
from .forms import InscriptionForm, ConnexionForm, ReinitialisationMotDePasseForm, EmailReinitialisationForm

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.mot_de_passe = make_password(form.cleaned_data['mot_de_passe'])
            user.save()
            Profile.objects.create(user=user)
            messages.success(request, "Inscription réussie ! Connectez-vous.")
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'gestion_comptes/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data['identifiant']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                user = User.objects.get(email=identifiant)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(telephone=identifiant)
                except User.DoesNotExist:
                    messages.error(request, "Identifiant incorrect.")
                    return render(request, 'gestion_comptes/connexion.html', {'form': form})
            if check_password(mot_de_passe, user.mot_de_passe):
                request.session['user_id'] = user.id
                messages.success(request, "Connexion réussie !")
                return redirect('accueil')
            else:
                messages.error(request, "Mot de passe incorrect.")
    else:
        form = ConnexionForm()
    return render(request, 'gestion_comptes/connexion.html', {'form': form})


def deconnexion(request):
    request.session.flush()
    return redirect('connexion')

import random

def reinitialisation_mot_de_passe(request):

    # ÉTAPE 1 — L'utilisateur entre son email
    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Générer un code à 4 chiffres
            code = random.randint(1000, 9999)
            
            # Stocker le code et l'email en session
            request.session['code_reinitialisation'] = code
            request.session['email_reinitialisation'] = email

            # Envoyer le code via la messagerie interne
            try:
                from backend.messagerie.models import Conversation, Message
                
                # Créer ou récupérer une conversation
                # entre l'app et l'utilisateur
                conversation, created = Conversation.objects.get_or_create(
                    id=0  # Conversation système
                )
                conversation.participants.add(user)
                
                # Envoyer le message avec le code
                Message.objects.create(
                    conversation=conversation,
                    expediteur=user,
                    contenu=f"Votre code de réinitialisation est : {code}"
                )
                messages.info(request, "Un code a été envoyé dans votre messagerie !")
                
            except:
                # Si messagerie pas encore disponible
                # on affiche le code directement
                messages.info(request, f"Votre code est : {code}")

            return render(request, 'gestion_comptes/reinitialisation_mot_de_passe.html', {
                'etape': 2,
                'form': ReinitialisationMotDePasseForm()
            })

        except User.DoesNotExist:
            messages.error(request, "Aucun compte trouvé avec cet email.")
            return render(request, 'gestion_comptes/reinitialisation_mot_de_passe.html', {
                'etape': 1,
                'form': EmailReinitialisationForm()
            })

    # ÉTAPE 2 — L'utilisateur entre le code + nouveau mot de passe
    elif request.method == 'POST' and 'code' in request.POST:
        code_saisi = int(request.POST.get('code'))
        code_session = request.session.get('code_reinitialisation')
        email = request.session.get('email_reinitialisation')
        nouveau_mot_de_passe = request.POST.get('nouveau_mot_de_passe')
        confirmation = request.POST.get('confirmation_nouveau_mot_de_passe')

        # Vérifier que les mots de passe correspondent
        if nouveau_mot_de_passe != confirmation:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'gestion_comptes/reinitialisation_mot_de_passe.html', {
                'etape': 2,
                'form': ReinitialisationMotDePasseForm()
            })

        # Vérifier que le code est correct
        if code_saisi == code_session:
            user = User.objects.get(email=email)
            user.mot_de_passe = make_password(nouveau_mot_de_passe)
            user.save()
            
            # Supprimer le code de la session
            del request.session['code_reinitialisation']
            del request.session['email_reinitialisation']
            
            messages.success(request, "Mot de passe modifié avec succès !")
            return redirect('connexion')
        else:
            messages.error(request, "Code incorrect. Veuillez réessayer.")
            return render(request, 'gestion_comptes/reinitialisation_mot_de_passe.html', {
                'etape': 2,
                'form': ReinitialisationMotDePasseForm()
            })

    # Afficher la page initiale
    else:
        return render(request, 'gestion_comptes/reinitialisation_mot_de_passe.html', {
            'etape': 1,
            'form': EmailReinitialisationForm()
        })