from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_proposals, name='liste_proposals'),
    path('creer/', views.creer_proposal, name='creer_proposal'),
    path('rechercher/', views.rechercher_proposals, name='rechercher_proposals'),
    path('<int:pk>/', views.detail_proposal, name='detail_proposal'),
    path('<int:pk>/repondre/', views.repondre_proposal, name='repondre_proposal'),
    path('<int:pk>/supprimer/', views.supprimer_proposal, name='supprimer_proposal'),
]