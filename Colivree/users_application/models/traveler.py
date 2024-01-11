from django.contrib.auth.models import User
from django.db import models
from .user import MyUser

class Traveler(MyUser):
    
    voyages = models.ManyToManyField('Voyage', related_name='voyageurs', blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username