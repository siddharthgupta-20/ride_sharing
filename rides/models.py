from django.db import models
from users.models import User

class Ride(models.Model):
    trip_id = models.CharField(max_length=100, unique=True)
    driver_name = models.CharField(max_length=100)
    driver_phone_number = models.CharField(max_length=15)
    cab_number = models.CharField(max_length=15)
    current_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    # start_time = models.DateTimeField()
    # end_time = models.DateTimeField(null=True, blank=True)
    traveler = models.ForeignKey(User, related_name='rides', on_delete=models.CASCADE)

    def __str__(self):
        return self.trip_id

