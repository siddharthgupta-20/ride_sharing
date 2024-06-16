from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255,unique = True)
    password = models.CharField(max_length = 255)
    is_traveler = models.BooleanField(default=False)  #if not null will have the value of ride_id
    is_traveler_companion = models.BooleanField(default=False) #if not null will have the value of traveler_id
    is_admin = models.BooleanField(default=False)
    ride_id = models.CharField(max_length=100,null = True) 
    traveler_id = models.CharField(max_length=100, null = True)
    phone_number = models.CharField(max_length=100,null = True)
    end_location = models.CharField(max_length=100,null = True)
    
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.username