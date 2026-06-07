from django.urls import path
from . import views

urlpatterns = [
    # Page de recherche de matchs
    path('recherche/', views.recherche_matchs, name='recherche_matchs'),
]  