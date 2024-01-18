# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    # Ajoutez des champs supplémentaires si nécessaire
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.username
    

class Traveler(MyUser):
    
    voyages = models.ManyToManyField('Voyage', related_name='voyageurs', blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class Sender(MyUser):

    booked_travels = models.ManyToManyField('Travel', related_name='booked_senders', blank=True)  
    is_verified = models.BooleanField(default=False)
    #Capacité demandée <--
    def __str__(self):
        return self.username
    


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