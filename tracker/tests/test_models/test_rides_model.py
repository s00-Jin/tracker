import pytest
from tracker.models.rides import RideEvent


@pytest.mark.django_db
def test_create_ride(create_ride):
    ride = create_ride()
    assert ride.status == "en-route"
    assert ride.id_rider.email == "rider@example.com"
    assert ride.id_driver.email == "driver@example.com"


@pytest.mark.django_db
def test_create_ride_event(create_ride):
    ride = create_ride()
    event = RideEvent.objects.create(id_ride=ride, description="Ride started")
    assert event.id_ride == ride
    assert event.description == "Ride started"
