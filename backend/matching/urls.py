from django.urls import path
from . import views

urlpatterns = [
    path('recherche/', views.recherche_matchs, name='recherche_matchs'),
    path('accepter/', views.accepter_match, name='accepter_match'),
    path('repondre/', views.repondre_match, name='repondre_match'),
]  