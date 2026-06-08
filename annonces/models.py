from django.db import models
from django.conf import settings

class Proposal(models.Model):
    # Choix pour le type, la modalité et le statut
    TYPE_CHOICES = [
        ('OFFRE', 'Offre'),
        ('DEMANDE', 'Demande'),
    ]
    MODALITE_CHOICES = [
        ('PRESENTIEL', 'Présentiel'),
        ('EN_LIGNE', 'En ligne'),
        ('LES_DEUX', 'Les deux'),
    ]
    STATUT_CHOICES = [
        ('OUVERTE', 'Ouverte'),
        ('EN_COURS', 'En cours'),
        ('FERMEE', 'Fermée'),
    ]

    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='proposals'
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    matiere = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Optionnel
    disponibilite_debut = models.DateTimeField()
    disponibilite_fin = models.DateTimeField()
    modalite = models.CharField(max_length=20, choices=MODALITE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='OUVERTE')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'proposals'  # Pour forcer le nom de la table exact demandé par Imma

    def __str__(self):
        return f"{self.type} - {self.matiere} (par {self.auteur.email})"
    