from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    mot_de_passe = models.CharField(max_length=255)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    filiere = models.CharField(max_length=100)
    SEXE_CHOICES = [
    ('M', 'Masculin'),
    ('F', 'Féminin'),
    ]
    niveau = models.CharField(max_length=50)
    competences = models.TextField(blank=True)
    lacunes = models.TextField(blank=True)
    disponibilites = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, blank=True)
    


    def __str__(self):
        return f"Profil de {self.user.prenom}"