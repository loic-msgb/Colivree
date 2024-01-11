# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    # Ajoutez des champs supplémentaires si nécessaire
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.username
