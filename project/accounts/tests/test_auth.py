import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_user_register(api_client):
    url = reverse("register")  # لازم يكون اسم الـ path في urls.py = "register"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test1234",
        "user_type": "buyer",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "email" in response.data
    assert response.data["email"] == "test@example.com"


@pytest.mark.django_db
def test_user_login(api_client, user_factory):
    user = user_factory(password="test1234")
    url = reverse("login")  # لو انت مسميها "login" غيّرها
    data = {"username": user.username, "password": "test1234"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
