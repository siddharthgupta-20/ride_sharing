from django.db import models
from rides.models import Ride
from users.models import User

class Feedback(models.Model):
    ride = models.ForeignKey(Ride, related_name='feedback', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='feedback', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for ride {self.ride.trip_id}"
