import pytest
from rest_framework.test import APIClient
from accounts.tests.factories.user_factory import UserFactory


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_factory():
    return UserFactory
