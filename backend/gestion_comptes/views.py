import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import InscriptionForm, ConnexionForm, ReinitialisationMotDePasseForm, EmailReinitialisationForm
from gestion_comptes.models import Profile
import random

User = get_user_model()


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['mot_de_passe'])
            user.save()
            sexe = request.POST.get('sexe', '')
            Profile.objects.create(user=user, sexe=sexe)
            user = authenticate(request, username=user.email, password=form.cleaned_data['mot_de_passe'])
            if user:
                login(request, user)
            messages.success(request, "Inscription réussie ! Complétez votre profil.")
            return redirect('completer_profil')
    else:
        form = InscriptionForm()
    return render(request, 'gestion_comptes/inscription.html', {'form': form})


@login_required
def completer_profil(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.filiere = request.POST.get('filiere', '')
        profile.niveau = request.POST.get('niveau', '')
        profile.competences = request.POST.get('competences', '')
        profile.lacunes = request.POST.get('lacunes', '')
        profile.disponibilites = request.POST.get('disponibilites', '')
        profile.save()
        messages.success(request, "Profil complété avec succès !")
        return redirect('hub')
    return render(request, 'gestion_comptes/completer_profil.html')


def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data['identifiant']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            user = authenticate(request, username=identifiant, password=mot_de_passe)
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect('hub')
            else:
                messages.error(request, "Identifiant ou mot de passe incorrect.")
    else:
        form = ConnexionForm()
    return render(request, 'gestion_comptes/connexion.html', {'form': form})


def deconnexion(request):
    logout(request)
    return redirect('connexion')


def reinitialisation_mot_de_passe(request):
    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            code = random.randint(1000, 9999)
            request.session['code_reinitialisation'] = code
            request.session['email_reinitialisation'] = email
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
            user.set_password(nouveau_mot_de_passe)
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

    else:
        return render(request, 'gestion_comptes/reinitialisation_mot_de_passe.html', {
            'etape': 1,
            'form': EmailReinitialisationForm()
        })


@login_required
def profil(request):
    profile = request.user.profile
    return render(request, 'profil.html', {'user': request.user})


@login_required
def sauvegarder_profil(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)

        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'email' in data:
            user.email = data['email']
        if 'telephone' in data:
            user.telephone = data['telephone']
        user.save()

        profile = user.profile
        if 'filiere' in data:
            profile.filiere = data['filiere']
        if 'niveau' in data:
            profile.niveau = data['niveau']
        if 'competences' in data:
            profile.competences = data['competences']
        if 'lacunes' in data:
            profile.lacunes = data['lacunes']
        if 'disponibilites' in data:
            profile.disponibilites = data['disponibilites']
        if 'bio' in data:
            profile.bio = data['bio']
        if 'sexe' in data:
            profile.sexe = data['sexe']
        profile.save()

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'erreur'}, status=400)
