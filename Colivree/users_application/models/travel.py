from django.contrib.auth.models import User
from django.db import models
from .traveler import Traveler

class Travel(models.Model):
    voyageur = models.ForeignKey(Traveler, on_delete=models.SET_NULL, null=True)
    date_depart = models.DateTimeField()
    destination = models.CharField(max_length=255)
    capacite_disponible = models.PositiveIntegerField()
    is_verified = models.BooleanField(default=False)
    booked_senders = models.ForeignKey('Sender', on_delete=models.SET_NULL, null=True, blank=True)
    # Ajoutez d'autres champs selon vos besoins

    def __str__(self):
        return f"{self.voyageur.username} - {self.destination}"