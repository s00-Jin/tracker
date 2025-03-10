import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRideViewSet:
    def test_admin_can_access_rides(self, auth_client, ride):
        """Test that an admin can view the ride list"""
        url = reverse("ride-list")
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "pickup"

    def test_filter_by_status(self, auth_client, ride):
        """Test filtering rides by status"""
        url = reverse("ride-list") + "?status=pickup"
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "pickup"

    def test_filter_by_rider_email(self, auth_client, ride):
        """Test filtering by rider email"""
        url = reverse("ride-list") + "?id_rider__email=rider@example.com"
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "pickup"

    def test_order_by_pickup_time(self, auth_client, ride):
        """Test ordering rides by pickup time"""
        url = reverse("ride-list") + "?ordering=pickup_time"
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_lat_lon_filtering(self, auth_client, ride):
        """Test filtering rides by latitude and longitude"""
        url = reverse("ride-list") + "?lat=37.7749&lon=-122.4194"
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_invalid_lat_lon(self, auth_client):
        """Test invalid latitude and longitude values"""
        url = reverse("ride-list") + "?lat=200&lon=400"
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "Invalid latitude or longitude values" in response.data["error"]
