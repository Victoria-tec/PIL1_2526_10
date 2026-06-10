from django.db import models
from backend.gestion_comptes.models import User

class Matching(models.Model):
    user1 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='matchings_en_tant_que_user1'
    )
    user2 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='matchings_en_tant_que_user2'
    )
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match {self.user1.prenom} ↔ {self.user2.prenom} : {self.score} points"
    