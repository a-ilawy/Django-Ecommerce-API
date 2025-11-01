import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.tests.factories.user_factory import UserFactory
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

@pytest.mark.django_db
def test_user_login(api_client, user_factory):
    user = user_factory(password="test1234")
    url = reverse("login")
    data = {"email": user.email, "password": "test1234"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data



@pytest.mark.django_db
class TestUserLogout:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("logout")

    def test_logout_with_valid_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)

        response = self.client.post(
            self.url, {"refresh": str(refresh)}, format="json"
        )

        assert response.status_code == status.HTTP_205_RESET_CONTENT
        assert response.data["message"] == "Logged out successfully"
        assert BlacklistedToken.objects.filter(token__jti=refresh["jti"]).exists()

    def test_logout_with_invalid_refresh_token(self):
        response = self.client.post(
            self.url, {"refresh": "invalidtoken"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data



@pytest.mark.django_db
class TestUserRegisterUsername:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("register")

    def test_register_without_username(self):
        data = {
            "email": "nousername@example.com",
            "password": "testpass123",
            "full_name": "Ahmed Mohamed",
            "user_type": "buyer",
        }

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert "id" in response.data or "email" in response.data

    def test_register_with_duplicate_username(self):
        user = UserFactory(username="ahmed")

        data = {
            "username": "ahmed",
            "email": "duplicate@example.com",
            "password": "testpass123",
            "full_name": "Ali Mohamed",
            "user_type": "buyer",
        }

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data
