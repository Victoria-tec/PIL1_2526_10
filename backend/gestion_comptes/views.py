# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import InscriptionForm, ConnexionForm
from .models import User, Profile

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