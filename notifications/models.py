from django.db import models
from rides.models import Ride
from users.models import User

class Notification(models.Model):
    ride = models.ForeignKey(Ride, related_name='notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}"
