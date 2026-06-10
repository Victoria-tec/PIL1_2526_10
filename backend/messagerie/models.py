from django.db import models
from django.conf import settings


class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    creee_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    envoye_le = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.expediteur.get_full_name()} : {self.contenu[:30]}"
