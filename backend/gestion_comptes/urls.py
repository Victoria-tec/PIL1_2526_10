from django.urls import path
from . import views

urlpatterns = [
    # Page d'inscription
    path('inscription/', views.inscription, name='inscription'),
    # Page de finalisation du profil après inscription
    path('completer-profil/', views.completer_profil, name='completer_profil'),
    # Page de connexion
    path('connexion/', views.connexion, name='connexion'),
    # Page de déconnexion
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    # Page de réinitialisation du mot de passe
    path('reinitialisation/', views.reinitialisation_mot_de_passe, name='reinitialisation_mot_de_passe'),
    # Page de profil
    path('profil/', views.profil, name='profil'),
    # API de sauvegarde du profil
    path('profil/sauvegarder/', views.sauvegarder_profil, name='sauvegarder_profil'),
]
