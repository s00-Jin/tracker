import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestRegisterViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup API client for tests"""
        self.client = APIClient()
        self.url = "/v1/register/"

    def test_register_success(self):
        """Test successful user registration"""
        payload = {
            "email": "testuser@example.com",
            "password": "SecurePassword123",
            "re_password": "SecurePassword123",
            "role": "rider",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "Successfully Registered."
        assert User.objects.filter(email=payload["email"]).exists()

    def test_register_password_mismatch(self):
        """Test registration failure due to password mismatch"""
        payload = {
            "email": "testuser@example.com",
            "password": "SecurePassword123",
            "re_password": "WrongPassword123",
            "role": "rider",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == [
            "password and re_password fields didn't match"
        ]

    def test_register_missing_fields(self):
        """Test registration failure due to missing required fields"""
        payload = {
            "email": "invalid@example.com",
            "password": "SecurePassword123",
            "re_password": "SecurePassword123",
        }
        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["role"] == ["This field is required."]
        assert response.data["phone_number"] == ["This field is required."]

    def test_register_invalid_email(self):
        """Test registration with an invalid email format"""
        payload = {
            "email": "invalid-email",
            "password": "SecurePassword123",
            "re_password": "SecurePassword123",
            "role": "rider",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["email"] == ["Enter a valid email address."]

    def test_register_duplicate_email(self):
        """Test registration failure when email is already taken"""
        User.objects.create_user(
            email="testuser@example.com",
            password="SecurePassword123",
            role="rider",
            phone_number="1234567890",
        )

        payload = {
            "email": "testuser@example.com",
            "password": "NewPassword123",
            "re_password": "NewPassword123",
            "role": "rider",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "0987654321",
        }
        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["email"] == ["custom user with this email already exists."]
