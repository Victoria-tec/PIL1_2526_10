from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messagerie/', include('backend.messagerie.urls')),
    path('comptes/', include('backend.gestion_comptes.urls')),
    path('matching/', include('backend.matching.urls')),
]