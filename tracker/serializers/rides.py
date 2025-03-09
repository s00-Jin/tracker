from django.utils.timezone import now, timedelta
from rest_framework import serializers
from ..models.rides import Ride, RideEvent
from ..serializers.users import UserSerializer


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ["id", "description", "created_at"]


class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            "id",
            "status",
            "id_rider",
            "id_driver",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "todays_ride_events",
        ]

    def get_todays_ride_events(self, obj):
        last_24_hours = now() - timedelta(hours=24)

        if hasattr(obj, "prefetched_events"):
            return RideEventSerializer(
                [
                    event
                    for event in obj.prefetched_events
                    if event.created_at >= last_24_hours
                ],
                many=True,
            ).data
        return []
