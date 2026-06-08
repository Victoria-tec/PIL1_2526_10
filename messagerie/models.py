from django.db import models
from django.conf import settings

class Conversation(models.Model):
    # Clé étrangère vers l'utilisateur qui est le mentor
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='conversations_as_mentor'
    )
    # Clé étrangère vers l'utilisateur qui est le mentoré
    mentore = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='conversations_as_mentore'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation entre Mentor ({self.mentor.email}) et Mentoré ({self.mentore.email})"


class Message(models.Model):
    # Un message appartient obligatoirement à une conversation
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    # L'expéditeur du message
    expediteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='messages_envoyes'
    )
    contenu = models.TextField()  # Texte du message
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.expediteur.email} à {self.date_envoi}"