from django.db import models
from django.conf import settings


class Proposal(models.Model):
    TYPE_CHOICES = [
        ('OFFRE', 'Offre de mentorat'),
        ('DEMANDE', 'Demande de mentorat'),
    ]
    FORMAT_CHOICES = [
        ('PRESENTIEL', 'Présentiel'),
        ('EN_LIGNE', 'En ligne'),
        ('LES_DEUX', 'Les deux'),
    ]
    STATUT_CHOICES = [
        ('OUVERTE', 'Ouverte'),
        ('FERMEE', 'Fermée'),
        ('EN_COURS', 'En cours'),
    ]
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    matiere = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    disponibilite_debut = models.DateTimeField()
    disponibilite_fin = models.DateTimeField()
    modalite = models.CharField(max_length=15, choices=FORMAT_CHOICES)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='OUVERTE')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.matiere} par {self.auteur}"
