from django.urls import path
from . import views

urlpatterns = [
    # Page d'inscription
    path('inscription/', views.inscription, name='inscription'),
    # Page de connexion
    path('connexion/', views.connexion, name='connexion'),
    # Page de déconnexion
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    # Page de réinitialisation du mot de passe
    path('reinitialisation/', views.reinitialisation_mot_de_passe, name='reinitialisation_mot_de_passe'),
]
