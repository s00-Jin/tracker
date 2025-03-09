from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ride(models.Model):
    STATUS_CHOICES = [
        ("en-route", "En Route"),
        ("pickup", "Pickup"),
        ("dropoff", "Dropoff"),
    ]

    id_rider = models.ForeignKey(
        User, related_name="rides_as_rider", on_delete=models.CASCADE
    )
    id_driver = models.ForeignKey(
        User, related_name="rides_as_driver", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"Ride {self.id} - {self.status}"


class RideEvent(models.Model):
    id_ride = models.ForeignKey(Ride, related_name="events", on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RideEvent {self.id} - {self.description}"
