from django.db import models
from django.conf import settings


class Matching(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDE', 'Validé'),
        ('TERMINE', 'Terminé'),
        ('REJETE', 'Rejeté'),
    ]
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='matchings_en_tant_que_user1'
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='matchings_en_tant_que_user2'
    )
    score = models.IntegerField(default=0)
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='EN_ATTENTE')
    matiere = models.CharField(max_length=100, blank=True, default='')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match {self.user1.get_full_name()} ↔ {self.user2.get_full_name()} : {self.score} points"
