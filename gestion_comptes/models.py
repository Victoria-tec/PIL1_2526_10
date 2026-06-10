from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Profile(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    filiere = models.CharField(max_length=100, blank=True, null=True)
    niveau = models.CharField(max_length=50, blank=True, null=True)
    competences = models.TextField(blank=True, null=True)
    lacunes = models.TextField(blank=True, null=True)
    disponibilites = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles_photos/', blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, blank=True)

    def __str__(self):
        return f"Profil de {self.user.email}"
