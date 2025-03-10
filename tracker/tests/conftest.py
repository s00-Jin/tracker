import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils.timezone import now, timedelta

from ..models.rides import Ride, RideEvent

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

User = get_user_model()


@pytest.fixture
def create_user(db):
    """Fixture to create a user with a specified role."""

    def make_user(email, role, password="testpass123"):
        return User.objects.create_user(email=email, role=role, password=password)

    return make_user


@pytest.fixture
def create_ride(db, create_user):
    """Fixture to create a ride between a rider and a driver."""

    def make_ride():
        rider = create_user("rider@example.com", "rider")
        driver = create_user("driver@example.com", "driver")
        return Ride.objects.create(
            id_rider=rider,
            id_driver=driver,
            status="en-route",
            pickup_latitude=12.34,
            pickup_longitude=56.78,
            dropoff_latitude=90.12,
            dropoff_longitude=34.56,
            pickup_time=now(),
        )

    return make_ride


@pytest.fixture
def create_ride_event(db, create_ride):
    """Fixture to create a ride event for a ride."""

    def make_ride_event():
        ride = create_ride()
        return RideEvent.objects.create(
            id_ride=ride,
            description="Ride started",
            created_at=now() - timedelta(hours=2),
        )

    return make_ride_event


@pytest.fixture
def admin_user(db):
    """Fixture to create an admin user."""
    return User.objects.create_superuser(
        email="admin@example.com",
        password="AdminPassword123",
        role="admin",
    )


@pytest.fixture
def rider_user(db):
    """Fixture to create a rider user."""
    return User.objects.create_user(
        email="rider@example.com",
        password="RiderPassword123",
        role="rider",
        phone_number="1234567890",
    )


@pytest.fixture
def driver_user(db):
    """Fixture to create a driver user."""
    return User.objects.create_user(
        email="driver@example.com",
        password="DriverPassword123",
        role="driver",
        phone_number="0987654321",
    )


@pytest.fixture
def ride(db, rider_user, driver_user):
    """Fixture to create a sample ride."""
    return Ride.objects.create(
        id_rider=rider_user,
        id_driver=driver_user,
        status="pickup",
        pickup_latitude=37.7749,
        pickup_longitude=-122.4194,
        dropoff_latitude=37.7849,
        dropoff_longitude=-122.4094,
        pickup_time=now(),
    )


@pytest.fixture
def ride_event(db, ride):
    """Fixture to create a ride event within the last 24 hours."""
    return RideEvent.objects.create(
        id_ride=ride,
        description="Ride started",
        created_at=now() - timedelta(hours=2),
    )


@pytest.fixture
def auth_client(db, admin_user):
    """Fixture to authenticate an admin user with Django test client."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
