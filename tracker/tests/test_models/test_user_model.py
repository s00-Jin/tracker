import pytest


@pytest.mark.django_db
def test_create_user(create_user):
    user = create_user("testuser@example.com", "rider")
    assert user.email == "testuser@example.com"
    assert user.role == "rider"
    assert user.is_active
