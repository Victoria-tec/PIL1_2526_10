# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import InscriptionForm, ConnexionForm
from .models import User, Profile
from .forms import InscriptionForm, ConnexionForm, ReinitialisationMotDePasseForm, EmailReinitialisationForm
import random

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
            # Stocker en session
            request.session['code_reinitialisation'] = code
            request.session['email_reinitialisation'] = email
            # Afficher le code sur la page
            messages.info(request, f"Votre code de réinitialisation est : {code}")
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

        if nouveau_mot_de_passe != confirmation:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'gestion_comptes/reinitialisation_mot_de_passe.html', {
                'etape': 2,
                'form': ReinitialisationMotDePasseForm()
            })

        if code_saisi == code_session:
            user = User.objects.get(email=email)
            user.mot_de_passe = make_password(nouveau_mot_de_passe)
            user.save()
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

    # Page initiale
    else:
        return render(request, 'gestion_comptes/reinitialisation_mot_de_passe.html', {
            'etape': 1,
            'form': EmailReinitialisationForm()
        })


