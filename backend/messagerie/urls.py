from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_conversations, name='liste_conversations'),
    path('<int:conversation_id>/', views.detail_conversation, name='detail_conversation'),
    path('<int:conversation_id>/envoyer/', views.envoyer_message, name='envoyer_message'),
]