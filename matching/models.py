from django.db import models
from django.conf import settings

class Matching(models.Model):
    # Clé étrangère vers le premier utilisateur
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='matchings_as_user1'
    )
    # Clé étrangère vers le deuxième utilisateur
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='matchings_as_user2'
    )
    score = models.IntegerField()  # Pour stocker le score de correspondance
    date = models.DateTimeField(auto_now_add=True)  # Met la date du jour automatiquement

    def __str__(self):
        return f"Matching entre {self.user1.email} et {self.user2.email} (Score: {self.score})"