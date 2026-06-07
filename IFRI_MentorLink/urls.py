from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Toutes les URLs de gestion_comptes seront accessibles via /comptes/
    # Exemple : /comptes/inscription/ | /comptes/connexion/ | /comptes/deconnexion/
    path('comptes/', include('backend.gestion_comptes.urls')),
    # URLs du matching : /matching/recherche/
    path('matching/', include('backend.matching.urls')),
]