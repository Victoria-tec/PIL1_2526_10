from django.urls import path
from . import views

urlpatterns = [
    # Page d'inscription
    path('inscription/', views.inscription, name='inscription'),
    # Page de connexion
    path('connexion/', views.connexion, name='connexion'),
    # Page de déconnexion
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]
