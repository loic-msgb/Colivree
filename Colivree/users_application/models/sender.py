from django.contrib.auth.models import User
from django.db import models
from .user import MyUser

class Sender(MyUser):

    booked_travels = models.ManyToManyField('Travel', related_name='booked_senders', blank=True)  
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username