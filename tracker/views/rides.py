from django.db.models import F, Prefetch, Value, FloatField
from django.db.models.functions import Radians, Sin, Cos, ATan2, Sqrt, Power
from django.utils.timezone import now
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError
from ..common.permissions import IsAdmin
from ..models.rides import Ride, RideEvent
from ..serializers.rides import RideSerializer


class RideViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RideSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "id_rider__email"]
    ordering_fields = ["pickup_time"]

    def get_queryset(self):
        queryset = Ride.objects.select_related(
            "id_rider", "id_driver"
        ).prefetch_related(
            Prefetch(
                "events",
                queryset=RideEvent.objects.filter(
                    created_at__gte=now() - timedelta(hours=24)
                ),
                to_attr="prefetched_events",
            )
        )

        lat = self.request.query_params.get("lat")
        lon = self.request.query_params.get("lon")

        if lat and lon:
            try:
                user_lat = float(lat)
                user_lon = float(lon)

                if not (-90 <= user_lat <= 90) or not (-180 <= user_lon <= 180):
                    raise ValueError

                earth_radius_km = 6371

                queryset = queryset.annotate(
                    distance=(
                        2
                        * earth_radius_km
                        * ATan2(
                            Sqrt(
                                Power(
                                    Sin(Radians(F("pickup_latitude") - user_lat) / 2), 2
                                )
                                + Cos(Radians(user_lat))
                                * Cos(Radians(F("pickup_latitude")))
                                * Power(
                                    Sin(Radians(F("pickup_longitude") - user_lon) / 2),
                                    2,
                                )
                            ),
                            Sqrt(
                                1
                                - (
                                    Power(
                                        Sin(
                                            Radians(F("pickup_latitude") - user_lat) / 2
                                        ),
                                        2,
                                    )
                                    + Cos(Radians(user_lat))
                                    * Cos(Radians(F("pickup_latitude")))
                                    * Power(
                                        Sin(
                                            Radians(F("pickup_longitude") - user_lon)
                                            / 2
                                        ),
                                        2,
                                    )
                                )
                            ),
                        )
                    )
                ).order_by("distance")

            except ValueError:
                raise ValidationError(
                    {
                        "error": "Invalid latitude or longitude values. Latitude must be between -90 and 90, and longitude must be between -180 and 180."
                    }
                )

        return queryset
