from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),
    path('hub/', views.hub, name='hub'),
    path('profil/<int:user_id>/', views.profil_visiteur, name='profil_visiteur'),
    path('messagerie/', include('backend.messagerie.urls')),
    path('comptes/', include('backend.gestion_comptes.urls')),
    path('matching/', include('backend.matching.urls')),
    path('proposals/', include('backend.offres_demandes.urls')),
]
